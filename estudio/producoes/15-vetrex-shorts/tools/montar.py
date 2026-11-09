"""Gera index.html versão vertical (9:16) do painel Vetrex pra Shorts/Reels/Stories.

UI em cima, legenda embaixo. Mesmo estilo (fundo preto, ondas roxas, cards de interface).
Uso: python3 tools/narracao_google.py && python3 tools/montar.py
"""
import json
import unicodedata

T = json.load(open("build/timing.json"))
F = T["frases"]
FIM = round(T["total"] + 2.0, 2)

W, H = 1080, 1920
ROXO, ROXO2 = "#7c3aed", "#c084fc"
VERDE, VERM = "#25d366", "#e2574c"
PILULA = {"vetrex", "antilink", "antipay", "antiflood", "advertencia", "sozinho", "automatico"}

js, CENAS, SFX = [], [], []


def norm(w):
    w = unicodedata.normalize("NFD", w.lower())
    return "".join(c for c in w if c.isalnum() and not unicodedata.combining(c))


def ini(i):
    return F[i]["ini"]


def pal(i, palavra, n=0):
    achadas = [p["ini"] for p in F[i]["palavras"] if norm(p["p"]).startswith(norm(palavra))]
    return achadas[n] if achadas else F[i]["ini"]


# ---------------------------------------------------------------- legendas
def legendas(sem=()):
    blocos = []
    for i, f in enumerate(F):
        if i in sem:
            continue
        grupo = []
        for w in f["palavras"]:
            grupo.append(w)
            if len(grupo) == 3 or (w["p"].endswith((".", ",", ":", "?", "!", "…")) and len(grupo) >= 2):
                blocos.append(grupo)
                grupo = []
        if grupo:
            blocos.append(grupo)
    els = []
    for n, grupo in enumerate(blocos):
        t0 = round(grupo[0]["ini"] - 0.08, 3)
        prox = blocos[n + 1][0]["ini"] - 0.08 if n + 1 < len(blocos) else grupo[-1]["fim"] + 0.5
        t1 = round(min(prox, grupo[-1]["fim"] + 0.7), 3)
        d = round(max(t1 - t0, 0.3), 3)
        texto = " ".join(f'<span class="{"pil" if norm(w["p"]) in PILULA else ""}">{w["p"]}</span>' for w in grupo)
        cid = f"cap{n}"
        els.append(f'        <div id="{cid}" class="clip cap" data-start="{t0}" data-duration="{d}" data-track-index="{n}"><div id="{cid}-in" class="cap-in">{texto}</div></div>')
        js.append(f'tl.fromTo("#{cid}-in", {{ y: 48, scale: 0.9, opacity: 0 }}, {{ y: 0, scale: 1, opacity: 1, duration: 0.22, ease: "back.out(2.2)", immediateRender: false }}, {round(t0 + 0.02, 3)});')
        js.append(f'tl.to("#{cid}-in", {{ y: -24, opacity: 0, duration: 0.09, ease: "power2.in", immediateRender: false }}, {round(t0 + d - 0.09, 3)});')
    return els


# ---------------------------------------------------------------- telas
def zap(linhas, topo="Grupo · 182 membros", cid="z"):
    return f'''<div class="zap">
  <div class="zap-top"><span class="dot"></span>{topo}</div>
  <div class="zap-corpo">{linhas}</div>
</div>'''


def m(txt, quem="", mid="", classe=""):
    i = f' id="{mid}"' if mid else ""
    autor = f'<b>{quem}</b>' if quem else ""
    return f'<div{i} class="m {classe}">{autor}{txt}</div>'


def caos():
    linhas = "".join(m(t, q, mid=f"ca{n}") for n, (q, t) in enumerate((
        ("+55 11 9 ****-4280", "🔥 PROMOÇÃO entra vip.link/x"),
        ("+55 62 9 ****-0631", "pix 000.111.222-33 manda 50"),
        ("+81 80 ****-0800", "aaaa aaaa aaaa"),
        ("+55 79 9 ****-5724", "bando de otário"))))
    return zap(linhas, "Grupo · 02:14")


def bloqueio(topo, msg_, selo, cor, cid):
    return f'''{zap(m(msg_[1], msg_[0], mid=f"{cid}-m"), topo)}
<div class="selo-bot" id="{cid}-selo" style="--c: {cor}">{selo}</div>'''


def antilink():
    return bloqueio("Grupo · antilink ligado",
                    ("+55 11 9 ****-4280", "entra vip.link/x"),
                    "🛡️ link apagado", VERDE, "al")


def antipay():
    return bloqueio("Grupo · antipay ligado",
                    ("+55 62 9 ****-0631", "pix 000.111.222-33"),
                    "🛡️ cobrança barrada", VERDE, "ap")


def antiflood():
    linhas = "".join(m("aaaa aaaa", "+81 80 ****-0800", mid=f"af-m{n}") for n in range(4))
    return f'''{zap(linhas, "Grupo · antiflood ligado")}
<div class="selo-bot" id="af-selo" style="--c: {VERDE}">🛡️ flood contido</div>'''


def warns():
    passos = (("1ª advertência", "aviso", "#f0b429"), ("2ª advertência", "último aviso", "#f08a29"), ("3ª advertência", "removido do grupo", VERM))
    return f'''<div class="cartao">
  <div class="kick">!WARN</div>
  {"".join(f'<div class="wr" id="wr{n}" style="--c: {c}"><b>{t}</b><small>{s}</small></div>' for n, (t, s, c) in enumerate(passos))}
</div>'''


def arquivar():
    return f'''<div class="cartao perigo">
  <div class="kick" style="color:#f0b429">!NUKE · LIMPAR E ARQUIVAR</div>
  <div class="nk" id="nk0">1 · <b>!nuke Nome novo</b></div>
  <div class="nk" id="nk1">2 · <b>!nuke confirmar</b></div>
  <div class="aviso" id="nk-av">⚠️ irreversível · expira em 60 s</div>
</div>'''


def lock(cid, grande=False):
    return (f'<div class="lock{" big" if grande else ""}" id="{cid}">'
            f'<img class="x" src="assets/img/marca-x.png" alt="" /><span class="bar"></span>'
            f'<img class="wm" src="assets/img/wordmark-sm.png" alt="" /></div>')


def fecho():
    return f'''<div class="fecho-in">
  {lock("fc-lock", True)}
  <div class="fc-sl" id="fc-sl">O seu grupo no <span class="pil">automático</span>.</div>
  <div class="fc-ar" id="fc-ar">t.me/vetrexzapbot</div>
</div>'''


# ---------------------------------------------------------------- cenas
def cena(cid, conteudo, t0, t1, centro=False, zoom=1):
    n = len(CENAS)
    t0, t1 = round(t0, 3), round(t1, 3)
    d = round(t1 - t0, 3)
    CENAS.append(f'      <div id="{cid}" class="clip cena{" centro" if centro else ""}" data-start="{t0}" data-duration="{d}" '
                 f'data-track-index="{40 + n}" data-track-kind="graphics"><div class="palco" id="{cid}-p">{conteudo}</div></div>')
    a, b = (1.0, 1.06) if zoom > 0 else (1.06, 1.0)
    js.append(f'tl.fromTo("#{cid}-p", {{ y: 40, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.3, ease: "power3.out", immediateRender: false }}, {t0});')
    js.append(f'tl.fromTo("#{cid}-p", {{ scale: {a} }}, {{ scale: {b}, duration: {d}, ease: "none", immediateRender: false }}, {t0});')
    js.append(f'tl.fromTo("#sweep", {{ x: -1300 }}, {{ x: 1300, duration: 0.35, ease: "power2.inOut", immediateRender: false }}, {round(t0 - 0.14, 3)});')
    js.append(f'tl.fromTo("#sweep", {{ opacity: 0.85 }}, {{ opacity: 0, duration: 0.12, immediateRender: false }}, {round(t0 + 0.14, 3)});')
    SFX.append((f"wh{n}", "whoosh-cinematic", t0 - 0.18, 1.0, 0.45))
    SFX.append((f"im{n}", "impact-bass-1", t0 - 0.04, 2.115, 0.6))


T_MARCA = ini(2)
T_LINK = ini(3)
T_PAY = pal(3, "Antipay")
T_FLOOD = pal(3, "Antiflood")
T_WARN = ini(4)
T_NUKE = ini(5)
T_FECHO = ini(6)

cena("c1", caos(), 0.0, T_MARCA - 0.1)
cena("c2", lock("m-lock", True), T_MARCA - 0.1, T_LINK - 0.1, zoom=-1)
cena("c3", antilink(), T_LINK - 0.1, T_PAY - 0.1)
cena("c4", antipay(), T_PAY - 0.1, T_FLOOD - 0.1, zoom=-1)
cena("c5", antiflood(), T_FLOOD - 0.1, T_WARN - 0.1)
cena("c6", warns(), T_WARN - 0.1, T_NUKE - 0.1, zoom=-1)
cena("c7", arquivar(), T_NUKE - 0.1, T_FECHO - 0.25)
cena("c8", fecho(), T_FECHO - 0.25, FIM, centro=True)

# ---------------------------------------------------------------- animações
for n in range(4):
    t = 0.2 + n * 0.3
    js.append(f'tl.fromTo("#ca{n}", {{ x: -30, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.28, ease: "power3.out", immediateRender: false }}, {round(t, 3)});')
    SFX.append((f"ck{n}", "pop", t, 0.72, 0.3))

js.append(f'tl.fromTo("#m-lock", {{ scale: 0.86, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.45, ease: "back.out(1.7)", immediateRender: false }}, {round(T_MARCA - 0.02, 3)});')
js.append(f'tl.fromTo("#m-lock .wm", {{ clipPath: "inset(0 100% 0 0)" }}, {{ clipPath: "inset(0 0% 0 0)", duration: 0.4, ease: "power2.out", immediateRender: false }}, {round(T_MARCA + 0.2, 3)});')
SFX.append(("gl", "glitch-1", T_MARCA - 0.1, 2.638, 0.4))

for cid, t0, t_selo in (("al", T_LINK + 0.15, T_PAY - 0.4), ("ap", T_PAY + 0.15, T_FLOOD - 0.4)):
    js.append(f'tl.fromTo("#{cid}-m", {{ x: -30, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.25, ease: "power3.out", immediateRender: false }}, {round(t0, 3)});')
    js.append(f'tl.to("#{cid}-m", {{ opacity: 0, x: 40, duration: 0.2, ease: "power2.in", immediateRender: false }}, {round(t_selo - 0.1, 3)});')
    js.append(f'tl.fromTo("#{cid}-selo", {{ y: 22, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.25, ease: "back.out(2)", immediateRender: false }}, {round(t_selo, 3)});')
    SFX.append((f"{cid}s", "ping", t_selo, 1.32, 0.45))

for n in range(4):
    t = T_FLOOD + 0.2 + n * 0.1
    js.append(f'tl.fromTo("#af-m{n}", {{ x: -24, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.18, ease: "power3.out", immediateRender: false }}, {round(t, 3)});')
    SFX.append((f"afp{n}", "key-press", t, 0.432, 0.25))
t_afs = T_WARN - 0.35
js.append(f'tl.to("#af-m0, #af-m1, #af-m2, #af-m3", {{ opacity: 0.25, duration: 0.18, immediateRender: false }}, {round(t_afs - 0.1, 3)});')
js.append(f'tl.fromTo("#af-selo", {{ y: 22, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.25, ease: "back.out(2)", immediateRender: false }}, {round(t_afs, 3)});')
SFX.append(("afs", "ping", t_afs, 1.32, 0.45))

for n in range(3):
    t = T_WARN + 0.15 + n * 0.4
    js.append(f'tl.fromTo("#wr{n}", {{ x: 40, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.28, ease: "power3.out", immediateRender: false }}, {round(t, 3)});')
    SFX.append((f"wrp{n}", "pop" if n < 2 else "impact-bass-2", t if n < 2 else t - 0.06, 0.72 if n < 2 else 2.592, 0.5))

for n in range(2):
    t = T_NUKE + 0.2 + n * 0.5
    js.append(f'tl.fromTo("#nk{n}", {{ x: 38, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.26, ease: "power3.out", immediateRender: false }}, {round(t, 3)});')
    SFX.append((f"nkp{n}", "click", t, 0.365, 0.4))
js.append(f'tl.fromTo("#nk-av", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3, immediateRender: false }}, {round(T_NUKE + 1.3, 3)});')

js += [f'tl.fromTo("#fc-lock", {{ scale: 0.88, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.55, ease: "back.out(1.6)", immediateRender: false }}, {round(T_FECHO - 0.1, 3)});',
       f'tl.fromTo("#fc-sl", {{ y: 26, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.4, ease: "power3.out", immediateRender: false }}, {round(T_FECHO + 0.35, 3)});',
       f'tl.fromTo("#fc-ar", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.4, immediateRender: false }}, {round(T_FECHO + 0.9, 3)});']
SFX.append(("fcch", "chime", T_FECHO + 0.7, 2.544, 0.4))

cap_els = legendas()
sfx = "\n".join(f'      <audio id="sfx-{i}" class="clip" src="assets/audio/{f}.mp3" data-start="{round(max(0, s), 3)}" data-duration="{d}" data-track-index="{90 + n}" data-volume="{v}"></audio>'
                for n, (i, f, s, d, v) in enumerate(SFX))

CSS = f"""
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html, body {{ width: {W}px; height: {H}px; background: #000; overflow: hidden; }}
#root {{ position: relative; width: 100%; height: 100%; font-family: "Inter", sans-serif; color: #fff; overflow: hidden; }}
#ondas {{ position: absolute; inset: 0; }} #ondas svg {{ width: 100%; height: 100%; display: block; }}
#sweep {{ position: absolute; left: 50%; top: 0; width: 460px; height: 100%; margin-left: -230px; opacity: 0;
  background: linear-gradient(90deg, rgba(124,58,237,0) 0%, rgba(192,132,252,0.45) 50%, rgba(124,58,237,0) 100%); }}
#brand {{ position: absolute; left: 60px; top: 70px; display: flex; align-items: center; gap: 16px; opacity: 0.9; }}
#brand img.x {{ height: 36px; }} #brand img.w {{ height: 24px; }}
#brand span {{ width: 2px; height: 30px; background: #4a4a55; }}
.cena {{ position: absolute; left: 0; right: 0; top: 230px; height: 1100px; }}
.palco {{ position: absolute; inset: 0; padding: 0 70px; display: flex; flex-direction: column; justify-content: center; }}
.cena.centro .palco {{ align-items: center; }}
#c2-p {{ align-items: center; }}
.cap {{ position: absolute; left: 70px; right: 70px; top: 1440px; height: 350px; display: flex; align-items: flex-start; justify-content: center; }}
.cap-in {{ font-family: "Outfit", "Inter", sans-serif; font-weight: 700; font-size: 108px; line-height: 1.1; letter-spacing: -0.02em; text-align: center; }}
.cap-in span {{ display: inline-block; }}
.pil {{ background: #fff; color: #000; border-radius: 16px; padding: 0 20px; }}
.zap {{ background: #0b0b0e; border: 2px solid #22222b; border-radius: 28px; padding: 32px 34px; }}
.zap-top {{ display: flex; align-items: center; gap: 16px; font-size: 32px; color: #b9b9c2; margin-bottom: 24px; }}
.dot {{ width: 18px; height: 18px; border-radius: 50%; background: {VERDE}; }}
.m {{ background: #15151c; border-radius: 18px; padding: 20px 24px; margin-bottom: 18px; font-size: 32px; color: #dcdce3; }}
.m:last-child {{ margin-bottom: 0; }}
.m b {{ display: block; font-size: 28px; color: #8e8e98; margin-bottom: 8px; font-weight: 600; }}
.selo-bot {{ margin-top: 24px; align-self: flex-start; background: #10151a; border: 2px solid var(--c); color: var(--c);
  border-radius: 16px; padding: 16px 26px; font-size: 34px; font-weight: 600; }}
.cartao {{ background: #0b0b0e; border: 2px solid #22222b; border-radius: 28px; padding: 40px; }}
.cartao.perigo {{ border-color: #4a3a12; }}
.kick {{ font-family: "JetBrains Mono", monospace; font-size: 29px; letter-spacing: 0.2em; color: #76767f; margin-bottom: 26px; }}
.wr {{ border-left: 8px solid var(--c); background: #11111a; border-radius: 14px; padding: 22px 28px; margin-bottom: 18px; }}
.wr:last-child {{ margin-bottom: 0; }}
.wr b {{ display: block; font-size: 42px; }} .wr small {{ font-size: 31px; color: #8c8c96; }}
.nk {{ background: #11111a; border: 2px solid #22222b; border-radius: 18px; padding: 24px 28px; margin-bottom: 18px; font-size: 36px; color: #c9c9d2; }}
.nk b {{ font-family: "JetBrains Mono", monospace; color: #ffd23a; }}
.aviso {{ margin-top: 20px; font-size: 32px; color: #f0b429; }}
.lock {{ display: flex; align-items: center; justify-content: center; gap: 28px; }}
.lock img.x {{ height: 100px; }} .lock img.wm {{ height: 76px; }}
.lock .bar {{ width: 3px; height: 86px; background: #55555f; }}
.lock.big img.x {{ height: 150px; }} .lock.big img.wm {{ height: 114px; }} .lock.big .bar {{ width: 4px; height: 132px; }}
.fecho-in {{ text-align: center; }}
.fc-sl {{ max-width: 820px; margin: 48px auto 0; font-family: "Outfit", "Inter", sans-serif; font-size: 56px; font-weight: 600; line-height: 1.25; }}
.fc-sl .pil {{ padding: 0 14px; }}
.fc-ar {{ margin-top: 32px; font-family: "JetBrains Mono", monospace; font-size: 36px; color: #8c8c96; letter-spacing: 0.08em; }}
"""

ONDAS = f'''<svg viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid slice">
<defs><linearGradient id="g1" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="{ROXO}" stop-opacity="0"/><stop offset="0.45" stop-color="{ROXO2}" stop-opacity="0.7"/><stop offset="1" stop-color="{ROXO}" stop-opacity="0"/></linearGradient>
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
</g>
</svg>'''

page = f'''<!doctype html>
<html lang="pt-BR">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={W}, height={H}" />
    <script src="assets/lib/gsap.min.js"></script>
    <style>{CSS}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{FIM}" data-width="{W}" data-height="{H}">
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
      tl.fromTo("#onda-a", {{ y: 0, x: 0 }}, {{ y: -130, x: 20, duration: {FIM}, ease: "none" }}, 0);
      tl.fromTo("#onda-b", {{ y: 0, x: 0 }}, {{ y: 100, x: -22, duration: {FIM}, ease: "none" }}, 0);
      tl.set("#sweep", {{ opacity: 0 }}, 0);
{chr(10).join("      " + x for x in js)}
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
'''
open("index.html", "w").write(page)
print("ok", len(CENAS), "cenas ·", len(cap_els), "legendas ·", len(SFX), "sfx ·", FIM, "s")
