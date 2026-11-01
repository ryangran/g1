"""Gera index.html de "O Bilhete · Parte 3" (caminho POSTO) a partir de build/timing.json.

Placar da Parte 2: build/votacao.json. Estilos base: tools/base.css (os mesmos da Parte 2).
Uso (na pasta do episódio): python3 tools/narracao_google.py && python3 tools/montar.py
"""
import json
import os
import sys
import unicodedata

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cenas  # noqa: E402
import cenas2  # noqa: E402
import cenas3  # noqa: E402

T = json.load(open("build/timing.json"))
F = T["frases"]
DUR = round(T["total"] + 4.2, 2)
VOTOS = json.load(open("build/votacao.json"))
CSS = open("tools/base.css").read()


def norm(w):
    w = unicodedata.normalize("NFD", w.lower())
    return "".join(c for c in w if c.isalnum() and not unicodedata.combining(c))


def fr(prefixo):
    return next(f for f in F if f["texto"].startswith(prefixo))


def ini(prefixo):
    return fr(prefixo)["ini"]


ALIAS = {"Ele conferiu": ("Um taxista", None), "Problema três": ("Ele deslizou", None), "Problema dois": ("Ele deslizou", None)}


def pal(prefixo, palavra, n=0):
    if not any(f["texto"].startswith(prefixo) for f in F):
        prefixo, alt = ALIAS.get(prefixo, (prefixo, None))
        palavra = alt or palavra
    achadas = [p["ini"] for p in fr(prefixo)["palavras"] if norm(p["p"]).startswith(norm(palavra))]
    return achadas[n] if achadas else fr(prefixo)["ini"]


def cena(nome):
    for m in (cenas3, cenas2, cenas):
        if nome in m.CENAS:
            return m.CENAS[nome]


PLANOS = [
    ("p01", "s31", 0.0),
    ("p02", "i03", ini("Um taxista") - 0.05),
    ("p03", "s01", pal("Um taxista", "desde") - 0.1),
    ("p04", "#votos", ini("Vocês mandaram") - 0.05),
    ("p05", "s33", ini("Mas o carro preto") - 0.05),
    ("p06", "s31", pal("Mas o carro preto", "homem") - 0.2),
    ("p07", "#cartao", ini("Ele deslizou") - 0.05),
    ("p08", "s32", ini("Pago vinte") - 0.05),
    ("p09", "#regra", ini("Regra número três") - 0.05),
    ("p10", "s35", ini("Opção A") - 0.05),
    ("p11", "s34", ini("Opção B") - 0.05),
    ("p12", "s31", ini("Ou tem") - 0.05),
    ("p13", "#fecho", ini("A maioria escreve") - 0.05),
]
fim = [p[2] for p in PLANOS[1:]] + [DUR]
tempo = {p[1]: (p[2], f) for p, f in zip(PLANOS, fim) if p[1].startswith("#")}
js, els = [], []
for n, ((pid, alvo, t0), t1) in enumerate(zip(PLANOS, fim)):
    if alvo.startswith("#"):
        continue
    t0, t1 = round(t0, 3), round(t1, 3)
    d = round(t1 - t0, 3)
    els.append(f'      <div id="{pid}" class="clip plano" data-start="{t0}" data-duration="{d}" data-track-index="1"><div id="{pid}-img" class="palco">{cena(alvo)()}</div></div>')
    if alvo in cenas3.CENAS:
        js += cenas3.anim(alvo, pid, t0, t1, pal, ini)
    elif alvo in cenas2.CENAS:
        js += cenas2.anim(alvo, pid, t0, t1, pal, ini)
    else:
        js += cenas.anim(alvo, pid, t0, t1, pal)
    if pid != "p12":
        a, b = (1.0, 1.08) if n % 2 == 0 else (1.09, 1.02)
        js.append(f'tl.fromTo("#{pid}-img", {{ scale: {a} }}, {{ scale: {b}, duration: {d}, ease: "none", immediateRender: false }}, {t0});')

# ---------------------------------------------------------------- vocês decidiram
placar = VOTOS["placar"]
lider = max(p["votos"] for p in placar)
barras = "".join(f'<div class="vb{" lider" if p["votos"] == lider and lider > 0 else ""}"><div class="vb-rot"><span>{p["opcao"]}{" · A VIATURA" if p["opcao"] == "3º JEITO" else ""}</span><b>{p["pct"]}%</b></div><div class="vb-trilho"><i id="vb-{k}"></i></div></div>' for k, p in enumerate(placar))
a, b = tempo["#votos"]
js.append(f'tl.fromTo("#votos-topo", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3 }}, {a + 0.05});')
for k, p in enumerate(placar):
    js.append(f'tl.fromTo("#vb-{k}", {{ width: "0%" }}, {{ width: "{p["pct"]}%", duration: 0.7, ease: "power3.out" }}, {round(a + 0.25 + k * 0.25, 3)});')

# ---------------------------------------------------------------- pergunta no meio do vídeo
t_perg = ini("E você?")
js += [f'tl.fromTo("#pergunta span", {{ scale: 0.4, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.35, ease: "back.out(2.5)", stagger: 0.25 }}, {round(t_perg, 3)});']

# ---------------------------------------------------------------- painel
js.append('tl.set("#hud-risco-barra", { scaleX: 0.99 }, 0);')
t_oferta = pal("Pago vinte", "vinte")
js += [f'tl.fromTo("#cx-oferta", {{ scale: 0.4, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.4, ease: "back.out(2.5)" }}, {round(t_oferta, 3)});']
for alvo in ("#votos", "#cartao", "#regra"):
    a, b = tempo[alvo]
    alvos = "#hud-in, #cx-oferta" if alvo == "#regra" else "#hud-in"
    js.append(f'tl.to("{alvos}", {{ opacity: 0, duration: 0.12 }}, {a}); tl.to("{alvos}", {{ opacity: 1, duration: 0.12 }}, {b});')

# ---------------------------------------------------------------- cartões e carimbos
a, b = tempo["#cartao"]
js += [f'tl.fromTo("#cartao-papel", {{ x: 700, rotation: 8 }}, {{ x: 0, rotation: -3, duration: 0.7, ease: "power3.out" }}, {a + 0.1});']
a, b = tempo["#regra"]
js += [f'tl.fromTo("#regra-1", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3 }}, {a + 0.05});',
       f'tl.fromTo("#regra-riscadas", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3 }}, {a + 0.1});',
       f'tl.fromTo("#regra-2", {{ y: 30, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.35, ease: "power3.out" }}, {pal("Regra número três", "todo") - 0.1});',
       f'tl.fromTo("#regra-3", {{ y: 30, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.35, ease: "power3.out" }}, {pal("Regra número três", "todo", 1) - 0.1});']
CARIMBOS = [("car-comprador", "O COMPRADOR", pal("Ele deslizou", "comprador") + 0.1, tempo["#cartao"][1], 1380, -6),
            ("car-ameaca", "AMEAÇA", pal("Ou você vende", "mora") - 0.1, ini("Regra número três") - 0.05, 1480, 6)]
for cid, _, t0, _, _, rot in CARIMBOS:
    js.append(f'tl.fromTo("#{cid} span", {{ scale: 2.4, opacity: 0, rotation: {rot} }}, {{ scale: 1, opacity: 1, rotation: {rot}, duration: 0.22, ease: "power4.in" }}, {round(t0, 3)});')
a, b = tempo["#fecho"]
js += [f'tl.fromTo("#fecho-1", {{ y: 30, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.4, ease: "power3.out" }}, {a + 0.05});',
       f'tl.fromTo("#fecho-2 .bt", {{ scale: 0.4, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.35, ease: "back.out(2.5)", stagger: 0.25 }}, {a + 0.3});',
       f'tl.fromTo("#fecho-3", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.4 }}, {a + 0.9});',
       f'tl.fromTo("#fecho-4", {{ scale: 0.5, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.45, ease: "back.out(2)" }}, {a + 1.4});']
t_a, t_b = pal("Opção A", "VENDE"), pal("Opção B", "FOGE")
js += [f'tl.fromTo("#selo-a", {{ scale: 0.4, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.35, ease: "back.out(2.5)" }}, {t_a});',
       f'tl.fromTo("#selo-b", {{ scale: 0.4, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.35, ease: "back.out(2.5)" }}, {t_b});']
t_circ = pal("Ou tem", "escondido")

# ---------------------------------------------------------------- legendas
DESTAQUE = {"carro", "preto", "posto", "clovis", "quarenta", "milhoes", "seguindo", "seguro", "cafe", "ficava", "fugia", "cartao", "comprador",
            "vinte", "rodrigo", "dez", "mora", "pressa", "medo", "vende", "foge", "escondido", "amanha"}
BAIXO = {"p03"}
caps = []
for k, f in enumerate(F):
    grupos, g = [], []
    for w in f["palavras"]:
        g.append(w)
        if len(g) == 3 or w["p"].endswith((".", ":", "?", "…", ",")) and len(g) >= 2:
            grupos.append(g); g = []
    if g:
        grupos.append(g)
    for j, g in enumerate(grupos):
        a = g[0]["ini"] - 0.06
        b = grupos[j + 1][0]["ini"] - 0.06 if j + 1 < len(grupos) else g[-1]["fim"] + 0.12
        if k + 1 < len(F):
            b = min(b, F[k + 1]["ini"] - 0.07)
        html = " ".join(f'<b class="dest">{w["p"]}</b>' if norm(w["p"]) in DESTAQUE else w["p"] for w in g)
        plano = max((p for p in PLANOS if p[2] <= a + 0.06), key=lambda p: p[2])[0]
        caps.append((f"cap-{k}-{j}", round(max(a, 0), 3), round(max(b - a, 0.2), 3), html, plano in BAIXO))
cap_els = "\n".join(f'        <div id="{cid}" class="clip cap"{" style=\"top: 1690px\"" if baixo else ""} data-start="{a}" data-duration="{d}" data-track-index="0"><span>{h}</span></div>' for cid, a, d, h, baixo in caps)

# ---------------------------------------------------------------- som
SFX = [("chegada", "whoosh", 0.0, 0.8, 0.45), ("senta", "impact-bass-2", 1.3 - 1.95 + 0.1, 2.5, 0.35),
       ("perg", "pop", t_perg - 0.09, 0.7, 0.6), ("cartao", "whoosh-short", tempo["#cartao"][0] - 0.05, 0.57, 0.5),
       ("oferta", "sparkle", t_oferta, 1.8, 0.45)]
for n, ((pid, alvo, t0), t1) in enumerate(zip(PLANOS, fim)):
    if n > 1 and not alvo.startswith("#") and n % 2 == 0:
        SFX.append((f"wh-{pid}", "whoosh-short", t0 - 0.13, 0.57, 0.26))
for alvo in ("#votos", "#regra"):
    SFX.append((f"imp-{alvo[1:]}", "impact-bass-1", tempo[alvo][0] - 0.04, 2.0, 0.7))
for cid, _, t0, _, _, _ in CARIMBOS:
    SFX.append((f"car-{cid}", "impact-bass-2", t0 + 0.22 - 1.95, 2.5, 0.5))
SFX += [("selo-a", "pop", t_a - 0.09, 0.7, 0.6), ("selo-b", "pop", t_b - 0.09, 0.7, 0.6),
        ("circulo", "sparkle", t_circ, 1.8, 0.55), ("fecho", "impact-bass-1", tempo["#fecho"][0] + 1.4 - 0.04, 2.0, 0.55)]
sfx = "\n".join(f'      <audio id="sfx-{i}" class="clip" src="assets/audio/{f}.mp3" data-start="{round(max(0, s), 3)}" data-duration="{d}" data-track-index="{30 + n}" data-volume="{v}"></audio>' for n, (i, f, s, d, v) in enumerate(SFX))


def cl(alvo):
    a, b = tempo[alvo]
    return f'data-start="{round(a, 3)}" data-duration="{round(b - a, 3)}"'


carimbos = "\n".join(f'      <div id="{i}" class="clip carimbo" style="top: {top}px" data-start="{round(a, 3)}" data-duration="{round(b - a, 3)}" data-track-index="7"><span>{t}</span></div>' for i, t, a, b, top, _ in CARIMBOS)
fecho_ini = tempo["#fecho"][0]
perg_fim = ini("Ele deslizou") - 0.05
CSS_EXTRA = """
      #pergunta { position: absolute; left: 0; right: 0; top: 430px; display: flex; flex-direction: column; align-items: center; gap: 18px; }
      #pergunta span { display: inline-block; font-family: "Archivo Black", sans-serif; font-size: 70px; padding: 10px 36px; border-radius: 20px; border: 6px solid #000; box-shadow: 0 10px 0 #000; color: #111; }
      #cartao-papel { background: #f4f1ea; color: #1c1a17; padding: 50px 60px; border-radius: 10px; box-shadow: 0 30px 60px rgba(0,0,0,.5); text-align: left; width: 860px; }
      #cartao-papel small { display: block; font-family: "JetBrains Mono", monospace; font-weight: 700; font-size: 30px; letter-spacing: .2em; color: #8a8378; }
      #cartao-papel b { display: block; font-family: "Archivo Black", sans-serif; font-weight: 400; font-size: 82px; line-height: 1.05; margin: 16px 0 26px; }
      #cartao-papel p { font-family: "JetBrains Mono", monospace; font-size: 34px; color: #5b554a; }
      #cx-oferta { position: absolute; left: 36px; top: 330px; background: #ffd23a; color: #111; border: 4px solid #000; border-radius: 14px; padding: 8px 18px; font-family: "Archivo Black", sans-serif; font-size: 40px; }
      #cx-oferta small { display: block; font-family: "JetBrains Mono", monospace; font-size: 24px; font-weight: 700; letter-spacing: .1em; }
      #regra-riscadas { font-family: "JetBrains Mono", monospace; font-size: 28px; color: #6d6a64; text-decoration: line-through; margin-bottom: 30px; line-height: 1.6; }
"""

page = f'''<!doctype html>
<html lang="pt-BR">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="assets/lib/gsap.min.js"></script>
    <style>{CSS}{CSS_EXTRA}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-width="1080" data-height="1920">
{chr(10).join(els)}
      <div id="votos" class="clip cartao preto" {cl("#votos")} data-track-index="2">
        <div class="kick" id="votos-topo">PARTE 2 · VOCÊS DECIDIRAM</div>
        {barras}
      </div>
      <div id="cartao" class="clip cartao preto" {cl("#cartao")} data-track-index="2">
        <div id="cartao-papel"><small>CARTÃO DE VISITA</small><b>COMPRADOR<br>DE BILHETES</b><p>pagamento à vista · sem perguntas</p></div>
      </div>
      <div id="regra" class="clip cartao preto" {cl("#regra")} data-track-index="2">
        <div class="kick" id="regra-1">O CÓDIGO DA MADRUGADA · REGRA 3</div>
        <div id="regra-riscadas">1. Todo bilhete tem dois donos.<br>2. Quem tem pressa de pegar… não é o dono.</div>
        <div id="regra-2">Todo comprador tem pressa.</div>
        <div id="regra-3">Todo vendedor tem medo.</div>
      </div>
      <div id="fecho" class="clip cartao preto" {cl("#fecho")} data-track-index="2"></div>
      <div id="pergunta" class="clip" data-start="{round(t_perg - 0.05, 3)}" data-duration="{round(perg_fim - t_perg + 0.05, 3)}" data-track-index="8"><span style="background:#fff">FICAVA?</span><span style="background:#ffd23a">FUGIA?</span></div>
{carimbos}
      <div id="selo-a" class="clip selo" data-start="{round(t_a - 0.05, 3)}" data-duration="{round(ini("Opção B") - t_a, 3)}" data-track-index="9"><span style="background:#fff">VENDE</span></div>
      <div id="selo-b" class="clip selo" data-start="{round(t_b - 0.05, 3)}" data-duration="{round(ini("Ou tem") - t_b, 3)}" data-track-index="10"><span style="background:#ffd23a">FOGE</span></div>
      <div id="hud" class="clip" data-start="0" data-duration="{round(fecho_ini, 3)}" data-track-index="3">
        <div id="hud-in">
          <div class="caixa" id="cx-mala"><small>NO BANCO DE TRÁS</small><b>R$ 40.000.000</b></div>
          <div class="caixa" id="cx-bolso"><small>NO BOLSO</small><b>R$ 0</b></div>
          <div class="caixa" id="cx-risco"><small>RISCO</small><b><span id="hud-risco-n">99</span>%</b><div class="barra"><div id="hud-risco-barra"></div></div><div id="hud-delta">+0%</div></div>
        </div>
        <div id="cx-oferta" style="opacity:0"><small>OFERTA NA MESA</small>R$ 20.000.000</div>
      </div>
      <div id="legendas" class="clip" data-start="0" data-duration="{round(T["total"] + 0.3, 3)}" data-track-index="4" data-track-kind="captions" style="position:absolute;inset:0">
{cap_els}
      </div>
      <div id="fecho-1" class="clip fecho" data-start="{round(fecho_ini, 3)}" data-duration="{round(DUR - fecho_ini, 3)}" data-track-index="11">Comente <span class="amarelo">uma</span> palavra</div>
      <div id="fecho-2" class="clip fecho" data-start="{round(fecho_ini, 3)}" data-duration="{round(DUR - fecho_ini, 3)}" data-track-index="12"><span class="bt" style="background:#fff">VENDE</span><span class="bt" style="background:#ffd23a">FOGE</span></div>
      <div id="fecho-3" class="clip fecho" data-start="{round(fecho_ini, 3)}" data-duration="{round(DUR - fecho_ini, 3)}" data-track-index="13">ou ache o 3º jeito escondido<br>(só vale se disser qual é)</div>
      <div id="fecho-4" class="clip fecho" data-start="{round(fecho_ini, 3)}" data-duration="{round(DUR - fecho_ini, 3)}" data-track-index="14">PARTE 4<br>AMANHÃ</div>
      <audio id="narracao" class="clip" src="assets/audio/narracao.mp3" data-start="0" data-duration="{T["total"]:.2f}" data-track-index="20" data-volume="1"></audio>
      <audio id="trilha" class="clip" src="assets/audio/trilha.mp3" data-start="0" data-duration="{DUR}" data-track-index="21" data-volume="0.42"></audio>
{sfx}
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{ paused: true }});
{chr(10).join("      " + x for x in js)}
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
'''
open("index.html", "w").write(page)
print("ok", len(caps), "legendas ·", DUR, "s")
