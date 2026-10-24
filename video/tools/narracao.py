import json, subprocess, os, sys
HF="npx"; HF_ARGS=["--yes", "hyperframes@0.8.193"]
D=sys.argv[1] if len(sys.argv) > 1 else "build/audio"; os.makedirs(D, exist_ok=True)
# scene -> list of (frase, pausa_depois_s)
scenes = [
 [("Lula votou contra o SUS?", 0.7), ("A resposta está escondida nos arquivos de mil novecentos e oitenta e oito.", 0.6)],
 [("Vinte e dois de setembro de mil novecentos e oitenta e oito.", 0.5), ("A Constituinte vota o texto final da nova Constituição.", 0.5),
  ("Quatrocentos e setenta e quatro votos a favor.", 0.4), ("Apenas quinze contra.", 0.5), ("Todos do PT.", 0.7)],
 [("E entre eles, estava o líder da bancada.", 0.5), ("Luiz Inácio Lula da Silva.", 0.5), ("Ele votou não.", 0.5),
  ("Para o partido, o texto era conservador demais.", 0.6)],
 [("Só que foi exatamente essa Constituição que criou o SUS.", 0.5), ("A saúde, direito de todos e dever do Estado.", 0.7)],
 [("Mas atenção.", 0.4), ("O voto foi contra o texto inteiro, não contra um artigo do SUS.", 0.5),
  ("E, dias depois, Lula assinou a Constituição.", 0.7)],
 [("O veredito?", 0.5), ("Lula votou contra a Constituição que criou o SUS.", 0.3), ("Fato.", 0.6),
  ("Mas a história completa é mais complicada do que parece.", 1.5)],
]
out = []
n = 0
for si, sc in enumerate(scenes):
    parts = []
    for text, pause in sc:
        f = f"{D}/seg{n:02d}.wav"; n += 1
        subprocess.run([HF, *HF_ARGS, "tts", text, "-v", "pm_alex", "-l", "pt-br", "-s", "0.88", "-o", f], check=True, capture_output=True, env={**os.environ, "HYPERFRAMES_PYTHON": os.environ.get("HYPERFRAMES_PYTHON", "python3")})
        sil = f"{D}/sil{n:02d}.wav"
        subprocess.run(["ffmpeg","-v","error","-y","-f","lavfi","-i","anullsrc=r=24000:cl=mono","-t",str(pause),sil], check=True)
        parts += [f, sil]
    lst = f"{D}/scene{si}.txt"; open(lst,"w").write("".join(f"file '{p}'\n" for p in parts))
    sf = f"{D}/scene{si}.wav"
    subprocess.run(["ffmpeg","-v","error","-y","-f","concat","-safe","0","-i",lst,"-ar","24000","-ac","1",sf], check=True)
    dur = float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",sf]))
    out.append(dur); print(si, round(dur,2))
json.dump(out, open(f"{D}/durs.json","w"))
