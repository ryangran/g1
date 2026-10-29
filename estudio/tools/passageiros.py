"""Lista quem pagou o Passageiro da madrugada (Mercado Pago, Pix aprovado) e monta a lista da próxima parte.

  python3 estudio/tools/passageiros.py --parte 2 --fecha 2026-10-31T15:00:00-03:00 --saida estudio/producoes/<ep>/build/passageiros.json

Regras (as mesmas dos Termos): até 10 por parte, por ordem de pagamento; quem pagou depois do horário de fechamento
ou passou das 10 vagas fica para a parte seguinte. O número de corrida é a ordem de chegada de todos os pagamentos.
Token: MP_ACCESS_TOKEN ou estudio/.chaves/mercadopago-access-token.key (fora do git).
"""
import argparse
import json
import os
import random
import sys
import urllib.request
from datetime import datetime

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DESTINOS = ["Centro", "Rodoviária", "Aeroporto", "Hospital São Lucas", "Vila Nova", "Jardim das Acácias", "Estação Norte", "Bairro Alto", "Praça da Sé", "Zona Leste"]


def token():
    t = os.environ.get("MP_ACCESS_TOKEN")
    p = os.path.join(RAIZ, ".chaves", "mercadopago-access-token.key")
    if not t and os.path.exists(p):
        t = open(p).read().strip()
    if not t:
        sys.exit("ERRO: sem MP_ACCESS_TOKEN")
    return t


def pagamentos():
    out, offset = [], 0
    while True:
        url = f"https://api.mercadopago.com/v1/payments/search?status=approved&sort=date_approved&criteria=asc&limit=100&offset={offset}"
        req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token()}"})
        with urllib.request.urlopen(req, timeout=30) as r:
            j = json.load(r)
        res = j.get("results", [])
        out += res
        offset += len(res)
        if not res or offset >= j.get("paging", {}).get("total", 0):
            return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--parte", type=int, required=True)
    ap.add_argument("--fecha", required=True, help="fechamento da lista desta parte (ISO, com fuso)")
    ap.add_argument("--vagas", type=int, default=10)
    ap.add_argument("--saida")
    ap.add_argument("--confirmar", action="store_true", help="registra no histórico quem entrou nesta parte")
    a = ap.parse_args()
    limite = datetime.fromisoformat(a.fecha)
    pagos = [p for p in pagamentos() if (p.get("external_reference") or "").startswith("@")]
    todos = []
    for n, p in enumerate(pagos, 1):
        todos.append({"numero": n, "arroba": p["external_reference"], "pago_em": p.get("date_approved"), "id": p.get("id")})
    # quem já entrou em partes anteriores fica registrado em estudio/passageiros-historico.json
    hist_p = os.path.join(RAIZ, "passageiros-historico.json")
    usados = {x["id"] for x in json.load(open(hist_p))} if os.path.exists(hist_p) else set()
    fila = [x for x in todos if x["id"] not in usados and datetime.fromisoformat(x["pago_em"].replace("Z", "+00:00")) <= limite]
    entram, ficam = fila[: a.vagas], fila[a.vagas:]
    rnd = random.Random(a.parte)
    for i, x in enumerate(entram):
        x["hora"] = f"{(23 + i // 3) % 24:02d}:{rnd.randint(0, 59):02d}"
        x["destino"] = rnd.choice(DESTINOS)
        x["parte"] = a.parte
    if a.saida:
        os.makedirs(os.path.dirname(os.path.abspath(a.saida)), exist_ok=True)
        json.dump(entram, open(a.saida, "w"), ensure_ascii=False, indent=1)
    if a.confirmar and entram:
        hist = json.load(open(hist_p)) if os.path.exists(hist_p) else []
        json.dump(hist + entram, open(hist_p, "w"), ensure_ascii=False, indent=1)
    print(f"{len(pagos)} pagamentos aprovados · {len(entram)} entram na Parte {a.parte} · {len(ficam)} ficam para a próxima")
    for x in entram:
        print(f"  corrida nº {x['numero']:03d}  {x['arroba']:<24} {x['hora']} → {x['destino']}")
    print("Depois de publicar a parte, rode com --confirmar para registrar no histórico." if entram else "")
