"""Cliente mínimo da API Gemini para o estúdio (imagem, voz, música).

Chave: variável GEMINI_API_KEY ou arquivo estudio/.chaves/gemini.key.

  python3 estudio/tools/gemini.py imagem "<prompt>" saida.png [--ref ref1.png ...] [--aspecto 9:16] [--modelo gemini-3-pro-image]
  python3 estudio/tools/gemini.py voz "<texto>" saida.wav [--voz Orus] [--estilo "..."] [--modelo gemini-2.5-pro-preview-tts]
  python3 estudio/tools/gemini.py musica "<prompt>" saida.mp3 [--modelo lyria-3-clip-preview]
"""
import argparse
import base64
import json
import os
import sys
import urllib.request
import wave

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
API = "https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent"


def chave():
    k = os.environ.get("GEMINI_API_KEY")
    if not k:
        p = os.path.join(RAIZ, ".chaves", "gemini.key")
        k = open(p).read().strip()
    return k


def chamar(modelo, corpo, tempo=300):
    req = urllib.request.Request(API.format(m=modelo), data=json.dumps(corpo).encode(), headers={"Content-Type": "application/json", "x-goog-api-key": chave()})
    try:
        with urllib.request.urlopen(req, timeout=tempo) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        sys.exit(f"ERRO {e.code}: {e.read().decode()[:800]}")


def partes_inline(resp):
    out = []
    for c in resp.get("candidates", []):
        for p in c.get("content", {}).get("parts", []):
            if "inlineData" in p:
                out.append(p["inlineData"])
            elif "text" in p:
                print("texto:", p["text"][:300], file=sys.stderr)
    return out


def imagem(a):
    partes = []
    for r in a.ref or []:
        mime = "image/png" if r.endswith(".png") else "image/jpeg"
        partes.append({"inlineData": {"mimeType": mime, "data": base64.b64encode(open(r, "rb").read()).decode()}})
    partes.append({"text": a.prompt})
    corpo = {"contents": [{"parts": partes}], "generationConfig": {"responseModalities": ["IMAGE"], "imageConfig": {"aspectRatio": a.aspecto}}}
    imgs = partes_inline(chamar(a.modelo, corpo))
    if not imgs:
        sys.exit("ERRO: nenhuma imagem retornada")
    open(a.saida, "wb").write(base64.b64decode(imgs[0]["data"]))
    print("ok", a.saida, imgs[0].get("mimeType"))


def voz(a):
    texto = (a.estilo + "\n\n" if a.estilo else "") + a.prompt
    corpo = {"contents": [{"parts": [{"text": texto}]}], "generationConfig": {"responseModalities": ["AUDIO"], "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": a.voz}}}}}
    aud = partes_inline(chamar(a.modelo, corpo))
    if not aud:
        sys.exit("ERRO: nenhum áudio retornado")
    pcm = base64.b64decode(aud[0]["data"])
    taxa = 24000
    mt = aud[0].get("mimeType", "")
    if "rate=" in mt:
        taxa = int(mt.split("rate=")[1].split(";")[0])
    with wave.open(a.saida, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(taxa); w.writeframes(pcm)
    print("ok", a.saida, mt, f"{len(pcm) / 2 / taxa:.2f}s")


def musica(a):
    corpo = {"contents": [{"parts": [{"text": a.prompt}]}], "generationConfig": {"responseModalities": ["AUDIO"]}}
    aud = partes_inline(chamar(a.modelo, corpo, 600))
    if not aud:
        sys.exit("ERRO: nenhum áudio retornado")
    dados = base64.b64decode(aud[0]["data"])
    mt = aud[0].get("mimeType", "")
    if "L16" in mt or "pcm" in mt:
        taxa = int(mt.split("rate=")[1].split(";")[0]) if "rate=" in mt else 48000
        with wave.open(a.saida.rsplit(".", 1)[0] + ".wav", "wb") as w:
            w.setnchannels(2); w.setsampwidth(2); w.setframerate(taxa); w.writeframes(dados)
    else:
        open(a.saida, "wb").write(dados)
    print("ok", a.saida, mt, len(dados))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("tipo", choices=["imagem", "voz", "musica"])
    ap.add_argument("prompt"); ap.add_argument("saida")
    ap.add_argument("--ref", nargs="*"); ap.add_argument("--aspecto", default="9:16")
    ap.add_argument("--voz", default="Orus"); ap.add_argument("--estilo", default="")
    ap.add_argument("--modelo")
    a = ap.parse_args()
    a.modelo = a.modelo or {"imagem": "gemini-3-pro-image", "voz": "gemini-2.5-pro-preview-tts", "musica": "lyria-3-clip-preview"}[a.tipo]
    {"imagem": imagem, "voz": voz, "musica": musica}[a.tipo](a)
