"""Gera index.html do institucional da Vetrex Networking a partir de build/timing.json.

Estilo: SaaS escuro (fundo preto, ondas roxas, texto cinético sincronizado com a narração,
cards de interface). Uso: python3 tools/narracao_google.py && python3 tools/montar.py
"""
import json
import unicodedata

T = json.load(open("build/timing.json"))
F = T["frases"]
FIM = round(T["total"] + 2.6, 2)

ROXO, ROXO2 = "#7c3aed", "#c084fc"


def norm(w):
    w = unicodedata.normalize("NFD", w.lower())
    return "".join(c for c in w if c.isalnum() and not unicodedata.combining(c))


def fr(i):
    return F[i]


def ini(i):
    return F[i]["ini"]


def pal(i, palavra, n=0):
    achadas = [p["ini"] for p in F[i]["palavras"] if norm(p["p"]).startswith(norm(palavra))]
    return achadas[n] if achadas else F[i]["ini"]


def fimf(i):
    return F[i]["fim"]


# ---------------------------------------------------------------- texto cinético
def bloco(i, linhas, pilulas=(), classe="fala", topo=None):
    """Monta o texto da frase i: cada palavra entra no tempo em que é falada."""
    pal_t = [(p["p"], p["ini"]) for p in F[i]["palavras"]]
    if " ".join(" ".join(linhas).split()) != " ".join(p for p, _ in pal_t):
        raise SystemExit(f"frase {i}: as linhas não batem com o roteiro\n  linhas: {' '.join(linhas)}\n  frase : {F[i]['texto']}")
    k = 0
    html, js = [], []
    for li, linha in enumerate(linhas):
        peças = []
        for palavra in linha.split():
            t = pal_t[k][1] if k < len(pal_t) else F[i]["fim"]
            k += 1
            pid = f"w{i}-{li}-{len(peças)}"
            cls = "pil" if norm(palavra).strip(".,?!") in {norm(x) for x in pilulas} else ""
            peças.append(f'<span id="{pid}" class="pl {cls}">{palavra}</span>')
            js.append(f'tl.fromTo("#{pid}", {{ y: 26, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.3, ease: "power3.out", immediateRender: false }}, {round(t - 0.07, 3)});')
        html.append('<div class="ln">' + " ".join(peças) + "</div>")
    estilo = f' style="top: {topo}px"' if topo else ""
    el = f'<div id="fala{i}" class="clip {classe}"{estilo} data-start="{round(ini(i) - 0.3, 3)}" data-duration="{round(dur_fala(i), 3)}" data-track-index="{20 + i}">' + "".join(html) + "</div>"
    return el, js


def dur_fala(i):
    fim = F[i + 1]["ini"] - 0.34 if i + 1 < len(F) else FIM
    return max(0.6, fim - (ini(i) - 0.3))


# ---------------------------------------------------------------- interfaces
def chat():
    msgs = "".join(
        f'<div class="ch-l" id="ch{n}"><div class="ch-g"><b>{g}</b><small>{m} membros</small></div>'
        f'<div class="ch-b">🔥 Promoção de hoje…</div><div class="ch-v">visto por {v}</div></div>'
        for n, (g, m, v) in enumerate((("Grupo Vendas BR", "248", "11"), ("Revenda Oficial", "186", "7"), ("Oportunidades 03", "312", "9"))))
    return f'<div class="card chat">{msgs}<div class="ch-fim" id="ch-fim">e acabou aí.</div></div>'


def status_grupos():
    linhas = "".join(f'<div class="gl" id="gl{n}"><span class="gl-p"></span><b>{g}</b><i id="gl-n{n}">0</i></div>'
                     for n, g in enumerate(("Grupo Vendas BR", "Revenda Oficial", "Oportunidades 03", "Atacado Geral", "Players Brasil", "Mercado Livre BR")))
    return f'''<div class="fone" id="fone-sg">
  <div class="fone-top"><span class="dot"></span>WhatsApp</div>
  <div class="st-row">{"".join(f'<div class="st" id="st{n}"><span></span></div>' for n in range(5))}<div class="st-lb">status</div></div>
  <div class="gl-wrap">{linhas}</div>
</div>'''


def fluxo():
    passos = (("✍️", "Você escreve", "uma vez só"), ("📅", "Escolhe os dias", "1, 7, 15, 30"), ("🤖", "O bot dispara", "todo dia, sozinho"), ("👀", "Seu público vê", "grupos e status"))
    itens = "".join(f'<div class="fx" id="fx{n}"><div class="fx-ic">{ic}</div><b>{t}</b><small>{s}</small></div>' for n, (ic, t, s) in enumerate(passos))
    return f'<div class="fluxo"><div class="fx-linha" id="fx-linha"></div>{itens}</div>'


def precos():
    planos = (("1 dia", "R$ 10", 100), ("7 dias", "menos por dia", 78), ("15 dias", "menos ainda", 58), ("30 dias", "o melhor preço", 38))
    itens = "".join(f'''<div class="pr" id="pr{n}"><div class="pr-top"><b>{d}</b><span>{v}</span></div>
  <div class="pr-trilho"><i id="pr-b{n}" style="--w: {w}%"></i></div></div>''' for n, (d, v, w) in enumerate(planos))
    return f'<div class="card precos"><div class="kick">VALOR POR DIA</div>{itens}<div class="pr-nota" id="pr-nota">quanto mais dias, menor o valor</div></div>'


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


def fecho():
    return f'''<div class="fecho-in">
  <div class="lock" id="fc-lock"><img src="assets/img/marca-x.png" alt=""><span class="bar"></span><img class="wm" src="assets/img/wordmark.png" alt=""></div>
  <div class="fc-sl" id="fc-sl">O seu recado onde o seu <span class="pil">público</span> já está.</div>
  <div class="fc-ar" id="fc-ar">t.me/vetrexzapbot</div>
</div>'''


# ---------------------------------------------------------------- planos (cena por frase)
js = []
CENAS = []


def cena(cid, conteudo, t0, t1, classe=""):
    CENAS.append(f'<div id="{cid}" class="clip cena {classe}" data-start="{round(t0, 3)}" data-duration="{round(t1 - t0, 3)}" data-track-index="{5 + len(CENAS)}" data-track-kind="graphics"><div class="palco" id="{cid}-p">{conteudo}</div></div>')


t_chat = (0.0, ini(1) - 0.1)
t_marca = (ini(1) - 0.1, ini(2) - 0.1)
t_sg = (ini(2) - 0.1, ini(3) - 0.1)
t_fx = (ini(3) - 0.1, ini(4) - 0.1)
t_3b = (ini(4) - 0.1, ini(5) - 0.1)
t_pr = (ini(5) - 0.1, ini(6) - 0.1)
t_lk = (ini(6) - 0.1, ini(7) - 0.1)
t_bot = (ini(7) - 0.1, ini(9) - 0.1)
t_fc = (ini(9) - 0.25, FIM)

cena("c1", chat(), *t_chat)
cena("c2", '<div class="lock big" id="m-lock"><img src="assets/img/marca-x.png" alt=""><span class="bar"></span><img class="wm" src="assets/img/wordmark.png" alt=""></div>', *t_marca, classe="centro")
cena("c3", status_grupos(), *t_sg)
cena("c4", fluxo(), *t_fx)
cena("c5", '<div class="tres" id="tres"></div>', *t_3b, classe="centro")
cena("c6", precos(), *t_pr)
cena("c7", links(), *t_lk)
cena("c8", bot(), *t_bot)
cena("c9", fecho(), *t_fc, classe="centro")

# animações das interfaces
for n in range(3):
    js.append(f'tl.fromTo("#ch{n}", {{ x: 60, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.45, ease: "power3.out", immediateRender: false }}, {round(0.35 + n * 0.45, 3)});')
js.append(f'tl.fromTo("#ch-fim", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.4, immediateRender: false }}, {round(pal(0, "parou") - 0.1, 3)});')
js.append(f'tl.fromTo("#m-lock", {{ scale: 0.86, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.7, ease: "power3.out", immediateRender: false }}, {round(t_marca[0] + 0.1, 3)});')
js.append(f'tl.fromTo("#m-lock .wm", {{ clipPath: "inset(0 100% 0 0)" }}, {{ clipPath: "inset(0 0% 0 0)", duration: 0.6, ease: "power2.out", immediateRender: false }}, {round(t_marca[0] + 0.45, 3)});')

for n in range(5):
    js.append(f'tl.fromTo("#st{n}", {{ scale: 0.4, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.3, ease: "back.out(2.4)", immediateRender: false }}, {round(t_sg[0] + 0.35 + n * 0.12, 3)});')
for n in range(6):
    js.append(f'tl.fromTo("#gl{n}", {{ x: 40, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.35, ease: "power3.out", immediateRender: false }}, {round(t_sg[0] + 0.5 + n * 0.16, 3)});')
    js.append(f'tl.fromTo("#gl-n{n}", {{ textContent: 0 }}, {{ textContent: {240 + n * 137}, duration: 1.1, ease: "power1.out", snap: {{ textContent: 1 }}, immediateRender: false }}, {round(t_sg[0] + 0.7 + n * 0.16, 3)});')

js.append(f'tl.fromTo("#fx-linha", {{ scaleX: 0, transformOrigin: "0% 50%" }}, {{ scaleX: 1, duration: 1.1, ease: "power2.inOut", immediateRender: false }}, {round(t_fx[0] + 0.25, 3)});')
for n in range(4):
    js.append(f'tl.fromTo("#fx{n}", {{ y: 30, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.38, ease: "power3.out", immediateRender: false }}, {round(t_fx[0] + 0.3 + n * 0.3, 3)});')

TRES = ("Escolheu.", "Pagou.", "Disparou.")
CENAS[4] = CENAS[4].replace('<div class="tres" id="tres"></div>', '<div class="tres">' + "".join(f'<b id="t3-{n}">{p}</b>' for n, p in enumerate(TRES)) + "</div>")
for n, p in enumerate(TRES):
    js.append(f'tl.fromTo("#t3-{n}", {{ y: 40, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.32, ease: "power3.out", immediateRender: false }}, {round(pal(4, p.strip(".")) - 0.08, 3)});')

for n in range(4):
    js.append(f'tl.fromTo("#pr{n}", {{ x: 50, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.35, ease: "power3.out", immediateRender: false }}, {round(t_pr[0] + 0.3 + n * 0.22, 3)});')
    js.append(f'tl.fromTo("#pr-b{n}", {{ width: "0%" }}, {{ width: "var(--w)", duration: 0.6, ease: "power3.out", immediateRender: false }}, {round(t_pr[0] + 0.42 + n * 0.22, 3)});')
js.append(f'tl.fromTo("#pr-nota", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.4, immediateRender: false }}, {round(pal(5, "menor") - 0.15, 3)});')

for n in range(3):
    js.append(f'tl.fromTo("#lk{n}", {{ y: 36, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.38, ease: "power3.out", immediateRender: false }}, {round(t_lk[0] + 0.3 + n * 0.26, 3)});')

js.append(f'tl.fromTo("#fone-bot", {{ y: 70, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.6, ease: "power3.out", immediateRender: false }}, {round(t_bot[0] + 0.15, 3)});')
for n in range(5):
    js.append(f'tl.fromTo("#bt{n}", {{ x: 40, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.3, ease: "power3.out", immediateRender: false }}, {round(t_bot[0] + 0.5 + n * 0.16, 3)});')

js += [f'tl.fromTo("#fc-lock", {{ scale: 0.9, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.7, ease: "power3.out", immediateRender: false }}, {round(t_fc[0] + 0.1, 3)});',
       f'tl.fromTo("#fc-sl", {{ y: 26, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.5, ease: "power3.out", immediateRender: false }}, {round(t_fc[0] + 0.55, 3)});',
       f'tl.fromTo("#fc-ar", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.5, immediateRender: false }}, {round(t_fc[0] + 1.1, 3)});']

# ---------------------------------------------------------------- falas
FALAS = [
    (0, ["Você mandou sua divulgação.", "Pra três grupos.", "E parou por aí."], (), 1180),
    (1, ["A Vetrex Networking existe", "pra isso não acontecer."], ("Vetrex",), 1400),
    (2, ["Sua mensagem sai todo dia,", "no automático, em grupos", "e no status do WhatsApp."], ("automático",), 1330),
    (3, ["Você escreve uma vez.", "O bot cuida do resto."], ("bot",), 1300),
    (5, ["Dez reais o dia.", "E quanto mais dias você pega,", "menor fica o valor."], ("menor",), 1330),
    (6, ["Precisa de público novo?", "Tem venda de link", "de grupo também."], ("link",), 1280),
    (7, ["Tudo dentro do Telegram.", "Num bot só."], ("Telegram",), 1330),
    (8, ["Sem painel complicado.", "Sem instalar nada."], (), 1330),
]
falas_html = []
for i, linhas, pilulas, topo in FALAS:
    el, j = bloco(i, linhas, pilulas, topo=topo)
    falas_html.append("      " + el)
    js += j

# ---------------------------------------------------------------- som
SFX = [("ab", "whoosh", 0.0, 0.57, 0.4), ("marca", "sparkle", t_marca[0], 1.8, 0.5),
       ("tres1", "pop", pal(4, "Escolheu") - 0.09, 0.7, 0.5), ("tres2", "pop", pal(4, "Pagou") - 0.09, 0.7, 0.5),
       ("tres3", "impact-bass-2", pal(4, "Disparou") + 0.1 - 1.95, 2.5, 0.5),
       ("preco", "sparkle", t_pr[0] + 0.3, 1.8, 0.4), ("fecho", "impact-bass-1", t_fc[0] + 0.1 - 0.04, 2.0, 0.55)]
for n, t in enumerate((t_sg[0], t_fx[0], t_lk[0], t_bot[0])):
    SFX.append((f"wh{n}", "whoosh-short", t - 0.14, 0.57, 0.3))
sfx = "\n".join(f'      <audio id="sfx-{i}" class="clip" src="assets/audio/{f}.mp3" data-start="{round(max(0, s), 3)}" data-duration="{d}" data-track-index="{60 + n}" data-volume="{v}"></audio>'
                for n, (i, f, s, d, v) in enumerate(SFX))

CSS = f"""
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html, body {{ width: 1080px; height: 1920px; background: #000; overflow: hidden; }}
#root {{ position: relative; width: 100%; height: 100%; font-family: "Inter", sans-serif; color: #fff; overflow: hidden; }}
#ondas {{ position: absolute; inset: 0; }}
#ondas svg {{ width: 100%; height: 100%; display: block; }}
#brand {{ position: absolute; left: 60px; top: 74px; display: flex; align-items: center; gap: 18px; opacity: 0.92; }}
#brand img.x {{ height: 40px; }} #brand img.w {{ height: 22px; opacity: 0.9; }}
#brand span {{ width: 2px; height: 34px; background: #4a4a55; }}
.cena {{ position: absolute; inset: 0; }}
.palco {{ position: absolute; left: 0; right: 0; top: 300px; padding: 0 70px; }}
.cena.centro .palco {{ top: 0; height: 100%; display: flex; align-items: center; justify-content: center; }}
.fala {{ position: absolute; left: 70px; right: 70px; font-family: "Outfit", "Inter", sans-serif; font-weight: 700; font-size: 86px; line-height: 1.14; letter-spacing: -0.02em; }}
.fala .ln {{ display: block; }}
.pl {{ display: inline-block; }}
.pil {{ background: #fff; color: #000; border-radius: 14px; padding: 0 18px; }}
.card {{ background: #0b0b0e; border: 2px solid #1d1d24; border-radius: 28px; padding: 44px; }}
.kick {{ font-family: "JetBrains Mono", monospace; font-size: 29px; letter-spacing: 0.26em; color: #76767f; margin-bottom: 30px; }}
.chat .ch-l {{ background: #121218; border: 2px solid #22222b; border-radius: 20px; padding: 28px 32px; margin-bottom: 22px; }}
.ch-g {{ display: flex; align-items: baseline; gap: 16px; }}
.ch-g b {{ font-size: 36px; }} .ch-g small {{ font-size: 28px; color: #76767f; }}
.ch-b {{ margin: 16px 0 12px; font-size: 32px; color: #d7d7de; background: #1d2b24; border-radius: 14px; padding: 16px 22px; display: inline-block; }}
.ch-v {{ font-size: 28px; color: #6d6d76; }}
.ch-fim {{ text-align: center; font-size: 34px; color: {ROXO2}; margin-top: 10px; }}
.fone {{ background: #0b0b0e; border: 2px solid #22222b; border-radius: 34px; padding: 34px; }}
.fone-top {{ display: flex; align-items: center; gap: 16px; font-size: 30px; color: #b9b9c2; margin-bottom: 28px; }}
.dot {{ width: 18px; height: 18px; border-radius: 50%; background: #25d366; }} .dot.az {{ background: #2aabee; }}
.st-row {{ display: flex; align-items: center; gap: 22px; margin-bottom: 30px; }}
.st {{ width: 92px; height: 92px; border-radius: 50%; border: 5px solid {ROXO}; display: flex; align-items: center; justify-content: center; }}
.st span {{ width: 70px; height: 70px; border-radius: 50%; background: #1b1b22; display: block; }}
.st-lb {{ font-family: "JetBrains Mono", monospace; font-size: 28px; letter-spacing: 0.2em; color: #76767f; }}
.gl {{ display: flex; align-items: center; gap: 20px; padding: 20px 0; border-top: 2px solid #1b1b22; }}
.gl-p {{ width: 56px; height: 56px; border-radius: 16px; background: #23232c; }}
.gl b {{ flex: 1; font-size: 32px; font-weight: 600; }}
.gl i {{ font-style: normal; font-family: "JetBrains Mono", monospace; font-size: 30px; color: {ROXO2}; }}
.fluxo {{ position: relative; display: grid; grid-template-columns: repeat(2, 1fr); gap: 28px; }}
.fx-linha {{ position: absolute; left: 10%; right: 10%; top: 50%; height: 3px; background: linear-gradient(90deg, {ROXO}, {ROXO2}); opacity: 0.5; }}
.fx {{ background: #0e0e13; border: 2px solid #22222b; border-radius: 24px; padding: 34px; }}
.fx-ic {{ font-size: 54px; margin-bottom: 14px; }}
.fx b {{ display: block; font-size: 38px; margin-bottom: 8px; }}
.fx small {{ font-size: 29px; color: #83838d; }}
.tres {{ text-align: center; }}
.tres b {{ display: block; font-family: "Outfit", "Inter", sans-serif; font-size: 132px; font-weight: 700; letter-spacing: -0.03em; line-height: 1.1; }}
.precos .pr {{ margin-bottom: 30px; }}
.pr-top {{ display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 14px; }}
.pr-top b {{ font-size: 44px; }} .pr-top span {{ font-size: 30px; color: #8c8c96; }}
.pr-trilho {{ height: 20px; background: #1b1b22; border-radius: 10px; overflow: hidden; }}
.pr-trilho i {{ display: block; height: 100%; border-radius: 10px; background: linear-gradient(90deg, {ROXO}, {ROXO2}); }}
.pr-nota {{ text-align: center; font-size: 32px; color: {ROXO2}; margin-top: 14px; }}
.grade {{ display: grid; gap: 26px; }}
.lk {{ display: flex; align-items: center; gap: 26px; background: #0e0e13; border: 2px solid #22222b; border-radius: 24px; padding: 34px; }}
.lk-ic {{ font-size: 50px; }} .lk b {{ display: block; font-size: 40px; }} .lk small {{ font-size: 28px; color: #83838d; }}
.bt-msg {{ background: #15151c; border-radius: 20px; padding: 26px 30px; font-size: 32px; color: #d4d4db; margin-bottom: 26px; }}
.bt-b {{ background: #16161d; border: 2px solid #2a2a34; border-radius: 18px; padding: 26px 30px; font-size: 34px; margin-bottom: 18px; }}
.lock {{ display: flex; align-items: center; justify-content: center; gap: 30px; }}
.lock img {{ height: 110px; }} .lock img.wm {{ height: 78px; }}
.lock .bar {{ width: 3px; height: 96px; background: #55555f; }}
.lock.big img {{ height: 150px; }} .lock.big img.wm {{ height: 104px; }} .lock.big .bar {{ height: 130px; }}
.fecho-in {{ text-align: center; }}
.fc-sl {{ max-width: 760px; margin: 56px auto 0; font-family: "Outfit", "Inter", sans-serif; font-size: 52px; font-weight: 600; line-height: 1.3; }}
.fc-sl .pil {{ padding: 0 14px; }}
.fc-ar {{ margin-top: 34px; font-family: "JetBrains Mono", monospace; font-size: 34px; color: #8c8c96; letter-spacing: 0.08em; }}
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
      <div id="ondas" class="clip" data-start="0" data-duration="{FIM}" data-track-index="0" data-layout-ignore>{ONDAS}</div>
      <div id="brand" class="clip" data-start="0" data-duration="{round(t_fc[0], 3)}" data-track-index="1" data-layout-ignore>
        <img class="x" src="assets/img/marca-x.png" alt="" /><span></span><img class="w" src="assets/img/wordmark-sm.png" alt="" />
      </div>
{chr(10).join(CENAS)}
{chr(10).join(falas_html)}
      <audio id="trilha" class="clip" src="assets/audio/trilha.mp3" data-start="0" data-duration="{FIM}" data-track-index="49" data-volume="0.5"></audio>
      <audio id="narracao" class="clip" src="assets/audio/narracao.mp3" data-start="0" data-duration="{T["total"]:.2f}" data-track-index="50" data-volume="1"></audio>
{sfx}
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{ paused: true }});
      tl.fromTo("#onda-a", {{ y: 0, x: 0 }}, {{ y: -120, x: 18, duration: {FIM}, ease: "none" }}, 0);
      tl.fromTo("#onda-b", {{ y: 0, x: 0 }}, {{ y: 90, x: -22, duration: {FIM}, ease: "none" }}, 0);
{chr(10).join("      " + x for x in js)}
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
'''
open("index.html", "w").write(page)
print("ok", len(CENAS), "cenas ·", FIM, "s")
