"""Gera index.html do vídeo do painel de moderação da Vetrex (YouTube, 1920x1080).

Mesmo estilo do institucional (fundo preto, ondas roxas, cards de interface, legendas curtas),
só que deitado: legenda na coluna da esquerda, interface na direita.
Uso: python3 tools/narracao_google.py && python3 tools/montar.py
"""
import json
import unicodedata

T = json.load(open("build/timing.json"))
F = T["frases"]
FIM = round(T["total"] + 2.8, 2)

W, H = 1920, 1080
ROXO, ROXO2 = "#7c3aed", "#c084fc"
VERDE, VERM = "#25d366", "#e2574c"
PILULA = {"vetrex", "antilink", "antipay", "antiflood", "advertencia", "admin", "automatico", "sozinho", "confirmacao"}

js, CENAS, SFX = [], [], []


def norm(w):
    w = unicodedata.normalize("NFD", w.lower())
    return "".join(c for c in w if c.isalnum() and not unicodedata.combining(c))


def ini(i):
    return F[i]["ini"]


def pal(i, palavra, n=0):
    achadas = [p["ini"] for p in F[i]["palavras"] if norm(p["p"]).startswith(norm(palavra))]
    return achadas[n] if achadas else F[i]["ini"]


# ---------------------------------------------------------------- legendas (coluna da esquerda)
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
        prox = blocos[n + 1][0]["ini"] - 0.08 if n + 1 < len(blocos) else grupo[-1]["fim"] + 0.6
        t1 = round(min(prox, grupo[-1]["fim"] + 0.9), 3)
        d = round(max(t1 - t0, 0.3), 3)
        texto = " ".join(f'<span class="{"pil" if norm(w["p"]) in PILULA else ""}">{w["p"]}</span>' for w in grupo)
        cid = f"cap{n}"
        els.append(f'        <div id="{cid}" class="clip cap" data-start="{t0}" data-duration="{d}" data-track-index="{n}"><div id="{cid}-in" class="cap-in">{texto}</div></div>')
        js.append(f'tl.fromTo("#{cid}-in", {{ y: 44, scale: 0.92, opacity: 0 }}, {{ y: 0, scale: 1, opacity: 1, duration: 0.22, ease: "back.out(2.2)", immediateRender: false }}, {round(t0 + 0.02, 3)});')
        js.append(f'tl.to("#{cid}-in", {{ y: -22, opacity: 0, duration: 0.09, ease: "power2.in", immediateRender: false }}, {round(t0 + d - 0.09, 3)});')
    return els


# ---------------------------------------------------------------- telas
def zap(linhas, topo="Grupo · 182 membros", cid="z"):
    return f'''<div class="zap">
  <div class="zap-top"><span class="dot"></span>{topo}</div>
  <div class="zap-corpo">{linhas}</div>
</div>'''


def msg(txt, quem="", eu=False, mid="", classe=""):
    i = f' id="{mid}"' if mid else ""
    autor = f'<b>{quem}</b>' if quem else ""
    return f'<div{i} class="m {"eu" if eu else ""} {classe}">{autor}{txt}</div>'


def caos():
    linhas = "".join(msg(t, q, mid=f"ca{n}") for n, (q, t) in enumerate((
        ("+55 11 9 ****-4280", "🔥 PROMOÇÃO entra no grupo vip.link/x"),
        ("+55 62 9 ****-0631", "chave pix 000.111.222-33 manda 50"),
        ("+81 80 ****-0800", "aaaa aaaa aaaa aaaa aaaa"),
        ("+55 79 9 ****-5724", "ô bando de otário"))))
    return zap(linhas, "Grupo · 182 membros · 02:14")


def bloqueio(titulo, msgs, selo, cor, cid):
    linhas = "".join(msg(t, q, mid=f"{cid}-m{n}") for n, (q, t) in enumerate(msgs))
    return f'''{zap(linhas, titulo)}
<div class="selo-bot" id="{cid}-selo" style="--c: {cor}">{selo}</div>'''


def antilink():
    return bloqueio("Grupo · antilink ligado", [("+55 11 9 ****-4280", "entra no meu grupo vip.link/x")],
                    "🛡️ link apagado · aviso enviado", VERDE, "al")


def antipay():
    return bloqueio("Grupo · antipay ligado", [("+55 62 9 ****-0631", "pix 000.111.222-33, manda 50 que eu envio")],
                    "🛡️ cobrança barrada", VERDE, "ap")


def antiflood():
    linhas = "".join(msg("aaaa aaaa", "+81 80 ****-0800", mid=f"af-m{n}") for n in range(5))
    return f'''{zap(linhas, "Grupo · antiflood ligado")}
<div class="selo-bot" id="af-selo" style="--c: {VERDE}">🛡️ flood contido · silenciado 10 min</div>'''


def modoforte():
    itens = ("antilink", "antipay", "antiflood", "antiinvisível")
    return f'''<div class="cartao">
  <div class="kick">!MODOFORTE</div>
  {"".join(f'<div class="sw" id="sw{n}"><span>{t}</span><i class="led"></i></div>' for n, t in enumerate(itens))}
</div>'''


def warns():
    passos = (("1ª advertência", "aviso no grupo", "#f0b429"), ("2ª advertência", "último aviso", "#f08a29"), ("3ª advertência", "removido do grupo", VERM))
    return f'''<div class="cartao">
  <div class="kick">!WARN</div>
  {"".join(f'<div class="wr" id="wr{n}" style="--c: {c}"><b>{t}</b><small>{s}</small></div>' for n, (t, s, c) in enumerate(passos))}
</div>'''


def comandos():
    cmds = (("!ban", "remove do grupo"), ("!mute", "fecha o grupo"), ("!promote", "dá admin"), ("!del", "apaga a mensagem"))
    return f'<div class="grade2">{"".join(f'<div class="cmd" id="cd{n}"><b>{c}</b><small>{d}</small></div>' for n, (c, d) in enumerate(cmds))}</div>'


def boasvindas():
    return f'''{zap(msg("Bem-vindo, <u>{user}</u>! Você está em <u>{group}</u>. Leia as regras no assunto 👊", "Vetrex", mid="bv-m", classe="bot"), "Grupo · alguém entrou")}
<div class="selo-bot" id="bv-selo" style="--c: {ROXO2}">!welcome set &lt;texto&gt;</div>'''


def arquivar():
    return f'''<div class="cartao perigo">
  <div class="kick" style="color:#f0b429">!NUKE · LIMPAR E ARQUIVAR O SEU GRUPO</div>
  <div class="nk" id="nk0">1 · <b>!nuke Nome novo</b><small>prepara a limpeza</small></div>
  <div class="nk" id="nk1">2 · <b>!nuke confirmar</b><small>só você, só admin</small></div>
  <div class="nk" id="nk2">✖ <b>!nuke recusar</b><small>cancela</small></div>
  <div class="aviso" id="nk-av">⚠️ irreversível · a confirmação expira em 60 s</div>
</div>'''


def painel():
    return f'''<div class="cartao">
  <div class="kick">PREFIXO !</div>
  <div class="pf" id="pf0"><b>!protecao</b><small>vê o que está ligado</small></div>
  <div class="pf" id="pf1"><b>!on</b> / <b>!off</b><small>liga e pausa o bot</small></div>
  <div class="pf" id="pf2"><b>só admin</b><small>o bot ignora o resto</small></div>
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
    a, b = (1.0, 1.05) if zoom > 0 else (1.05, 1.0)
    js.append(f'tl.fromTo("#{cid}-p", {{ y: 38, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.34, ease: "power3.out", immediateRender: false }}, {t0});')
    js.append(f'tl.fromTo("#{cid}-p", {{ scale: {a} }}, {{ scale: {b}, duration: {d}, ease: "none", immediateRender: false }}, {t0});')
    js.append(f'tl.fromTo("#sweep", {{ x: -2200 }}, {{ x: 2200, duration: 0.4, ease: "power2.inOut", immediateRender: false }}, {round(t0 - 0.16, 3)});')
    js.append(f'tl.fromTo("#sweep", {{ opacity: 0.8 }}, {{ opacity: 0, duration: 0.12, immediateRender: false }}, {round(t0 + 0.16, 3)});')
    SFX.append((f"wh{n}", "whoosh-cinematic", t0 - 0.2, 1.0, 0.4))
    SFX.append((f"im{n}", "impact-bass-1", t0 - 0.04, 2.115, 0.55))


T_MARCA = ini(2)
T_LINK = ini(3)
T_PAY = ini(4)
T_FLOOD = ini(5)
T_FORTE = ini(6)
T_WARN = ini(7)
T_CMD = ini(8)
T_BV = ini(9)
T_ARQ = ini(10)
T_PREF = ini(11)
T_FECHO = ini(12)

cena("c1", caos(), 0.0, T_MARCA - 0.12)
cena("c2", lock("m-lock", True), T_MARCA - 0.12, T_LINK - 0.12, zoom=-1)
cena("c3", antilink(), T_LINK - 0.12, T_PAY - 0.12)
cena("c4", antipay(), T_PAY - 0.12, T_FLOOD - 0.12, zoom=-1)
cena("c5", antiflood(), T_FLOOD - 0.12, T_FORTE - 0.12)
cena("c6", modoforte(), T_FORTE - 0.12, T_WARN - 0.12, zoom=-1)
cena("c7", warns(), T_WARN - 0.12, T_CMD - 0.12)
cena("c8", comandos(), T_CMD - 0.12, T_BV - 0.12, zoom=-1)
cena("c9", boasvindas(), T_BV - 0.12, T_ARQ - 0.12)
cena("c10", arquivar(), T_ARQ - 0.12, T_PREF - 0.12, zoom=-1)
cena("c11", painel(), T_PREF - 0.12, T_FECHO - 0.25)
cena("c12", fecho(), T_FECHO - 0.25, FIM, centro=True)

# ---------------------------------------------------------------- animações
for n in range(4):
    t = 0.25 + n * 0.3
    js.append(f'tl.fromTo("#ca{n}", {{ x: -40, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.3, ease: "power3.out", immediateRender: false }}, {round(t, 3)});')
    SFX.append((f"ck{n}", "pop", t, 0.72, 0.3))

js.append(f'tl.fromTo("#m-lock", {{ scale: 0.84, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.5, ease: "back.out(1.7)", immediateRender: false }}, {round(T_MARCA - 0.02, 3)});')
js.append(f'tl.fromTo("#m-lock .wm", {{ clipPath: "inset(0 100% 0 0)" }}, {{ clipPath: "inset(0 0% 0 0)", duration: 0.45, ease: "power2.out", immediateRender: false }}, {round(T_MARCA + 0.24, 3)});')
SFX.append(("gl", "glitch-1", T_MARCA - 0.12, 2.638, 0.35))
SFX.append(("spk", "sparkle", T_MARCA + 0.2, 1.802, 0.45))

for cid, t_msg, t_selo in (("al", T_LINK + 0.2, pal(3, "some")), ("ap", T_PAY + 0.2, pal(4, "barrado"))):
    js.append(f'tl.fromTo("#{cid}-m0", {{ x: -40, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.3, ease: "power3.out", immediateRender: false }}, {round(t_msg, 3)});')
    js.append(f'tl.to("#{cid}-m0", {{ opacity: 0, x: 60, duration: 0.3, ease: "power2.in", immediateRender: false }}, {round(t_selo - 0.1, 3)});')
    js.append(f'tl.fromTo("#{cid}-selo", {{ y: 26, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.3, ease: "back.out(2)", immediateRender: false }}, {round(t_selo + 0.12, 3)});')
    SFX.append((f"{cid}s", "ping", t_selo + 0.12, 1.32, 0.45))

for n in range(5):
    t = T_FLOOD + 0.2 + n * 0.1
    js.append(f'tl.fromTo("#af-m{n}", {{ x: -30, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.2, ease: "power3.out", immediateRender: false }}, {round(t, 3)});')
    SFX.append((f"afp{n}", "key-press", t, 0.432, 0.25))
t_af = pal(5, "para")
js.append(f'tl.to("#af-m0, #af-m1, #af-m2, #af-m3, #af-m4", {{ opacity: 0.25, duration: 0.2, immediateRender: false }}, {round(t_af - 0.1, 3)});')
js.append(f'tl.fromTo("#af-selo", {{ y: 26, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.3, ease: "back.out(2)", immediateRender: false }}, {round(t_af + 0.1, 3)});')
SFX.append(("afs", "ping", t_af + 0.1, 1.32, 0.45))

for n in range(4):
    t = T_FORTE + 0.2 + n * 0.16
    js.append(f'tl.fromTo("#sw{n}", {{ x: 40, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.26, ease: "power3.out", immediateRender: false }}, {round(t, 3)});')
    js.append(f'tl.fromTo("#sw{n} .led", {{ background: "#2a2a34" }}, {{ background: "{VERDE}", duration: 0.2, immediateRender: false }}, {round(t + 0.18, 3)});')
    SFX.append((f"swp{n}", "click", t + 0.18, 0.365, 0.4))

for n in range(3):
    t = T_WARN + 0.25 + n * 0.55
    js.append(f'tl.fromTo("#wr{n}", {{ x: 50, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.3, ease: "power3.out", immediateRender: false }}, {round(t, 3)});')
    SFX.append((f"wrp{n}", "pop" if n < 2 else "impact-bass-2", t if n < 2 else t - 0.06, 0.72 if n < 2 else 2.592, 0.45))

for n in range(4):
    t = T_CMD + 0.2 + n * 0.22
    js.append(f'tl.fromTo("#cd{n}", {{ y: 34, scale: 0.94, opacity: 0 }}, {{ y: 0, scale: 1, opacity: 1, duration: 0.28, ease: "back.out(2)", immediateRender: false }}, {round(t, 3)});')
    SFX.append((f"cdp{n}", "pop", t, 0.72, 0.3))

js.append(f'tl.fromTo("#bv-m", {{ y: 30, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.35, ease: "power3.out", immediateRender: false }}, {round(T_BV + 0.2, 3)});')
js.append(f'tl.fromTo("#bv-selo", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3, immediateRender: false }}, {round(T_BV + 0.8, 3)});')
SFX.append(("bvp", "chime", T_BV + 0.2, 2.544, 0.35))

for n in range(3):
    t = T_ARQ + 0.25 + n * 0.5
    js.append(f'tl.fromTo("#nk{n}", {{ x: 46, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.28, ease: "power3.out", immediateRender: false }}, {round(t, 3)});')
    SFX.append((f"nkp{n}", "click", t, 0.365, 0.4))
js.append(f'tl.fromTo("#nk-av", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3, immediateRender: false }}, {round(pal(10, "confirmação") - 0.2, 3)});')

for n in range(3):
    t = T_PREF + 0.2 + n * 0.3
    js.append(f'tl.fromTo("#pf{n}", {{ y: 30, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.28, ease: "power3.out", immediateRender: false }}, {round(t, 3)});')
    SFX.append((f"pfp{n}", "key-press", t, 0.432, 0.3))

js += [f'tl.fromTo("#fc-lock", {{ scale: 0.88, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.6, ease: "back.out(1.6)", immediateRender: false }}, {round(T_FECHO - 0.1, 3)});',
       f'tl.fromTo("#fc-sl", {{ y: 28, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.45, ease: "power3.out", immediateRender: false }}, {round(T_FECHO + 0.45, 3)});',
       f'tl.fromTo("#fc-ar", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.45, immediateRender: false }}, {round(T_FECHO + 1.0, 3)});']
SFX.append(("fcch", "chime", T_FECHO + 0.9, 2.544, 0.4))

cap_els = legendas(sem=(12,))
sfx = "\n".join(f'      <audio id="sfx-{i}" class="clip" src="assets/audio/{f}.mp3" data-start="{round(max(0, s), 3)}" data-duration="{d}" data-track-index="{90 + n}" data-volume="{v}"></audio>'
                for n, (i, f, s, d, v) in enumerate(SFX))

CSS = f"""
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html, body {{ width: {W}px; height: {H}px; background: #000; overflow: hidden; }}
#root {{ position: relative; width: 100%; height: 100%; font-family: "Inter", sans-serif; color: #fff; overflow: hidden; }}
#ondas {{ position: absolute; inset: 0; }} #ondas svg {{ width: 100%; height: 100%; display: block; }}
#sweep {{ position: absolute; left: 50%; top: 0; width: 520px; height: 100%; margin-left: -260px; opacity: 0;
  background: linear-gradient(90deg, rgba(124,58,237,0) 0%, rgba(192,132,252,0.4) 50%, rgba(124,58,237,0) 100%); }}
#brand {{ position: absolute; left: 72px; top: 58px; display: flex; align-items: center; gap: 16px; opacity: 0.9; }}
#brand img.x {{ height: 34px; }} #brand img.w {{ height: 23px; }}
#brand span {{ width: 2px; height: 28px; background: #4a4a55; }}
.cena {{ position: absolute; left: 760px; right: 90px; top: 110px; height: 860px; }}
.palco {{ position: absolute; inset: 0; display: flex; flex-direction: column; justify-content: center; }}
.cena.centro {{ left: 0; right: 0; top: 0; height: {H}px; }}
.cena.centro .palco {{ align-items: center; }}
#c2-p {{ align-items: center; }}
.cap {{ position: absolute; left: 88px; width: 600px; top: 150px; height: 790px; display: flex; align-items: center; }}
.cap-in {{ font-family: "Outfit", "Inter", sans-serif; font-weight: 700; font-size: 74px; line-height: 1.12; letter-spacing: -0.02em; }}
.cap-in span {{ display: inline-block; }}
.pil {{ background: #fff; color: #000; border-radius: 12px; padding: 0 14px; }}
.zap {{ background: #0b0b0e; border: 2px solid #22222b; border-radius: 26px; padding: 26px 28px; }}
.zap-top {{ display: flex; align-items: center; gap: 14px; font-size: 28px; color: #b9b9c2; margin-bottom: 20px; }}
.dot {{ width: 15px; height: 15px; border-radius: 50%; background: {VERDE}; }}
.m {{ background: #15151c; border-radius: 16px; padding: 16px 20px; margin-bottom: 14px; font-size: 27px; color: #dcdce3; }}
.m:last-child {{ margin-bottom: 0; }}
.m b {{ display: block; font-size: 28px; color: #8e8e98; margin-bottom: 6px; font-weight: 600; }}
.m.bot {{ background: #16231d; border: 2px solid #23402f; }}
.m u {{ color: {ROXO2}; text-decoration: none; }}
.selo-bot {{ margin-top: 20px; align-self: flex-start; background: #10151a; border: 2px solid var(--c); color: var(--c);
  border-radius: 14px; padding: 14px 22px; font-size: 28px; font-weight: 600; }}
.cartao {{ background: #0b0b0e; border: 2px solid #22222b; border-radius: 26px; padding: 34px; }}
.cartao.perigo {{ border-color: #4a3a12; }}
.kick {{ font-family: "JetBrains Mono", monospace; font-size: 29px; letter-spacing: 0.2em; color: #76767f; margin-bottom: 24px; }}
.sw {{ display: flex; align-items: center; justify-content: space-between; background: #11111a; border: 2px solid #22222b;
  border-radius: 16px; padding: 20px 24px; margin-bottom: 14px; font-size: 32px; }}
.sw:last-child {{ margin-bottom: 0; }}
.led {{ width: 54px; height: 28px; border-radius: 14px; background: #2a2a34; display: block; }}
.wr {{ border-left: 7px solid var(--c); background: #11111a; border-radius: 12px; padding: 18px 24px; margin-bottom: 14px; }}
.wr:last-child {{ margin-bottom: 0; }}
.wr b {{ display: block; font-size: 34px; }} .wr small {{ font-size: 29px; color: #8c8c96; }}
.grade2 {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }}
.cmd {{ background: #0e0e13; border: 2px solid #22222b; border-radius: 20px; padding: 26px; }}
.cmd b {{ display: block; font-family: "JetBrains Mono", monospace; font-size: 40px; color: {ROXO2}; }}
.cmd small {{ font-size: 29px; color: #83838d; }}
.nk {{ background: #11111a; border: 2px solid #22222b; border-radius: 16px; padding: 18px 24px; margin-bottom: 14px; font-size: 28px; color: #c9c9d2; }}
.nk b {{ font-family: "JetBrains Mono", monospace; color: #ffd23a; }}
.nk small {{ display: block; font-size: 29px; color: #83838d; margin-top: 4px; }}
.aviso {{ margin-top: 18px; font-size: 29px; color: #f0b429; }}
.pf {{ background: #0e0e13; border: 2px solid #22222b; border-radius: 18px; padding: 22px 26px; margin-bottom: 14px; }}
.pf b {{ font-family: "JetBrains Mono", monospace; font-size: 34px; color: {ROXO2}; }}
.pf small {{ display: block; font-size: 29px; color: #83838d; margin-top: 4px; }}
.lock {{ display: flex; align-items: center; justify-content: center; gap: 26px; }}
.lock img.x {{ height: 96px; }} .lock img.wm {{ height: 72px; }}
.lock .bar {{ width: 3px; height: 84px; background: #55555f; }}
.lock.big img.x {{ height: 108px; }} .lock.big img.wm {{ height: 82px; }} .lock.big .bar {{ width: 3px; height: 94px; }}
#c12-p .lock.big img.x {{ height: 132px; }} #c12-p .lock.big img.wm {{ height: 100px; }} #c12-p .lock.big .bar {{ height: 116px; }}
.fecho-in {{ text-align: center; }}
.fc-sl {{ margin-top: 44px; font-family: "Outfit", "Inter", sans-serif; font-size: 56px; font-weight: 600; }}
.fc-ar {{ margin-top: 26px; font-family: "JetBrains Mono", monospace; font-size: 34px; color: #8c8c96; letter-spacing: 0.08em; }}
"""

ONDAS = f'''<svg viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid slice">
<defs><linearGradient id="g1" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0" stop-color="{ROXO}" stop-opacity="0"/><stop offset="0.45" stop-color="{ROXO2}" stop-opacity="0.6"/><stop offset="1" stop-color="{ROXO}" stop-opacity="0"/></linearGradient>
<linearGradient id="g2" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0" stop-color="{ROXO}" stop-opacity="0"/><stop offset="0.5" stop-color="{ROXO}" stop-opacity="0.45"/><stop offset="1" stop-color="{ROXO}" stop-opacity="0"/></linearGradient></defs>
<g id="onda-a" fill="none" stroke="url(#g1)" stroke-width="3">
  <path d="M-80 -40 C 420 260 260 520 700 760 C 940 900 1160 880 1500 1140"/>
  <path d="M-80 120 C 460 400 300 640 760 880 C 1000 1010 1220 1000 1560 1240"/>
  <path d="M-80 -200 C 380 120 220 400 660 640 C 900 780 1120 760 1460 1020"/>
</g>
<g id="onda-b" fill="none" stroke="url(#g2)" stroke-width="2.5">
  <path d="M2000 -40 C 1500 260 1660 520 1220 760 C 980 900 760 880 420 1140"/>
  <path d="M2000 160 C 1540 440 1700 680 1260 920 C 1020 1050 800 1040 460 1280"/>
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
      tl.fromTo("#onda-a", {{ x: 0, y: 0 }}, {{ x: -90, y: -40, duration: {FIM}, ease: "none" }}, 0);
      tl.fromTo("#onda-b", {{ x: 0, y: 0 }}, {{ x: 80, y: 30, duration: {FIM}, ease: "none" }}, 0);
      tl.set("#sweep", {{ opacity: 0 }}, 0);
{chr(10).join("      " + x for x in js)}
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
'''
open("index.html", "w").write(page)
print("ok", len(CENAS), "cenas ·", len(cap_els), "legendas ·", len(SFX), "sfx ·", FIM, "s")
