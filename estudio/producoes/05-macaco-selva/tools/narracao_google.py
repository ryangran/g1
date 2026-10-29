"""Narração com a voz fixa do estúdio (Gemini TTS, voz Orus) → assets/audio/narracao.mp3 + build/timing.json.

1. Gera o texto inteiro numa chamada só (mesma voz e mesmo tom do começo ao fim).
2. Encurta as pausas longas (máx. PAUSA_MAX s) para manter o ritmo de reel.
3. Transcreve (whisper) para ter o tempo de cada palavra; as legendas usam esses tempos.
Uso (na pasta do episódio): python3 tools/narracao_google.py [--sem-gerar]
"""
import json, os, re, subprocess, sys

FRASES = [
    "Você é um macaco.",
    "E a maior banana da selva está do outro lado do rio.",
    "Só tem um problema.",
    "O rio tem crocodilo.",
    "Opção um: o cipó.",
    "Mas ele tá rachando.",
    "Opção dois: as pedras.",
    "Só que uma delas... piscou.",
    "Comente CIPÓ ou PEDRA.",
    "E tem um terceiro jeito escondido nessa imagem.",
    "A parte dois sai amanhã.",
]
VOZ = "Orus"  # voz fixa do estúdio: ver estudio/VOZ.md
ESTILO = open(os.path.join(os.path.dirname(__file__), "../../../VOZ-ESTILO.txt")).read().strip()
PAUSA_MAX, LEAD = 0.38, 0.15
HF = "/tmp/claude-0/hf/node_modules/.bin/hyperframes"
os.makedirs("build/gvoz", exist_ok=True)
bruto = "build/gvoz/narracao.wav"

if "--sem-gerar" not in sys.argv:
    texto = "\n".join(f.replace("CIPÓ", "cipó").replace("PEDRA", "pedra") for f in FRASES)
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
os.replace("transcript.json", "build/gvoz/transcript.json")
tr = json.load(open("build/gvoz/transcript.json"))
ws = tr["words"] if isinstance(tr, dict) else tr
n_rot = sum(len(f.split()) for f in FRASES)
if len(ws) != n_rot:
    sys.exit(f"ERRO: transcrição tem {len(ws)} palavras, roteiro tem {n_rot}: " + " ".join(w["text"] for w in ws))
frases, k = [], 0
for f in FRASES:
    pal = []
    for p in f.split():
        pal.append({"p": p, "ini": round(ws[k]["start"], 3), "fim": round(ws[k]["end"], 3)}); k += 1
    frases.append({"texto": f, "ini": pal[0]["ini"], "fim": pal[-1]["fim"], "palavras": pal})
total = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", "assets/audio/narracao.mp3"]))
json.dump({"voz": f"gemini-tts:{VOZ}", "frases": frases, "total": round(total, 3)}, open("build/timing.json", "w"), ensure_ascii=False, indent=1)
print(round(total, 2), "s")
for x in frases: print(x["ini"], x["fim"], x["texto"])
