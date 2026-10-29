"""Narração com a voz fixa do estúdio (Gemini TTS, voz Orus) → assets/audio/narracao.mp3 + build/timing.json.

1. Gera o texto inteiro numa chamada só (mesma voz e mesmo tom do começo ao fim).
2. Encurta as pausas longas (máx. PAUSA_MAX s) para manter o ritmo de reel.
3. Transcreve (whisper) para ter o tempo de cada palavra; as legendas usam esses tempos.
Uso (na pasta do episódio): python3 tools/narracao_google.py [--sem-gerar]
"""
import json, os, re, subprocess, sys

FRASES = [
    "Uma da manhã. O Clóvis, taxista há vinte e dois anos, acabou de deixar um passageiro de terno na porta de um hotel.",
    "Quando olhou pra trás, tinha um bilhete de loteria no banco.",
    "Ele conferiu os números no celular. Um, dois, três… os seis.",
    "Quarenta milhões de reais.",
    "No banco de trás de um táxi com a parcela atrasada há três meses.",
    "Agora vem a parte difícil. Porque todo prêmio… tem dono.",
    "Problema um: o passageiro. Em dois minutos ele percebe o que esqueceu.",
    "E ele lembra de tudo: táxi branco, placa final sete, a música que tava tocando.",
    "Problema dois: a central. Toda corrida fica no sistema. Hora, endereço… e o nome do motorista.",
    "Problema três: o Clóvis virou o bilhete. Atrás, escrito à caneta: Seu Antônio. E um telefone.",
    "Seu Antônio. Mas o passageiro… não era nenhum Antônio.",
    "Ele saiu do hotel correndo, com o telefone na orelha. E o Clóvis ouviu: Achei o táxi do velho.",
    "Regra número um: todo bilhete tem dois donos. Quem comprou… e quem tá com ele.",
    "O que a gente faz agora? Opção A: acelerar e sumir na madrugada. Comente ACELERA.",
    "Opção B: esperar o homem e devolver o bilhete. Comente ESPERA.",
    "Ou tem um terceiro jeito escondido nessa cena. Só vale se você disser qual é.",
    "A maioria escreve a parte dois amanhã.",
]
VOZ = "Orus"  # voz fixa do estúdio: ver estudio/VOZ.md
ESTILO = open(os.path.join(os.path.dirname(__file__), "../../../VOZ-ESTILO.txt")).read().strip()
PAUSA_MAX, LEAD = 0.38, 0.15
HF = "/tmp/claude-0/hf/node_modules/.bin/hyperframes"
os.makedirs("build/gvoz", exist_ok=True)
bruto = "build/gvoz/narracao.wav"

if "--sem-gerar" not in sys.argv:
    texto = "\n".join(f.replace("ACELERA", "acelera").replace("ESPERA", "espera") for f in FRASES)
    subprocess.run([sys.executable, "../../tools/gemini.py", "voz", texto, bruto, "--voz", VOZ, "--modelo", "gemini-2.5-flash-preview-tts", "--estilo", ESTILO], check=True)

# pausas longas → PAUSA_MAX (corta o miolo do silêncio)
log = subprocess.run(["ffmpeg", "-nostdin", "-i", bruto, "-af", "silencedetect=n=-38dB:d=0.2", "-f", "null", "-"], capture_output=True, text=True).stderr
ini = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", log)]
fim = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", log)]
dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", bruto]))
manter, t = [], 0.0
for a, b in zip(ini, fim):
    corta = (b - a) - PAUSA_MAX
    if a == 0:  # silêncio inicial: some inteiro
        t = max(0, b - 0.05); continue
    if corta > 0:
        manter.append((t, a + PAUSA_MAX / 2)); t = b - PAUSA_MAX / 2
manter.append((t, dur))
sel = "+".join(f"between(t,{a:.3f},{b:.3f})" for a, b in manter)
limpo = "build/gvoz/limpo.wav"
subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", bruto, "-af", f"aselect='{sel}',asetpts=N/SR/TB", limpo], check=True)
subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", limpo, "-af",
                f"adelay={int(LEAD * 1000)},highpass=f=70,acompressor=threshold=-20dB:ratio=3:attack=5:release=120,loudnorm=I=-15:TP=-1.5:LRA=7,aresample=44100",
                "-ac", "2", "-c:a", "libmp3lame", "-b:a", "192k", "assets/audio/narracao.mp3"], check=True)

# tempos por palavra (whisper) — o texto exibido é sempre o do roteiro, só o tempo vem da transcrição
env = {**os.environ, "NODE_USE_ENV_PROXY": "1", "NODE_EXTRA_CA_CERTS": "/root/.ccr/ca-bundle.crt", "HYPERFRAMES_SKIP_SKILLS": "1"}
subprocess.run([HF, "transcribe", "assets/audio/narracao.mp3", "-e", "whisper", "-m", "small", "-l", "pt", "--json"], check=True, capture_output=True, env=env)
os.replace(next(p for p in ("transcript.json", "assets/audio/transcript.json") if os.path.exists(p)), "build/gvoz/transcript.json")
tr = json.load(open("build/gvoz/transcript.json"))
ws = tr["words"] if isinstance(tr, dict) else tr
import difflib, unicodedata
def norm(w):
    w = unicodedata.normalize("NFD", w.lower())
    return "".join(c for c in w if c.isalnum() and not unicodedata.combining(c))
rot = [(fi, p) for fi, f in enumerate(FRASES) for p in f.split()]
tr_n, rot_n = [norm(w["text"]) for w in ws], [norm(p) for _, p in rot]
tempos = [None] * len(rot)
for bl in difflib.SequenceMatcher(None, rot_n, tr_n, autojunk=False).get_matching_blocks():
    for d in range(bl.size):
        w = ws[bl.b + d]; tempos[bl.a + d] = (w["start"], w["end"])
casadas = sum(t is not None for t in tempos)
if casadas < 0.6 * len(rot):
    sys.exit(f"ERRO: só {casadas}/{len(rot)} palavras do roteiro batem com a transcrição: " + " ".join(w["text"] for w in ws))
# palavras sem par: interpola entre as vizinhas casadas
i = 0
while i < len(rot):
    if tempos[i] is None:
        j = i
        while j < len(rot) and tempos[j] is None: j += 1
        t0 = tempos[i - 1][1] if i else 0.0
        t1 = tempos[j][0] if j < len(rot) else ws[-1]["end"]
        passo = (t1 - t0) / (j - i)
        for k in range(i, j): tempos[k] = (t0 + passo * (k - i), t0 + passo * (k - i + 1))
        i = j
    i += 1
frases = []
for fi, f in enumerate(FRASES):
    pal = [{"p": p, "ini": round(tempos[k][0], 3), "fim": round(tempos[k][1], 3)} for k, (g, p) in enumerate(rot) if g == fi]
    frases.append({"texto": f, "ini": pal[0]["ini"], "fim": pal[-1]["fim"], "palavras": pal})
print(f"alinhamento: {casadas}/{len(rot)} palavras casadas")
total = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", "assets/audio/narracao.mp3"]))
json.dump({"voz": f"gemini-tts:{VOZ}", "frases": frases, "total": round(total, 3)}, open("build/timing.json", "w"), ensure_ascii=False, indent=1)
print(round(total, 2), "s")
for x in frases: print(x["ini"], x["fim"], x["texto"])
