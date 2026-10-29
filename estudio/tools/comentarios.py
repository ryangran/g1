"""Lê os comentários de um Reel e gera o resumo que abre o próximo episódio.

Resumo: placar (um voto por pessoa, vale o último comentário antes do fechamento), quem achou o
3º jeito primeiro (e quantos minutos depois do post), e os comentários mais curtidos para citar.
As regras de voto são as mesmas do placar do site (site/lib/contagem.js).

Fonte dos comentários (escolha uma):
  --instagram           API do Instagram: token em IG_TOKEN ou em estudio/.chaves/instagram.key
                        (o Reel é o post mais recente, ou --media <id>, ou --link <url do reel>)
  --arquivo c.json      lista de {"username", "text", "timestamp", "like_count"} (export manual)

  python3 estudio/tools/comentarios.py --instagram --opcoes ACELERA,ESPERA \
      --jeito recibo,farmacia,drogaria,antonio,acacias,endereco --fecha 2026-10-31T15:00:00-03:00 \
      --saida estudio/producoes/06-o-bilhete-p01/build/votacao.json
"""
import argparse
import json
import os
import re
import sys
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
API = "https://graph.instagram.com/v21.0"


def norm(t):
    t = unicodedata.normalize("NFD", str(t or "").lower())
    return "".join(c for c in t if not unicodedata.combining(c))


def palavras(t):
    return " " + re.sub(r"[^a-z0-9]+", " ", norm(t)) + " "


def opcao_do(texto, opcoes):
    t = palavras(texto)
    achadas = [o for o in opcoes if " " + palavras(o).strip() + " " in t]
    return achadas[0] if len(achadas) == 1 else None


def quando(ts):
    return datetime.fromisoformat(ts.replace("Z", "+00:00").replace("+0000", "+00:00"))


def pegar(url):
    try:
        with urllib.request.urlopen(url, timeout=30) as r:
            j = json.load(r)
    except urllib.error.HTTPError as e:
        j = json.load(e)
    if "error" in j:
        sys.exit(f"ERRO do Instagram: {j['error'].get('message')}")
    return j


def tokens():
    """Tokens disponíveis, na ordem: IG_TOKEN, estudio/.chaves/instagram-ig.key (login do Instagram, IG…),
    estudio/.chaves/instagram.key (Facebook, EAA…)."""
    ts = [os.environ.get("IG_TOKEN")]
    for nome in ("instagram-ig.key", "instagram.key"):
        p = os.path.join(RAIZ, ".chaves", nome)
        if os.path.exists(p):
            ts.append(open(p).read().strip())
    ts = [t for t in ts if t]
    if not ts:
        sys.exit("ERRO: sem token. Defina IG_TOKEN ou crie estudio/.chaves/instagram.key (veja site/INSTAGRAM-PASSO-A-PASSO.md)")
    return ts


def base_e_conta(t):
    """Token IG… usa graph.instagram.com/me. Token EAA… (login do Facebook) chega na conta profissional
    pela Página do Facebook ligada a ela, em graph.facebook.com."""
    tk = urllib.parse.quote(t)
    if not t.startswith("EAA"):
        return API, "me", tk
    fb = "https://graph.facebook.com/v21.0"
    paginas = pegar(f"{fb}/me/accounts?fields=name,instagram_business_account{{id,username}}&access_token={tk}").get("data", [])
    contas = [p["instagram_business_account"] for p in paginas if p.get("instagram_business_account")]
    if not contas:
        raise LookupError("token do Facebook sem Página com Instagram ligado (falta pages_show_list ou o vínculo Página↔Instagram)")
    return fb, contas[0]["id"], tk


def do_instagram(a):
    erros = []
    for t in tokens():
        try:
            base, conta, tk = base_e_conta(t)
            break
        except (LookupError, SystemExit, urllib.error.HTTPError) as e:
            erros.append(str(e))
    else:
        sys.exit("ERRO: nenhum token chegou à conta do Instagram:\n  " + "\n  ".join(erros))
    API_ = base
    media = a.media
    post_ts = None
    if not media:
        lista = pegar(f"{API_}/{conta}/media?fields=id,permalink,timestamp,caption&limit=25&access_token={tk}")["data"]
        if a.link:
            alvo = a.link.rstrip("/").split("?")[0]
            achou = [m for m in lista if m.get("permalink", "").rstrip("/").split("?")[0] == alvo]
            if not achou:
                sys.exit("ERRO: esse link não está entre os 25 posts mais recentes da conta")
            m = achou[0]
        else:
            m = lista[0]
        media, post_ts = m["id"], m.get("timestamp")
    else:
        post_ts = pegar(f"{API_}/{media}?fields=timestamp&access_token={tk}").get("timestamp")
    todos, url = [], f"{API_}/{media}/comments?fields=id,text,username,timestamp,like_count&limit=50&access_token={tk}"
    while url and len(todos) < 5000:
        j = pegar(url)
        todos += j.get("data", [])
        url = j.get("paging", {}).get("next")
    return todos, post_ts


def resumir(coms, opcoes, jeito, fecha=None, post_ts=None):
    limite = quando(fecha) if fecha else None
    coms = sorted((c for c in coms if c.get("username") and c.get("timestamp")), key=lambda c: quando(c["timestamp"]))
    ultimo, palpites, outros = {}, [], []
    for c in coms:
        if limite and quando(c["timestamp"]) > limite:
            continue
        o = opcao_do(c.get("text", ""), opcoes)
        if o:
            ultimo[c["username"]] = o
        elif jeito and any(" " + norm(k) in palavras(c.get("text", "")) for k in jeito):
            palpites.append(c)
        else:
            outros.append(c)
    total_votos = len(ultimo)
    contagem = {o: sum(1 for v in ultimo.values() if v == o) for o in opcoes}
    # o 3º jeito entra no placar como uma opção a mais (igual ao Rastro: "3º JEITO · O BINÓCULO 6%")
    quem_jeito = {c["username"] for c in palpites}
    base = total_votos + len(quem_jeito - set(ultimo))
    placar = [{"opcao": o, "votos": n, "pct": round(100 * n / base) if base else 0} for o, n in contagem.items()]
    placar.append({"opcao": "3º JEITO", "votos": len(quem_jeito), "pct": round(100 * len(quem_jeito) / base) if base else 0})
    primeiro = None
    if palpites:
        p = palpites[0]
        primeiro = {"username": p["username"], "text": p.get("text", ""), "timestamp": p["timestamp"]}
        if post_ts:
            primeiro["minutos"] = max(1, round((quando(p["timestamp"]) - quando(post_ts)).total_seconds() / 60))
    destaque = sorted((c for c in outros + palpites if len(c.get("text", "")) >= 15), key=lambda c: -int(c.get("like_count") or 0))[:8]
    return {
        "total_votos": total_votos, "placar": placar,
        "vencedor": max(placar, key=lambda x: x["votos"])["opcao"] if base else None,
        "primeiro_3o_jeito": primeiro,
        "outros_que_acharam": [c["username"] for c in palpites[1:6]],
        "destaques": [{"username": c["username"], "text": c.get("text", ""), "like_count": c.get("like_count", 0)} for c in destaque],
        "comentarios_lidos": len(coms),
    }


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    fonte = ap.add_mutually_exclusive_group(required=True)
    fonte.add_argument("--instagram", action="store_true")
    fonte.add_argument("--arquivo")
    ap.add_argument("--media"); ap.add_argument("--link")
    ap.add_argument("--opcoes", required=True); ap.add_argument("--jeito", default="")
    ap.add_argument("--fecha"); ap.add_argument("--saida")
    a = ap.parse_args()
    if a.instagram:
        coms, post_ts = do_instagram(a)
    else:
        coms, post_ts = json.load(open(a.arquivo)), None
    r = resumir(coms, [o.strip() for o in a.opcoes.split(",")], [k.strip() for k in a.jeito.split(",") if k.strip()], a.fecha, post_ts)
    if a.saida:
        os.makedirs(os.path.dirname(os.path.abspath(a.saida)), exist_ok=True)
        json.dump(r, open(a.saida, "w"), ensure_ascii=False, indent=1)
    print(f"{r['comentarios_lidos']} comentários lidos · {r['total_votos']} votos válidos")
    for p in r["placar"]:
        print(f"  {p['opcao']:<10} {p['pct']:>3}%  ({p['votos']})")
    if r["primeiro_3o_jeito"]:
        p = r["primeiro_3o_jeito"]
        print(f"1º a achar o 3º jeito: @{p['username']}" + (f" ({p['minutos']} min depois do post)" if "minutos" in p else "") + f": \"{p['text']}\"")
    for d in r["destaques"][:3]:
        print(f"  destaque @{d['username']} ({d['like_count']} curtidas): \"{d['text']}\"")
