"""Gera a narração por frase (Kokoro pm_alex) e grava build/timing.json com início/fim de cada frase."""
import json, os, subprocess
HF = "/tmp/claude-0/hf/node_modules/.bin/hyperframes" if os.path.exists("/tmp/claude-0/hf/node_modules/.bin/hyperframes") else "npx"
FRASES = [
    ("Você é um macaco.", 0.25),
    ("E a maior banana da selva está do outro lado do rio.", 0.3),
    ("Só tem um problema.", 0.35),
    ("O rio tem crocodilo.", 0.9),
    ("Opção um: o cipó.", 0.2),
    ("Mas ele tá rachando.", 0.75),
    ("Opção dois: as pedras.", 0.2),
    ("Só que uma delas... piscou.", 0.95),
    ("Comente CIPÓ ou PEDRA.", 0.5),
    ("E tem um terceiro jeito escondido nessa imagem.", 0.25),
    ("A parte dois sai amanhã.", 0.4),
]
LEAD = 0.15
partes, t, tempos = [], LEAD, []
env = {**os.environ, "HYPERFRAMES_PYTHON": os.environ.get("HYPERFRAMES_PYTHON", "/tmp/claude-0/kvenv/bin/python")}
for i, (txt, pausa) in enumerate(FRASES):
    f = f"build/voz/f{i:02d}.wav"
    cmd = ([HF] if HF != "npx" else ["npx", "--yes", "hyperframes@0.8.193"]) + ["tts", txt.replace("CIPÓ", "cipó").replace("PEDRA", "pedra"), "-v", "pm_alex", "-l", "pt-br", "-s", "0.93", "-o", f]
    subprocess.run(cmd, check=True, capture_output=True, env=env)
    d = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f]))
    tempos.append({"texto": txt, "ini": round(t, 3), "fim": round(t + d, 3)})
    s = f"build/voz/s{i:02d}.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", "anullsrc=r=24000:cl=mono", "-t", str(pausa), s], check=True)
    partes += [f, s]; t += d + pausa
open("build/lista.txt", "w").write("".join(f"file '{os.path.abspath(p)}'\n" for p in partes))
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", "build/lista.txt", "-af",
                f"adelay={int(LEAD*1000)},highpass=f=70,acompressor=threshold=-20dB:ratio=3:attack=5:release=120,loudnorm=I=-16:TP=-1.5:LRA=7,aresample=44100",
                "-ac", "2", "-c:a", "libmp3lame", "-b:a", "192k", "assets/audio/narracao.mp3"], check=True)
json.dump({"frases": tempos, "total": round(t, 3)}, open("build/timing.json", "w"), ensure_ascii=False, indent=1)
print(round(t, 2), "s")
for x in tempos: print(x["ini"], x["fim"], x["texto"])
