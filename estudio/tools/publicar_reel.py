"""Publica um Reel no @clovis.obilhete pela API do Instagram (envio do arquivo direto, sem hospedar o vídeo).

  python3 estudio/tools/publicar_reel.py VIDEO.mp4 --legenda LEGENDA.txt [--capa URL_DA_CAPA] [--teste]

--teste: envia e espera o Instagram processar, mas NÃO publica (o rascunho some sozinho em 24 h).
Token: IG_TOKEN ou estudio/.chaves/instagram.key; conta: estudio/instagram.json.
"""
import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
G = "https://graph.facebook.com/v21.0"


def token():
    t = os.environ.get("IG_TOKEN")
    p = os.path.join(RAIZ, ".chaves", "instagram.key")
    if not t and os.path.exists(p):
        t = open(p).read().strip()
    if not t:
        sys.exit("ERRO: sem token do Instagram (estudio/.chaves/instagram.key)")
    return t


def chamar(metodo, url, dados=None, cab=None, corpo=None):
    if dados:
        corpo = urllib.parse.urlencode(dados).encode()
    req = urllib.request.Request(url, data=corpo, method=metodo, headers=cab or {})
    try:
        with urllib.request.urlopen(req, timeout=600) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        sys.exit(f"ERRO {e.code}: {e.read().decode()[:600]}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("video", help="arquivo local (envio direto) ou URL pública https://… do vídeo"); ap.add_argument("--legenda", required=True); ap.add_argument("--capa")
    ap.add_argument("--teste", action="store_true")
    a = ap.parse_args()
    tk = token()
    conta = json.load(open(os.path.join(RAIZ, "instagram.json")))["id"]
    url_publica = a.video.startswith("https://")
    dados = {"media_type": "REELS", "caption": open(a.legenda).read().strip(), "share_to_feed": "true", "access_token": tk}
    if a.capa:
        dados["cover_url"] = a.capa
    if url_publica:  # o Instagram baixa o vídeo da URL
        dados["video_url"] = a.video
        cid = chamar("POST", f"{G}/{conta}/media", dados)["id"]
        print(f"rascunho {cid} · o Instagram está baixando o vídeo…", flush=True)
    else:  # envio direto do arquivo
        dados["upload_type"] = "resumable"
        c = chamar("POST", f"{G}/{conta}/media", dados)
        cid, uri = c["id"], c["uri"]
        tam = os.path.getsize(a.video)
        print(f"rascunho {cid} · enviando {tam / 1e6:.1f} MB…", flush=True)
        r = chamar("POST", uri, corpo=open(a.video, "rb").read(), cab={"Authorization": f"OAuth {tk}", "offset": "0", "file_size": str(tam)})
        print("envio:", r, flush=True)
    for _ in range(90):  # até ~15 min processando
        st = chamar("GET", f"{G}/{cid}?fields=status_code,status&access_token={urllib.parse.quote(tk)}")
        print("status:", st.get("status_code"), st.get("status", ""), flush=True)
        if st.get("status_code") == "FINISHED":
            break
        if st.get("status_code") in ("ERROR", "EXPIRED"):
            sys.exit(f"ERRO no processamento: {st}")
        time.sleep(10)
    else:
        sys.exit("ERRO: o Instagram não terminou de processar a tempo")
    if a.teste:
        print("TESTE OK: o Instagram aceitou o vídeo. Nada foi publicado.")
        sys.exit(0)
    p = chamar("POST", f"{G}/{conta}/media_publish", {"creation_id": cid, "access_token": tk})
    m = chamar("GET", f"{G}/{p['id']}?fields=permalink,timestamp&access_token={urllib.parse.quote(tk)}")
    print("PUBLICADO:", m.get("permalink"), m.get("timestamp"))
