"""Gera index.html do institucional da Vetrex a partir de build/timing.json.

Estilo: SaaS escuro (fundo preto, ondas roxas, cards de interface) com legendas curtas que
trocam a cada poucas palavras, cortes marcados e som de impacto.
Uso: python3 tools/narracao_google.py && python3 tools/montar.py
"""
import json
import unicodedata

T = json.load(open("build/timing.json"))
F = T["frases"]
FIM = round(T["total"] + 2.8, 2)

ROXO, ROXO2 = "#7c3aed", "#c084fc"
ZONA_UI = (250, 1340)      # faixa onde moram as interfaces
ZONA_CAP = 1440            # topo da faixa de legenda (nunca encosta na UI)
PILULA = {"vetrex", "automatico", "bot", "menor", "link", "telegram", "publico", "sozinho"}


def norm(w):
    w = unicodedata.normalize("NFD", w.lower())
    return "".join(c for c in w if c.isalnum() and not unicodedata.combining(c))


def ini(i):
    return F[i]["ini"]


def pal(i, palavra, n=0):
    achadas = [p["ini"] for p in F[i]["palavras"] if norm(p["p"]).startswith(norm(palavra))]
    return achadas[n] if achadas else F[i]["ini"]


js = []
CENAS = []
SFX = []


# ---------------------------------------------------------------- legendas em blocos curtos
def legendas():
    """Blocos de no máximo 3 palavras; cada um some antes do próximo entrar."""
    blocos = []
    for i, f in enumerate(F):
        grupo = []
        for w in f["palavras"]:
            grupo.append(w)
            if len(grupo) == 3 or (w["p"].endswith((".", ",", ":", "?", "!", "…")) and len(grupo) >= 2):
                if i not in (4, 9):
                    blocos.append(grupo)
                grupo = []
        if grupo and i not in (4, 9):
            blocos.append(grupo)
    els = []
    for n, grupo in enumerate(blocos):
        t0 = round(grupo[0]["ini"] - 0.08, 3)
        prox = blocos[n + 1][0]["ini"] - 0.08 if n + 1 < len(blocos) else grupo[-1]["fim"] + 0.6
        t1 = round(min(prox, grupo[-1]["fim"] + 0.8), 3)
        d = round(max(t1 - t0, 0.3), 3)
        texto = " ".join(f'<span class="{"pil" if norm(w["p"]) in PILULA else ""}">{w["p"]}</span>' for w in grupo)
        cid = f"cap{n}"
        els.append(f'        <div id="{cid}" class="clip cap" data-start="{t0}" data-duration="{d}" data-track-index="{n}"><div id="{cid}-in" class="cap-in">{texto}</div></div>')
        js.append(f'tl.fromTo("#{cid}-in", {{ y: 52, scale: 0.9, opacity: 0 }}, {{ y: 0, scale: 1, opacity: 1, duration: 0.22, ease: "back.out(2.2)", immediateRender: false }}, {round(t0 + 0.02, 3)});')
        js.append(f'tl.to("#{cid}-in", {{ y: -24, opacity: 0, duration: 0.09, ease: "power2.in", immediateRender: false }}, {round(t0 + d - 0.09, 3)});')
    return els


# ---------------------------------------------------------------- interfaces
def chat():
    msgs = "".join(
        f'<div class="ch-l" id="ch{n}"><div class="ch-g"><b>{g}</b><small>{m} membros</small></div>'
        f'<div class="ch-b">🔥 Promoção de hoje…</div><div class="ch-v">visto por {v}</div></div>'
        for n, (g, m, v) in enumerate((("Grupo Vendas BR", "248", "11"), ("Revenda Oficial", "186", "7"), ("Oportunidades 03", "312", "9"))))
    return f'<div class="card chat">{msgs}</div>'


def status():
    bolas = "".join(f'<div class="st" id="st{n}"><span></span></div>' for n in range(5))
    return f'''<div class="fone">
  <div class="fone-top"><span class="dot"></span>WhatsApp · status</div>
  <div class="st-row">{bolas}</div>
  <div class="st-leg" id="st-leg">sua arte no status, todo dia</div>
</div>'''


def grupos():
    linhas = "".join(f'<div class="gl" id="gl{n}"><span class="gl-p"></span><b>{g}</b><i id="gl-n{n}">0</i></div>'
                     for n, g in enumerate(("Grupo Vendas BR", "Revenda Oficial", "Oportunidades 03", "Atacado Geral", "Players Brasil", "Mercado Livre BR")))
    return f'<div class="fone"><div class="fone-top"><span class="dot"></span>WhatsApp · grupos</div><div class="gl-wrap">{linhas}</div></div>'


def fluxo():
    passos = (("✍️", "Você escreve", "uma vez só"), ("📅", "Escolhe os dias", "1, 7, 15, 30"),
              ("🤖", "O bot dispara", "todo dia, sozinho"), ("👀", "Seu público vê", "grupos e status"))
    itens = "".join(f'<div class="fx" id="fx{n}"><div class="fx-ic">{ic}</div><b>{t}</b><small>{s}</small></div>' for n, (ic, t, s) in enumerate(passos))
    return f'<div class="fluxo"><div class="fx-linha" id="fx-linha"></div>{itens}</div>'


def preco_grande():
    return '<div class="pg"><div class="pg-n" id="pg-n">R$ 10</div><div class="pg-d" id="pg-d">POR DIA</div></div>'


PLANOS = (("1 dia", "R$ 10", 100), ("7 dias", "menos por dia", 76), ("15 dias", "menos ainda", 56), ("30 dias", "o melhor preço", 36))


def barras():

    itens = "".join(f'''<div class="pr" id="pr{n}"><div class="pr-top"><b>{d}</b><span>{v}</span></div>
  <div class="pr-trilho"><i id="pr-b{n}" style="width: {w}%"></i></div></div>''' for n, (d, v, w) in enumerate(PLANOS))
    return f'<div class="card precos"><div class="kick">VALOR POR DIA</div>{itens}</div>'


def links():
    itens = "".join(f'<div class="lk" id="lk{n}"><div class="lk-ic">🔗</div><div><b>{t}</b><small>{s}</small></div></div>'
                    for n, (t, s) in enumerate((("Grupos de vendas", "público comprador"), ("Grupos de nicho", "escolha o tema"), ("Entrega na hora", "link direto no bot"))))
    return f'<div class="grade">{itens}</div>'


def bot():
    botoes = "".join(f'<div class="bt-b" id="bt{n}">{t}</div>' for n, t in enumerate(("📣 Divulgar em grupos", "📲 Divulgar no status", "🔗 Comprar link de grupo", "💳 Adicionar saldo", "📊 Minhas campanhas")))
    return f'''<div class="fone" id="fone-bot">
  <div class="fone-top tg"><span class="dot az"></span>Telegram · @vetrexzapbot</div>
  <div class="bt-msg">Bem-vindo à <b>Vetrex</b>. O que você quer fazer?</div>
  {botoes}
</div>'''


def semgrilo():
    nao = "".join(f'<div class="ng" id="ng{n}"><span>✕</span>{t}</div>' for n, t in enumerate(("painel complicado", "programa pra instalar", "equipe pra operar")))
    return f'<div class="grade">{nao}<div class="ng sim" id="ng-sim"><span>✓</span>só o bot no Telegram</div></div>'


def lock(cid, grande=False):
    return (f'<div class="lock{" big" if grande else ""}" id="{cid}">'
            f'<img class="x" src="assets/img/marca-x.png" alt="" /><span class="bar"></span>'
            f'<img class="wm" src="assets/img/wordmark-sm.png" alt="" /></div>')


def fecho():
    return f'''<div class="fecho-in">
  {lock("fc-lock", True)}
  <div class="fc-sl" id="fc-sl">O seu recado onde o seu <span class="pil">público</span> já está.</div>
  <div class="fc-ar" id="fc-ar">t.me/vetrexzapbot</div>
</div>'''


# ---------------------------------------------------------------- cenas
def cena(cid, conteudo, t0, t1, centro=False, zoom=1, cheia=False):
    n = len(CENAS)
    t0, t1 = round(t0, 3), round(t1, 3)
    d = round(t1 - t0, 3)
    CENAS.append(f'      <div id="{cid}" class="clip cena{" centro" if centro else ""}{" cheia" if cheia else ""}" data-start="{t0}" data-duration="{d}" '
                 f'data-track-index="{40 + n}" data-track-kind="graphics"><div class="palco" id="{cid}-p">{conteudo}</div></div>')
    a, b = (1.0, 1.07) if zoom > 0 else (1.07, 1.0)
    js.append(f'tl.fromTo("#{cid}-p", {{ y: 46, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.34, ease: "power3.out", immediateRender: false }}, {t0});')
    js.append(f'tl.fromTo("#{cid}-p", {{ scale: {a} }}, {{ scale: {b}, duration: {d}, ease: "none", immediateRender: false }}, {t0});')
    js.append(f'tl.fromTo("#sweep", {{ x: -1300 }}, {{ x: 1300, duration: 0.4, ease: "power2.inOut", immediateRender: false }}, {round(t0 - 0.16, 3)});')
    js.append(f'tl.fromTo("#sweep", {{ opacity: 0.85 }}, {{ opacity: 0, duration: 0.12, immediateRender: false }}, {round(t0 + 0.16, 3)});')
    SFX.append((f"wh{n}", "whoosh-cinematic", t0 - 0.2, 1.0, 0.45))
    SFX.append((f"im{n}", "impact-bass-1", t0 - 0.04, 2.115, 0.6))
    return t0, t1


T_MARCA = ini(1)
T_STATUS = ini(2)
T_GRUPOS = pal(2, "em")
T_FLUXO = ini(3)
T_TRES = ini(4)
T_PRECO = ini(5)
T_BARRAS = pal(5, "quanto")
T_LINKS = ini(6)
T_BOT = ini(7)
T_SEM = ini(8)
T_FECHO = ini(9)

cena("c1", chat(), 0.0, T_MARCA - 0.12)
cena("c2", lock("m-lock", True), T_MARCA - 0.12, T_STATUS - 0.12, centro=True, zoom=-1)
cena("c3", status(), T_STATUS - 0.12, T_GRUPOS - 0.12)
cena("c4", grupos(), T_GRUPOS - 0.12, T_FLUXO - 0.12)
cena("c5", fluxo(), T_FLUXO - 0.12, T_TRES - 0.12, zoom=-1)
cena("c6", '<div class="tres" id="tres"></div>', T_TRES - 0.12, T_PRECO - 0.12, centro=True)
cena("c7", preco_grande(), T_PRECO - 0.12, T_BARRAS - 0.12, centro=True, zoom=-1)
cena("c8", barras(), T_BARRAS - 0.12, T_LINKS - 0.12)
cena("c9", links(), T_LINKS - 0.12, T_BOT - 0.12, zoom=-1)
cena("c10", bot(), T_BOT - 0.12, T_SEM - 0.12)
cena("c11", semgrilo(), T_SEM - 0.12, T_FECHO - 0.25, zoom=-1)
cena("c12", fecho(), T_FECHO - 0.25, FIM, centro=True, cheia=True)

# ---------------------------------------------------------------- animações dentro das cenas
for n in range(3):
    t = 0.3 + n * 0.42
    js.append(f'tl.fromTo("#ch{n}", {{ x: 70, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.4, ease: "power3.out", immediateRender: false }}, {round(t, 3)});')
    SFX.append((f"ck{n}", "click-soft", t, 0.365, 0.5))

js.append(f'tl.fromTo("#m-lock", {{ scale: 0.82, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.5, ease: "back.out(1.7)", immediateRender: false }}, {round(T_MARCA - 0.02, 3)});')
js.append(f'tl.fromTo("#m-lock .wm", {{ clipPath: "inset(0 100% 0 0)" }}, {{ clipPath: "inset(0 0% 0 0)", duration: 0.45, ease: "power2.out", immediateRender: false }}, {round(T_MARCA + 0.26, 3)});')
js.append(f'tl.fromTo("#m-lock .x", {{ rotation: -26 }}, {{ rotation: 0, duration: 0.6, ease: "back.out(2)", transformOrigin: "50% 50%", immediateRender: false }}, {round(T_MARCA - 0.02, 3)});')
SFX.append(("gl", "glitch-1", T_MARCA - 0.12, 2.638, 0.4))
SFX.append(("spk", "sparkle", T_MARCA + 0.2, 1.802, 0.5))

for n in range(5):
    t = T_STATUS + 0.12 + n * 0.1
    js.append(f'tl.fromTo("#st{n}", {{ scale: 0.3, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.3, ease: "back.out(2.6)", immediateRender: false }}, {round(t, 3)});')
    SFX.append((f"pp{n}", "pop", t, 0.72, 0.35))
js.append(f'tl.fromTo("#st-leg", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3, immediateRender: false }}, {round(T_STATUS + 0.6, 3)});')

for n in range(6):
    t = T_GRUPOS + 0.1 + n * 0.13
    js.append(f'tl.fromTo("#gl{n}", {{ x: 50, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.3, ease: "power3.out", immediateRender: false }}, {round(t, 3)});')
    js.append(f'tl.fromTo("#gl-n{n}", {{ textContent: 0 }}, {{ textContent: {240 + n * 137}, duration: 0.9, ease: "power1.out", snap: {{ textContent: 1 }}, immediateRender: false }}, {round(t + 0.1, 3)});')
    SFX.append((f"kp{n}", "key-press", t, 0.432, 0.3))

js.append(f'tl.fromTo("#fx-linha", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 1.0, ease: "power2.inOut", transformOrigin: "0% 50%", immediateRender: false }}, {round(T_FLUXO + 0.1, 3)});')
for n in range(4):
    t = T_FLUXO + 0.15 + n * 0.26
    js.append(f'tl.fromTo("#fx{n}", {{ y: 40, scale: 0.9, opacity: 0 }}, {{ y: 0, scale: 1, opacity: 1, duration: 0.32, ease: "back.out(2)", immediateRender: false }}, {round(t, 3)});')
    SFX.append((f"pg{n}", "pop", t, 0.72, 0.3))

TRES = ("Escolheu.", "Pagou.", "Disparou.")
CENAS[5] = CENAS[5].replace('<div class="tres" id="tres"></div>', '<div class="tres">' + "".join(f'<b id="t3-{n}">{p}</b>' for n, p in enumerate(TRES)) + "</div>")
for n, p in enumerate(TRES):
    t = pal(4, p.strip(".")) - 0.06
    js.append(f'tl.fromTo("#t3-{n}", {{ y: 60, scale: 0.8, opacity: 0 }}, {{ y: 0, scale: 1, opacity: 1, duration: 0.26, ease: "back.out(2.6)", immediateRender: false }}, {round(t, 3)});')
    SFX.append((f"t3{n}", "pop" if n < 2 else "impact-bass-2", t if n < 2 else t - 0.06, 0.72 if n < 2 else 2.592, 0.55))
SFX.append(("ris", "riser", max(0.0, T_TRES - 2.2), 2.4, 0.4))

js += [f'tl.fromTo("#pg-n", {{ scale: 0.6, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.4, ease: "back.out(2.4)", immediateRender: false }}, {round(T_PRECO, 3)});',
       f'tl.fromTo("#pg-d", {{ y: 24, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.3, immediateRender: false }}, {round(T_PRECO + 0.3, 3)});']
SFX.append(("prspk", "sparkle", T_PRECO, 1.802, 0.5))

for n in range(4):
    t = T_BARRAS + 0.12 + n * 0.2
    js.append(f'tl.fromTo("#pr{n}", {{ x: 60, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.3, ease: "power3.out", immediateRender: false }}, {round(t, 3)});')
    js.append(f'tl.fromTo("#pr-b{n}", {{ width: "0%" }}, {{ width: "{PLANOS[n][2]}%", duration: 0.5, ease: "power3.out", immediateRender: false }}, {round(t + 0.1, 3)});')
    SFX.append((f"pb{n}", "click", t, 0.365, 0.4))

for n in range(3):
    t = T_LINKS + 0.15 + n * 0.24
    js.append(f'tl.fromTo("#lk{n}", {{ y: 44, scale: 0.94, opacity: 0 }}, {{ y: 0, scale: 1, opacity: 1, duration: 0.32, ease: "back.out(2)", immediateRender: false }}, {round(t, 3)});')
    SFX.append((f"lkp{n}", "pop", t, 0.72, 0.3))

js.append(f'tl.fromTo("#fone-bot", {{ y: 80, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.45, ease: "power3.out", immediateRender: false }}, {round(T_BOT, 3)});')
for n in range(5):
    t = T_BOT + 0.28 + n * 0.14
    js.append(f'tl.fromTo("#bt{n}", {{ x: 46, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.26, ease: "power3.out", immediateRender: false }}, {round(t, 3)});')
    SFX.append((f"btp{n}", "key-press", t, 0.432, 0.3))

for n in range(3):
    t = T_SEM + 0.12 + n * 0.22
    js.append(f'tl.fromTo("#ng{n}", {{ x: -50, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.28, ease: "power3.out", immediateRender: false }}, {round(t, 3)});')
    SFX.append((f"ngc{n}", "click", t, 0.365, 0.4))
js.append(f'tl.fromTo("#ng-sim", {{ scale: 0.86, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.34, ease: "back.out(2.4)", immediateRender: false }}, {round(T_SEM + 0.84, 3)});')
SFX.append(("ngs", "ping", T_SEM + 0.84, 1.32, 0.5))

js += [f'tl.fromTo("#fc-lock", {{ scale: 0.86, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.6, ease: "back.out(1.6)", immediateRender: false }}, {round(T_FECHO - 0.1, 3)});',
       f'tl.fromTo("#fc-sl", {{ y: 30, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.45, ease: "power3.out", immediateRender: false }}, {round(T_FECHO + 0.45, 3)});',
       f'tl.fromTo("#fc-ar", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.45, immediateRender: false }}, {round(T_FECHO + 1.0, 3)});']
SFX.append(("fcch", "chime", T_FECHO + 0.9, 2.544, 0.4))

cap_els = legendas()
sfx = "\n".join(f'      <audio id="sfx-{i}" class="clip" src="assets/audio/{f}.mp3" data-start="{round(max(0, s), 3)}" data-duration="{d}" data-track-index="{90 + n}" data-volume="{v}"></audio>'
                for n, (i, f, s, d, v) in enumerate(SFX))

CSS = f"""
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html, body {{ width: 1080px; height: 1920px; background: #000; overflow: hidden; }}
#root {{ position: relative; width: 100%; height: 100%; font-family: "Inter", sans-serif; color: #fff; overflow: hidden; }}
#ondas {{ position: absolute; inset: 0; }}
#ondas svg {{ width: 100%; height: 100%; display: block; }}
#sweep {{ position: absolute; left: 50%; top: 0; width: 420px; height: 100%; margin-left: -210px; opacity: 0;
  background: linear-gradient(90deg, rgba(124,58,237,0) 0%, rgba(192,132,252,0.45) 50%, rgba(124,58,237,0) 100%); }}
#brand {{ position: absolute; left: 60px; top: 74px; display: flex; align-items: center; gap: 18px; opacity: 0.9; }}
#brand img.x {{ height: 38px; }} #brand img.w {{ height: 26px; }}
#brand span {{ width: 2px; height: 32px; background: #4a4a55; }}
.cena {{ position: absolute; left: 0; right: 0; top: {ZONA_UI[0]}px; height: {ZONA_UI[1] - ZONA_UI[0]}px; }}
.palco {{ position: absolute; inset: 0; padding: 0 70px; display: flex; flex-direction: column; justify-content: center; }}
.cena.centro .palco {{ align-items: center; }}
.cena.cheia {{ top: 0; height: 1920px; }}
.cap {{ position: absolute; left: 70px; right: 70px; top: {ZONA_CAP}px; height: 330px; display: flex; align-items: flex-start; justify-content: center; }}
.cap-in {{ font-family: "Outfit", "Inter", sans-serif; font-weight: 700; font-size: 100px; line-height: 1.1; letter-spacing: -0.02em; text-align: center; }}
.cap-in span {{ display: inline-block; }}
.pil {{ background: #fff; color: #000; border-radius: 16px; padding: 0 20px; }}
.card {{ background: #0b0b0e; border: 2px solid #1d1d24; border-radius: 28px; padding: 40px; }}
.kick {{ font-family: "JetBrains Mono", monospace; font-size: 29px; letter-spacing: 0.26em; color: #76767f; margin-bottom: 26px; }}
.chat .ch-l {{ background: #121218; border: 2px solid #22222b; border-radius: 20px; padding: 26px 30px; margin-bottom: 20px; }}
.chat .ch-l:last-child {{ margin-bottom: 0; }}
.ch-g {{ display: flex; align-items: baseline; gap: 16px; }}
.ch-g b {{ font-size: 36px; }} .ch-g small {{ font-size: 28px; color: #76767f; }}
.ch-b {{ margin: 14px 0 10px; font-size: 32px; color: #d7d7de; background: #1d2b24; border-radius: 14px; padding: 14px 20px; display: inline-block; }}
.ch-v {{ font-size: 28px; color: #6d6d76; }}
.fone {{ width: 100%; background: #0b0b0e; border: 2px solid #22222b; border-radius: 34px; padding: 34px; }}
.fone-top {{ display: flex; align-items: center; gap: 16px; font-size: 30px; color: #b9b9c2; margin-bottom: 26px; }}
.dot {{ width: 18px; height: 18px; border-radius: 50%; background: #25d366; }} .dot.az {{ background: #2aabee; }}
.st-row {{ display: flex; align-items: center; justify-content: space-between; margin: 10px 0 26px; }}
.st {{ width: 150px; height: 150px; border-radius: 50%; border: 7px solid {ROXO}; display: flex; align-items: center; justify-content: center; }}
.st span {{ width: 118px; height: 118px; border-radius: 50%; background: #1b1b22; display: block; }}
.st-leg {{ text-align: center; font-size: 32px; color: {ROXO2}; }}
.gl {{ display: flex; align-items: center; gap: 20px; padding: 18px 0; border-top: 2px solid #1b1b22; }}
.gl-p {{ width: 54px; height: 54px; border-radius: 16px; background: #23232c; }}
.gl b {{ flex: 1; font-size: 32px; font-weight: 600; }}
.gl i {{ font-style: normal; font-family: "JetBrains Mono", monospace; font-size: 30px; color: {ROXO2}; }}
.fluxo {{ position: relative; display: grid; grid-template-columns: repeat(2, 1fr); gap: 26px; }}
.fx-linha {{ position: absolute; left: 10%; right: 10%; top: 50%; height: 3px; background: linear-gradient(90deg, {ROXO}, {ROXO2}); opacity: 0.5; }}
.fx {{ background: #0e0e13; border: 2px solid #22222b; border-radius: 24px; padding: 32px; }}
.fx-ic {{ font-size: 52px; margin-bottom: 12px; }}
.fx b {{ display: block; font-size: 38px; margin-bottom: 6px; }}
.fx small {{ font-size: 29px; color: #83838d; }}
.tres {{ text-align: center; }}
.tres b {{ display: block; font-family: "Outfit", "Inter", sans-serif; font-size: 132px; font-weight: 700; letter-spacing: -0.03em; line-height: 1.08; }}
.pg {{ text-align: center; }}
.pg-n {{ font-family: "Outfit", "Inter", sans-serif; font-size: 280px; font-weight: 700; letter-spacing: -0.04em; line-height: 1; }}
.pg-d {{ font-family: "JetBrains Mono", monospace; font-size: 46px; letter-spacing: 0.22em; color: {ROXO2}; margin-top: 10px; }}
.precos .pr {{ margin-bottom: 26px; }} .precos .pr:last-child {{ margin-bottom: 0; }}
.pr-top {{ display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 12px; }}
.pr-top b {{ font-size: 44px; }} .pr-top span {{ font-size: 30px; color: #8c8c96; }}
.pr-trilho {{ height: 20px; background: #1b1b22; border-radius: 10px; overflow: hidden; }}
.pr-trilho i {{ display: block; height: 100%; border-radius: 10px; background: linear-gradient(90deg, {ROXO}, {ROXO2}); }}
.grade {{ display: grid; gap: 24px; width: 100%; }}
.lk {{ display: flex; align-items: center; gap: 26px; background: #0e0e13; border: 2px solid #22222b; border-radius: 24px; padding: 32px; }}
.lk-ic {{ font-size: 50px; }} .lk b {{ display: block; font-size: 40px; }} .lk small {{ font-size: 29px; color: #83838d; }}
.ng {{ display: flex; align-items: center; gap: 24px; background: #0e0e13; border: 2px solid #22222b; border-radius: 22px; padding: 30px 34px; font-size: 42px; color: #8b8b95; }}
.ng span {{ font-size: 46px; color: #e2574c; }}
.ng.sim {{ color: #fff; border-color: {ROXO}; }} .ng.sim span {{ color: #4ade80; }}
.bt-msg {{ background: #15151c; border-radius: 20px; padding: 24px 28px; font-size: 32px; color: #d4d4db; margin-bottom: 22px; }}
.bt-b {{ background: #16161d; border: 2px solid #2a2a34; border-radius: 18px; padding: 24px 28px; font-size: 34px; margin-bottom: 16px; }}
.bt-b:last-child {{ margin-bottom: 0; }}
.lock {{ display: flex; align-items: center; justify-content: center; gap: 30px; }}
.lock img.x {{ height: 110px; }} .lock img.wm {{ height: 84px; }}
.lock .bar {{ width: 3px; height: 96px; background: #55555f; }}
.lock.big {{ gap: 26px; }} .lock.big img.x {{ height: 124px; }} .lock.big img.wm {{ height: 94px; }} .lock.big .bar {{ width: 3px; height: 108px; }}
.fecho-in {{ text-align: center; }}
.fc-sl {{ max-width: 780px; margin: 56px auto 0; font-family: "Outfit", "Inter", sans-serif; font-size: 54px; font-weight: 600; line-height: 1.3; }}
.fc-sl .pil {{ padding: 0 14px; }}
.fc-ar {{ margin-top: 32px; font-family: "JetBrains Mono", monospace; font-size: 36px; color: #8c8c96; letter-spacing: 0.08em; }}
"""

ONDAS = f'''<svg viewBox="0 0 1080 1920" preserveAspectRatio="xMidYMid slice">
<defs><linearGradient id="g1" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="{ROXO}" stop-opacity="0"/><stop offset="0.45" stop-color="{ROXO2}" stop-opacity="0.75"/><stop offset="1" stop-color="{ROXO}" stop-opacity="0"/></linearGradient>
<linearGradient id="g2" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="{ROXO}" stop-opacity="0"/><stop offset="0.5" stop-color="{ROXO}" stop-opacity="0.5"/><stop offset="1" stop-color="{ROXO}" stop-opacity="0"/></linearGradient></defs>
<g id="onda-a" fill="none" stroke="url(#g1)" stroke-width="3">
  <path d="M-60 2050 C 240 1500 60 1080 320 640 C 450 420 420 180 520 -80"/>
  <path d="M60 2050 C 360 1520 180 1100 440 660 C 570 440 540 200 640 -60"/>
  <path d="M-200 2050 C 120 1540 -40 1120 220 680 C 350 460 320 220 420 -40"/>
</g>
<g id="onda-b" fill="none" stroke="url(#g2)" stroke-width="2.5">
  <path d="M1180 2050 C 880 1480 1060 1060 800 620 C 670 400 700 160 600 -100"/>
  <path d="M1300 2050 C 1000 1500 1180 1080 920 640 C 790 420 820 180 720 -80"/>
  <path d="M980 2050 C 700 1520 860 1100 620 680 C 500 460 530 220 430 -40"/>
</g>
</svg>'''

page = f'''<!doctype html>
<html lang="pt-BR">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="assets/lib/gsap.min.js"></script>
    <style>{CSS}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{FIM}" data-width="1080" data-height="1920">
      <div id="ondas" class="clip" data-start="0" data-duration="{FIM}" data-track-index="200" data-layout-ignore>{ONDAS}</div>
      <div id="sweep" class="clip" data-start="0" data-duration="{FIM}" data-track-index="201" data-layout-ignore></div>
      <div id="brand" class="clip" data-start="0" data-duration="{round(T_FECHO - 0.25, 3)}" data-track-index="202" data-layout-ignore>
        <img class="x" src="assets/img/marca-x.png" alt="" /><span></span><img class="w" src="assets/img/wordmark-sm.png" alt="" />
      </div>
{chr(10).join(CENAS)}
      <div id="legendas" class="clip" data-start="0" data-duration="{FIM}" data-track-index="203" data-track-kind="captions" style="position:absolute;inset:0">
{chr(10).join(cap_els)}
      </div>
      <audio id="trilha" class="clip" src="assets/audio/trilha.mp3" data-start="0" data-duration="{FIM}" data-track-index="80" data-volume="0.4"></audio>
      <audio id="narracao" class="clip" src="assets/audio/narracao.mp3" data-start="0" data-duration="{T["total"]:.2f}" data-track-index="81" data-volume="1"></audio>
{sfx}
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{ paused: true }});
      tl.fromTo("#onda-a", {{ y: 0, x: 0 }}, {{ y: -140, x: 22, duration: {FIM}, ease: "none" }}, 0);
      tl.fromTo("#onda-b", {{ y: 0, x: 0 }}, {{ y: 110, x: -26, duration: {FIM}, ease: "none" }}, 0);
      tl.set("#sweep", {{ opacity: 0 }}, 0);
{chr(10).join("      " + x for x in js)}
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
'''
open("index.html", "w").write(page)
print("ok", len(CENAS), "cenas ·", len(cap_els), "legendas ·", len(SFX), "sfx ·", FIM, "s")
