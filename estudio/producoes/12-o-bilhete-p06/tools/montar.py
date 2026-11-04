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
import cenas4  # noqa: E402
import cenas5  # noqa: E402
import cenas6  # noqa: E402

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
    for m in (cenas6, cenas5, cenas4, cenas3, cenas2, cenas):
        if nome in m.CENAS:
            return m.CENAS[nome]


PLANOS = [
    ("p01", "s61", 0.0),
    ("p02", "s61", ini("Ele levantou") - 0.05),
    ("p03", "#votos", ini("Um taxista") - 0.05),
    ("p04", "#rg", ini("Vocês acharam") - 0.05),
    ("p05", "s62", ini("No vídeo") - 0.05),
    ("p06", "s64", ini("O velho assistiu") - 0.05),
    ("p07", "s62", ini("Só que o vídeo") - 0.05),
    ("p08", "s63", ini("Na porta do posto") - 0.05),
    ("p09", "s66", ini("Opção A") - 0.05),
    ("p09b", "s67", ini("Opção B") - 0.05),
    ("p10", "s65", ini("Ou tem") - 0.05),
    ("p11", "#fecho", ini("Hoje só vale") - 0.05),
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
    if alvo in cenas6.CENAS:
        js += cenas6.anim(alvo, pid, t0, t1, pal, ini)
    elif alvo in cenas5.CENAS:
        js += cenas5.anim(alvo, pid, t0, t1, pal, ini)
    elif alvo in cenas4.CENAS:
        js += cenas4.anim(alvo, pid, t0, t1, pal, ini)
    elif alvo in cenas3.CENAS:
        js += cenas3.anim(alvo, pid, t0, t1, pal, ini)
    elif alvo in cenas2.CENAS:
        js += cenas2.anim(alvo, pid, t0, t1, pal, ini)
    else:
        js += cenas.anim(alvo, pid, t0, t1, pal)
    if pid != cenas6.ZOOM6:
        a, b = (1.0, 1.08) if n % 2 == 0 else (1.09, 1.02)
        js.append(f'tl.fromTo("#{pid}-img", {{ scale: {a} }}, {{ scale: {b}, duration: {d}, ease: "none", immediateRender: false }}, {t0});')

# ---------------------------------------------------------------- vocês decidiram
placar = VOTOS["placar"]
lider = max(p["votos"] for p in placar)
barras = "".join(f'<div class="vb{" lider" if p["votos"] == lider and lider > 0 else ""}"><div class="vb-rot"><span>{p["opcao"]}</span><b>{p["pct"]}%</b></div><div class="vb-trilho"><i id="vb-{k}"></i></div></div>' for k, p in enumerate(placar))
a, b = tempo["#votos"]
js.append(f'tl.fromTo("#votos-topo", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3 }}, {a + 0.05});')
for k, p in enumerate(placar):
    js.append(f'tl.fromTo("#vb-{k}", {{ width: "0%" }}, {{ width: "{p["pct"]}%", duration: 0.7, ease: "power3.out" }}, {round(a + 0.25 + k * 0.25, 3)});')

# ---------------------------------------------------------------- pergunta no meio do vídeo


# ---------------------------------------------------------------- painel
js.append('tl.set("#hud-risco-barra", { scaleX: 0.99 }, 0);')
t_oferta = ini("No vídeo") + 0.3
js += [f'tl.fromTo("#cx-oferta", {{ scale: 0.4, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.4, ease: "back.out(2.5)" }}, {round(t_oferta, 3)});']
for alvo in ("#votos", "#rg"):
    a, b = tempo[alvo]
    alvos = "#hud-in, #cx-oferta"
    js.append(f'tl.to("{alvos}", {{ opacity: 0, duration: 0.12 }}, {a}); tl.to("{alvos}", {{ opacity: 1, duration: 0.12 }}, {b});')

# ---------------------------------------------------------------- cartões e carimbos
a, b = tempo["#rg"]
t_alug = pal("Vocês acharam", "Beatriz")
js += [f'tl.fromTo("#rg-papel", {{ x: 700, rotation: 8 }}, {{ x: 0, rotation: -3, duration: 0.7, ease: "power3.out" }}, {a + 0.1});',
       f'tl.fromTo("#rg-carimbo", {{ scale: 2.6, opacity: 0, rotation: -14 }}, {{ scale: 1, opacity: 1, rotation: -14, duration: 0.22, ease: "power4.in" }}, {round(t_alug, 3)});']
CARIMBOS = [("car-prova", "A PROVA", pal("No vídeo", "vinte") - 0.1, ini("O velho assistiu") - 0.05, 1470, -6),
            ("car-rodrigo", "O SOBRINHO", pal("Na porta do posto", "Rodrigo") - 0.1, ini("Opção A") - 0.05, 1470, 6)]
for cid, _, t0, _, _, rot in CARIMBOS:
    js.append(f'tl.fromTo("#{cid} span", {{ scale: 2.4, opacity: 0, rotation: {rot} }}, {{ scale: 1, opacity: 1, rotation: {rot}, duration: 0.22, ease: "power4.in" }}, {round(t0, 3)});')
a, b = tempo["#fecho"]
js += [f'tl.fromTo("#fecho-1", {{ y: 30, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.4, ease: "power3.out" }}, {a + 0.05});',
       f'tl.fromTo("#fecho-2 .bt", {{ scale: 0.4, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.35, ease: "back.out(2.5)", stagger: 0.25 }}, {a + 0.3});',
       f'tl.fromTo("#fecho-3", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.4 }}, {a + 0.9});',
       f'tl.fromTo("#fecho-4", {{ scale: 0.5, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.45, ease: "back.out(2)" }}, {a + 1.4});']
t_p08 = next(p[2] for p in PLANOS if p[0] == "p08")
js.append(f'tl.to("#cx-oferta", {{ opacity: 0, duration: 0.12 }}, {round(t_p08 - 0.14, 3)});')
t_a, t_b = pal("Opção A", "DEVOLVE"), pal("Opção B", "SEGUE")
js += [f'tl.fromTo("#selo-a", {{ scale: 0.4, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.35, ease: "back.out(2.5)" }}, {t_a});',
       f'tl.fromTo("#selo-b", {{ scale: 0.4, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.35, ease: "back.out(2.5)" }}, {t_b});']
t_circ = pal("Ou tem", "escondido")

# ---------------------------------------------------------------- legendas
DESTAQUE = {"contou", "fingiu", "celular", "video", "quarenta", "milhoes", "errado", "escondido", "beatriz", "primeiro",
            "vinte", "antonio", "re", "acabou", "rodrigo", "sobrinho", "devolve", "segue", "amanha"}
BAIXO = {"p01", "p02", "p05", "p06", "p07", "p08", "p09", "p09b", "p10"}
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
SFX = [("chegada", "whoosh", 0.0, 0.8, 0.45), ("abre", "impact-bass-2", 0.6 - 1.95 + 0.1, 2.5, 0.45),
       ("rg", "whoosh-short", tempo["#rg"][0] - 0.05, 0.57, 0.5), ("achou", "sparkle", t_alug, 1.8, 0.6),
       ("oferta", "sparkle", t_oferta, 1.8, 0.45)]
for n, ((pid, alvo, t0), t1) in enumerate(zip(PLANOS, fim)):
    if n > 1 and not alvo.startswith("#") and n % 2 == 0:
        SFX.append((f"wh-{pid}", "whoosh-short", t0 - 0.13, 0.57, 0.26))
for alvo in ("#votos", "#rg"):
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
CSS_EXTRA = """
      #pergunta { position: absolute; left: 0; right: 0; top: 430px; display: flex; flex-direction: column; align-items: center; gap: 18px; }
      #pergunta span { display: inline-block; font-family: "Archivo Black", sans-serif; font-size: 70px; padding: 10px 36px; border-radius: 20px; border: 6px solid #000; box-shadow: 0 10px 0 #000; color: #111; }
      #rg-papel { position: relative; background: #f6f1e2; color: #1c1a17; padding: 50px 60px; border-radius: 16px; border: 6px solid #d9b44a; box-shadow: 0 30px 60px rgba(0,0,0,.5); text-align: left; width: 860px; }
      #rg-papel small { display: block; font-family: "JetBrains Mono", monospace; font-weight: 700; font-size: 28px; letter-spacing: .18em; color: #8a6d1f; }
      #rg-papel b { display: block; font-family: "Archivo Black", sans-serif; font-weight: 400; font-size: 62px; margin: 14px 0 18px; }
      #rg-papel p { font-family: "JetBrains Mono", monospace; font-size: 32px; color: #3d4a3f; line-height: 1.5; }
      #rg-carimbo { position: absolute; right: 20px; bottom: 24px; font-family: "Archivo Black", sans-serif; font-size: 60px; color: #2f8f4f; border: 8px solid #2f8f4f; border-radius: 12px; padding: 4px 22px; opacity: 0; }
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
        <div class="kick" id="votos-topo">PARTE 5 · VOCÊS DECIDIRAM</div>
        {barras}
      </div>
      <div id="rg" class="clip cartao preto" {cl("#rg")} data-track-index="2">
        <div id="rg-papel"><small>3º JEITO ENCONTRADO</small><b>@beatrizxw_ana</b><p>"Pega o vídeo do posto"<br>5 minutos depois do vídeo</p><div id="rg-carimbo" data-layout-allow-overlap>ACHOU</div></div>
      </div>
      <div id="fecho" class="clip cartao preto" {cl("#fecho")} data-track-index="2"></div>
{carimbos}
      <div id="selo-a" class="clip selo" data-start="{round(t_a - 0.05, 3)}" data-duration="{round(ini("Opção B") - t_a, 3)}" data-track-index="9"><span style="background:#fff">DEVOLVE</span></div>
      <div id="selo-b" class="clip selo" data-start="{round(t_b - 0.05, 3)}" data-duration="{round(ini("Ou tem") - t_b, 3)}" data-track-index="10"><span style="background:#ffd23a">SEGUE</span></div>
      <div id="hud" class="clip" data-start="0" data-duration="{round(fecho_ini, 3)}" data-track-index="3">
        <div id="hud-in">
          <div class="caixa" id="cx-mala"><small>NO BANCO DE TRÁS</small><b>R$ 40.000.000</b></div>
          <div class="caixa" id="cx-bolso"><small>NO BOLSO</small><b>R$ 0</b></div>
          <div class="caixa" id="cx-risco"><small>RISCO</small><b><span id="hud-risco-n">99</span>%</b><div class="barra"><div id="hud-risco-barra"></div></div><div id="hud-delta">+0%</div></div>
        </div>
        <div id="cx-oferta" style="opacity:0"><small>NA MALA, NO TÁXI</small>R$ 20.000.000</div>
      </div>
      <div id="legendas" class="clip" data-start="0" data-duration="{round(T["total"] + 0.3, 3)}" data-track-index="4" data-track-kind="captions" style="position:absolute;inset:0">
{cap_els}
      </div>
      <div id="fecho-1" class="clip fecho" data-start="{round(fecho_ini, 3)}" data-duration="{round(DUR - fecho_ini, 3)}" data-track-index="11">Hoje só vale <span class="amarelo">uma</span> destas</div>
      <div id="fecho-2" class="clip fecho" data-start="{round(fecho_ini, 3)}" data-duration="{round(DUR - fecho_ini, 3)}" data-track-index="12"><span class="bt" style="background:#fff">DEVOLVE</span><span class="bt" style="background:#ffd23a">SEGUE</span></div>
      <div id="fecho-3" class="clip fecho" data-start="{round(fecho_ini, 3)}" data-duration="{round(DUR - fecho_ini, 3)}" data-track-index="13">ou ache o 3º jeito escondido<br>(só vale se disser qual é)</div>
      <div id="fecho-4" class="clip fecho" data-start="{round(fecho_ini, 3)}" data-duration="{round(DUR - fecho_ini, 3)}" data-track-index="14">PARTE 7<br>AMANHÃ</div>
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
