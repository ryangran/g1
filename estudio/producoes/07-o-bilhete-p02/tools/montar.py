"""Gera index.html de "O Bilhete · Parte 2" (caminho ACELERA) a partir de build/timing.json.

Placar do "vocês decidiram": build/votacao.json (estudio/tools/comentarios.py). Passageiros pagos:
build/passageiros.json (estudio/tools/passageiros.py); sem passageiros o bloco não entra.
Uso (na pasta do episódio): python3 tools/narracao_google.py && python3 tools/montar.py
"""
import json
import os
import sys
import unicodedata

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cenas  # noqa: E402  (cenas da Parte 1)
import cenas2  # noqa: E402  (cenas novas)

T = json.load(open("build/timing.json"))
F = T["frases"]
DUR = round(T["total"] + 4.2, 2)
VOTOS = json.load(open("build/votacao.json"))


def norm(w):
    w = unicodedata.normalize("NFD", w.lower())
    return "".join(c for c in w if c.isalnum() and not unicodedata.combining(c))


def fr(prefixo):
    return next(f for f in F if f["texto"].startswith(prefixo))


def ini(prefixo):
    return fr(prefixo)["ini"]


# frases da Parte 1 que as animações das cenas reaproveitadas procuram → equivalentes da Parte 2
ALIAS = {("Ele saiu do hotel", "velho"): ("Ou seja", "dele"), ("Ele conferiu", None): ("A maioria", None),
         ("Problema três", None): ("Problema dois", None)}


def pal(prefixo, palavra, n=0):
    if not any(f["texto"].startswith(prefixo) for f in F):
        prefixo, palavra = ALIAS.get((prefixo, palavra), ALIAS.get((prefixo, None), (prefixo, palavra)))[0], ALIAS.get((prefixo, palavra), (None, palavra))[1] or palavra
    achadas = [p["ini"] for p in fr(prefixo)["palavras"] if norm(p["p"]).startswith(norm(palavra))]
    return achadas[n]


def cena(nome):
    return cenas2.CENAS[nome] if nome in cenas2.CENAS else cenas.CENAS[nome]


PLANOS = [  # (id, cena ou #cartão, início)
    ("p01", "s01", 0.0),
    ("p02", "#rebobina", ini("Mas volta") - 0.05),
    ("p03", "#votos", ini("A maioria") - 0.05),
    ("p04", "i02", pal("A maioria", "terceiro") - 0.15),
    ("p05", "i11", ini("O Clóvis arrancou") - 0.05),
    ("p06", "i09", pal("O Clóvis arrancou", "Mas") - 0.05),
    ("p07", "#placa", ini("Problema um") - 0.05),
    ("p08", "s06", ini("Dez minutos") - 0.05),
    ("p09", "s07", ini("Clóvis, um passageiro") - 0.05),
    ("p10", "s08", ini("Problema dois") - 0.05),
    ("p11", "#ficha", ini("E a central contou") - 0.05),
    ("p12", "i10", ini("Ou seja") - 0.05),
    ("p13", "s01", ini("Duas da manhã") - 0.05),
    ("p14", "s12", ini("O carro preto encostou") - 0.05),
    ("p15", "#regra", ini("Regra número dois") - 0.05),
    ("p16", "s14", ini("O que a gente faz") - 0.05),
    ("p17", "s15", ini("Opção B") - 0.05),
    ("p18", "s01", ini("Ou tem um terceiro") - 0.05),
    ("p19", "#fecho", ini("A maioria escreve") - 0.05),
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
    if alvo in cenas2.CENAS:
        js += cenas2.anim(alvo, pid, t0, t1, pal, ini)
    else:
        js += cenas.anim(alvo, pid, t0, t1, pal) if alvo != "i02" else []
    a, b = (1.0, 1.08) if n % 2 == 0 else (1.09, 1.02)
    if pid not in ("p04", "p18"):  # esses têm zoom próprio
        js.append(f'tl.fromTo("#{pid}-img", {{ scale: {a} }}, {{ scale: {b}, duration: {d}, ease: "none", immediateRender: false }}, {t0});')

# o recibo continua no tapete (ninguém achou): zoom nele com uma interrogação
t_rec = tempo["#votos"][1]
js += [f'tl.fromTo("#p04 svg", {{ scale: 1, x: 0, y: 0, transformOrigin: "0px 0px" }}, {{ scale: 2.0, x: {540 - 800 * 2.0}, y: {960 - 1690 * 2.0}, duration: 1.0, ease: "power3.inOut", immediateRender: false }}, {round(t_rec + 0.6, 3)});',
       f'tl.fromTo("#interroga", {{ scale: 0.3, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.35, ease: "back.out(2.5)" }}, {round(pal("A maioria", "Ele"), 3)});']
# flash do celular fotografando a placa
t_foto = pal("O Clóvis arrancou", "fotografou")
js.append(f'tl.fromTo("#flash", {{ opacity: 0 }}, {{ opacity: 0.9, duration: 0.06, yoyo: true, repeat: 1, immediateRender: false }}, {round(t_foto + 0.25, 3)});')
# rebobinar: "10 MINUTOS ANTES"
a, b = tempo["#rebobina"]
js += [f'tl.fromTo("#rebob-1", {{ x: 60, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.25, ease: "power3.out" }}, {a + 0.05});',
       f'tl.fromTo("#rebob-2", {{ scale: 1.6, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.25, ease: "power4.in" }}, {a + 0.2});',
       f'tl.fromTo("#rebobina .scan", {{ y: 0 }}, {{ y: 1920, duration: 0.5, ease: "none", repeat: 2, immediateRender: false }}, {a});']

# ---------------------------------------------------------------- vocês decidiram (placar real)
placar = VOTOS["placar"]
lider = max(p["votos"] for p in placar) if placar else 0
barras = "".join(
    f'<div class="vb{" lider" if p["votos"] == lider and lider > 0 else ""}"><div class="vb-rot"><span>{p["opcao"]}{" · O RECIBO" if p["opcao"] == "3º JEITO" else ""}</span><b>{p["pct"]}%</b></div><div class="vb-trilho"><i id="vb-{k}"></i></div></div>'
    for k, p in enumerate(placar))
a, b = tempo["#votos"]
js.append(f'tl.fromTo("#votos-topo", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3 }}, {a + 0.05});')
for k, p in enumerate(placar):
    js.append(f'tl.fromTo("#vb-{k}", {{ width: "0%" }}, {{ width: "{p["pct"]}%", duration: 0.7, ease: "power3.out" }}, {round(a + 0.25 + k * 0.25, 3)});')
total_txt = f'{VOTOS["total_votos"]} voto{"s" if VOTOS["total_votos"] != 1 else ""} · vale o último comentário'

# ---------------------------------------------------------------- painel
RISCO = [(pal("Problema um", "placa"), 90), (pal("Problema dois", "nome"), 95), (pal("O carro preto encostou", "devagar"), 99)]
js.append('tl.set("#hud-risco-barra", { scaleX: 0.85 }, 0);')
antes = 85
for tt, v in RISCO:
    js += [f'tl.to("#hud-risco-n", {{ textContent: {v}, snap: {{ textContent: 1 }}, duration: 0.5, ease: "power1.out" }}, {tt});',
           f'tl.to("#hud-risco-barra", {{ scaleX: {v / 100}, duration: 0.5, ease: "power1.out" }}, {tt});',
           f'tl.set("#hud-delta", {{ textContent: "+{v - antes}%" }}, {tt});',
           f'tl.fromTo("#hud-delta", {{ opacity: 1, y: 0 }}, {{ opacity: 0, y: -14, duration: 1.1, ease: "power1.in", immediateRender: false }}, {tt});']
    antes = v
for alvo in ("#rebobina", "#votos", "#placa", "#ficha", "#regra"):
    a, b = tempo[alvo]
    js.append(f'tl.to("#hud-in", {{ opacity: 0, duration: 0.12 }}, {a}); tl.to("#hud-in", {{ opacity: 1, duration: 0.12 }}, {b});')

# ---------------------------------------------------------------- cartões, carimbos, etiquetas
a, b = tempo["#placa"]
js += [f'tl.fromTo("#placa-topo", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3 }}, {a + 0.05});',
       f'tl.fromTo("#placa-foto", {{ scale: 0.6, rotation: -8, opacity: 0 }}, {{ scale: 1, rotation: -3, opacity: 1, duration: 0.4, ease: "back.out(1.8)" }}, {a + 0.15});',
       f'tl.fromTo("#placa-7", {{ color: "#1c1a17" }}, {{ color: "#e23b2e", duration: 0.2 }}, {round(pal("Problema um", "sete") - 0.05, 3)});']
a, b = tempo["#ficha"]
FICHA = [("ficha-1", pal("E a central contou", "Rodrigo")), ("ficha-2", pal("E a central contou", "sobrinho"))]
js.append(f'tl.fromTo("#ficha-topo", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3 }}, {a + 0.05});')
for fid, tt in FICHA:
    js.append(f'tl.fromTo("#{fid}", {{ x: -60, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.25, ease: "power3.out" }}, {round(tt - 0.15, 3)});')
a, b = tempo["#regra"]
js += [f'tl.fromTo("#regra-1", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3 }}, {a + 0.05});',
       f'tl.fromTo("#regra-riscada", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3 }}, {a + 0.1});',
       f'tl.fromTo("#regra-2", {{ y: 30, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.35, ease: "power3.out" }}, {pal("Regra número dois", "quem") - 0.1});',
       f'tl.fromTo("#regra-3", {{ y: 30, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.35, ease: "power3.out" }}, {pal("Regra número dois", "não") - 0.1});']
CARIMBOS = [("car-foto", "FOTOGRAFADA", pal("Problema um", "Final"), tempo["#placa"][1], 1380, -6),
            ("car-ident", "IDENTIFICADO", pal("Problema dois", "nome") + 0.05, ini("E a central contou") - 0.05, 1500, 6),
            ("car-dono", "NÃO É O DONO", pal("Ou seja", "dele") - 0.1, ini("Duas da manhã") - 0.05, 1470, -5)]
for cid, _, t0, _, _, rot in CARIMBOS:
    js.append(f'tl.fromTo("#{cid} span", {{ scale: 2.4, opacity: 0, rotation: {rot} }}, {{ scale: 1, opacity: 1, rotation: {rot}, duration: 0.22, ease: "power4.in" }}, {round(t0, 3)});')
TAGS = [("tag-2", "PROBLEMA 2 · O NOME", ini("Problema dois"), ini("E a central contou") - 0.05)]
for tid, _, t0, _ in TAGS:
    js.append(f'tl.fromTo("#{tid} span", {{ x: -40, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.3, ease: "power3.out" }}, {round(t0, 3)});')
a, b = tempo["#fecho"]
js += [f'tl.fromTo("#fecho-1", {{ y: 30, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.4, ease: "power3.out" }}, {a + 0.05});',
       f'tl.fromTo("#fecho-2 .bt", {{ scale: 0.4, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.35, ease: "back.out(2.5)", stagger: 0.25 }}, {a + 0.3});',
       f'tl.fromTo("#fecho-3", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.4 }}, {a + 0.9});',
       f'tl.fromTo("#fecho-4", {{ scale: 0.5, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.45, ease: "back.out(2)" }}, {a + 1.4});']
t_a, t_b = pal("O que a gente faz", "POSTO"), pal("Opção B", "LIGA")
js += [f'tl.fromTo("#selo-a", {{ scale: 0.4, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.35, ease: "back.out(2.5)" }}, {t_a});',
       f'tl.fromTo("#selo-b", {{ scale: 0.4, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.35, ease: "back.out(2.5)" }}, {t_b});']
t_circ = pal("Ou tem um terceiro", "escondido")

# ---------------------------------------------------------------- legendas
DESTAQUE = {"carro", "preto", "clovis", "acelerar", "terceiro", "ninguem", "tapete", "placa", "sete", "nome", "rodrigo", "sobrinho", "antonio",
            "dele", "vidro", "devagar", "pressa", "dono", "posto", "liga", "escondido", "amanha", "central", "fotografou"}
BAIXO = {"p01", "p13", "p18"}  # cenas com o carro preto embaixo: legenda vai para o rodapé
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
SFX = [("chegada", "whoosh", 0.0, 0.8, 0.5), ("freio", "impact-bass-2", 1.45 - 1.95 + 0.1, 2.5, 0.35),
       ("rebob", "glitch-3", tempo["#rebobina"][0] - 0.05, 0.6, 0.55), ("flash", "click-soft", t_foto + 0.2, 0.36, 0.9)]
for n, ((pid, alvo, t0), t1) in enumerate(zip(PLANOS, fim)):
    if n > 2 and not alvo.startswith("#") and n % 2 == 1:
        SFX.append((f"wh-{pid}", "whoosh-short", t0 - 0.13, 0.57, 0.26))
for alvo in ("#votos", "#regra"):
    SFX.append((f"imp-{alvo[1:]}", "impact-bass-1", tempo[alvo][0] - 0.04, 2.0, 0.7))
for cid, _, t0, _, _, _ in CARIMBOS:
    SFX.append((f"car-{cid}", "impact-bass-2", t0 + 0.22 - 1.95, 2.5, 0.5))
for fid, tt in FICHA:
    SFX.append((f"clk-{fid}", "click-soft", tt - 0.19, 0.36, 0.8))
SFX += [("virada", "glitch-3", pal("Ou seja", "dele") - 0.15, 0.6, 0.35), ("radio", "glitch-3", ini("Clóvis, um passageiro") - 0.1, 0.6, 0.4),
        ("selo-a", "pop", t_a - 0.09, 0.7, 0.6), ("selo-b", "pop", t_b - 0.09, 0.7, 0.6),
        ("circulo", "sparkle", t_circ, 1.8, 0.55), ("fecho", "impact-bass-1", tempo["#fecho"][0] + 1.4 - 0.04, 2.0, 0.55)]
sfx = "\n".join(f'      <audio id="sfx-{i}" class="clip" src="assets/audio/{f}.mp3" data-start="{round(max(0, s), 3)}" data-duration="{d}" data-track-index="{30 + n}" data-volume="{v}"></audio>' for n, (i, f, s, d, v) in enumerate(SFX))


def cl(alvo):
    a, b = tempo[alvo]
    return f'data-start="{round(a, 3)}" data-duration="{round(b - a, 3)}"'


tags = "\n".join(f'      <div id="{i}" class="clip tag" data-start="{round(a, 3)}" data-duration="{round(b - a, 3)}" data-track-index="6"><span>{t}</span></div>' for i, t, a, b in TAGS)
carimbos = "\n".join(f'      <div id="{i}" class="clip carimbo" style="top: {top}px" data-start="{round(a, 3)}" data-duration="{round(b - a, 3)}" data-track-index="7"><span>{t}</span></div>' for i, t, a, b, top, _ in CARIMBOS)
fecho_ini = tempo["#fecho"][0]
p04a, p04b = next(p[2] for p in PLANOS if p[0] == "p04"), next(p[2] for p in PLANOS if p[0] == "p05")
p06a, p06b = next(p[2] for p in PLANOS if p[0] == "p06"), next(p[2] for p in PLANOS if p[0] == "p07")

page = f'''<!doctype html>
<html lang="pt-BR">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="assets/lib/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: #0b111b; }}
      #root {{ position: relative; width: 100%; height: 100%; font-family: "Inter", sans-serif; overflow: hidden; }}
      .plano {{ position: absolute; inset: 0; overflow: hidden; }}
      .palco, .palco svg {{ width: 1080px; height: 1920px; display: block; }}
      .cartao {{ position: absolute; inset: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; padding: 0 90px; overflow: hidden; }}
      .preto {{ background: #1c1a17; color: #fff; }}
      .creme {{ background: #efe9df; color: #1c1a17; }}
      .kick {{ font-family: "JetBrains Mono", monospace; font-weight: 700; font-size: 30px; letter-spacing: .18em; opacity: .7; margin-bottom: 40px; }}
      .grande {{ font-family: "Archivo Black", sans-serif; font-size: 118px; line-height: 1.02; }}
      .amarelo {{ color: #ffd23a; }}
      .scan {{ position: absolute; left: 0; right: 0; top: -40px; height: 40px; background: rgba(255,255,255,.08); }}
      /* placar */
      .vb {{ width: 100%; margin: 26px 0; text-align: left; }}
      .vb-rot {{ display: flex; justify-content: space-between; font-family: "Archivo Black", sans-serif; font-size: 52px; }}
      .vb-rot b {{ font-weight: 400; color: #ffd23a; }}
      .vb-trilho {{ height: 34px; background: rgba(255,255,255,.12); border-radius: 17px; overflow: hidden; margin-top: 10px; }}
      .vb-trilho i {{ display: block; height: 100%; width: 0; background: #efe9df; border-radius: 17px; }}
      .vb.lider .vb-trilho i {{ background: #ffd23a; }}
      #votos-total {{ font-family: "JetBrains Mono", monospace; font-size: 28px; color: #a8b0ba; margin-top: 26px; }}
      #interroga {{ position: absolute; left: 0; right: 0; top: 600px; text-align: center; font-family: "Archivo Black", sans-serif; font-size: 240px; color: #ffd23a; -webkit-text-stroke: 8px #000; paint-order: stroke fill; }}
      #flash {{ position: absolute; inset: 0; background: #fff; opacity: 0; }}
      /* painel */
      #hud {{ position: absolute; left: 36px; right: 36px; top: 180px; }}
      #hud-in {{ display: flex; gap: 12px; }}
      .caixa {{ background: rgba(8,10,14,.84); border: 3px solid rgba(255,255,255,.16); border-radius: 16px; padding: 10px 14px; color: #fff; position: relative; }}
      .caixa small {{ display: block; font-family: "JetBrains Mono", monospace; font-size: 28px; font-weight: 700; letter-spacing: .06em; color: #a8b0ba; }}
      .caixa b {{ display: block; font-family: "Archivo Black", sans-serif; font-size: 40px; line-height: 1.15; }}
      #cx-mala {{ flex: 1.7; }} #cx-bolso {{ flex: 1; }} #cx-risco {{ flex: 1.1; }}
      #cx-risco b {{ color: #ff4b3e; }}
      .barra {{ height: 8px; background: rgba(255,255,255,.14); border-radius: 4px; margin-top: 4px; overflow: hidden; }}
      #hud-risco-barra {{ height: 100%; width: 100%; background: linear-gradient(90deg, #ffd23a, #ff4b3e); transform-origin: left center; }}
      #hud-delta {{ position: absolute; right: 12px; top: 8px; font-family: "JetBrains Mono", monospace; font-weight: 700; font-size: 28px; color: #fff; background: #e23b2e; border-radius: 8px; padding: 0 8px; opacity: 0; }}
      .tag {{ position: absolute; left: 36px; top: 330px; }}
      .tag span {{ display: inline-block; font-family: "JetBrains Mono", monospace; font-weight: 700; font-size: 30px; letter-spacing: .12em; color: #111; background: #ffd23a; padding: 6px 16px; border-radius: 8px; }}
      .carimbo {{ position: absolute; left: 0; right: 0; text-align: center; }}
      .carimbo span {{ display: inline-block; font-family: "Archivo Black", sans-serif; font-size: 92px; color: #ff3b30; border: 10px solid #ff3b30; border-radius: 16px; padding: 4px 30px; background: rgba(255,255,255,.1); }}
      /* placa */
      #placa-foto {{ background: #fff; padding: 24px 24px 60px; box-shadow: 0 20px 40px rgba(0,0,0,.35); }}
      #placa-foto .chapa {{ border: 10px solid #1c1a17; border-radius: 18px; padding: 10px 40px 20px; background: #f4f4f2; }}
      #placa-foto .chapa small {{ display: block; font-family: "JetBrains Mono", monospace; font-weight: 700; font-size: 30px; background: #2a5bd7; color: #fff; margin: 0 -40px 14px; padding: 6px; }}
      #placa-foto .chapa b {{ font-family: "Archivo Black", sans-serif; font-weight: 400; font-size: 130px; letter-spacing: .04em; }}
      #placa-foto p {{ font-family: "JetBrains Mono", monospace; font-size: 30px; margin-top: 22px; color: #555; }}
      .ficha-linha {{ font-family: "Archivo Black", sans-serif; font-size: 74px; line-height: 1.2; margin: 16px 0; }}
      .ficha-linha i {{ font-style: normal; font-family: "JetBrains Mono", monospace; font-size: 36px; display: block; opacity: .55; letter-spacing: .1em; }}
      #regra-riscada {{ font-family: "JetBrains Mono", monospace; font-size: 30px; color: #6d6a64; text-decoration: line-through; margin-bottom: 30px; }}
      #regra-2 {{ font-family: "Archivo Black", sans-serif; font-size: 90px; line-height: 1.08; }}
      #regra-3 {{ font-family: "Archivo Black", sans-serif; font-size: 96px; line-height: 1.08; color: #ffd23a; margin-top: 24px; }}
      .cap {{ position: absolute; left: 0; right: 0; top: 1300px; text-align: center; padding: 0 60px; }}
      .cap span {{ display: inline-block; font-family: "Archivo Black", sans-serif; font-size: 68px; line-height: 1.12; color: #fff; -webkit-text-stroke: 3px #000; paint-order: stroke fill; text-shadow: 0 6px 0 #000, 0 10px 24px rgba(0,0,0,.6); }}
      .dest {{ color: #ffd23a; }}
      .selo {{ position: absolute; left: 0; right: 0; top: 420px; text-align: center; }}
      .selo span {{ display: inline-block; font-family: "Archivo Black", sans-serif; font-size: 110px; padding: 14px 60px; border-radius: 24px; border: 7px solid #000; box-shadow: 0 12px 0 #000; color: #111; }}
      .fecho {{ position: absolute; left: 0; right: 0; text-align: center; color: #fff; }}
      #fecho-1 {{ top: 520px; font-size: 66px; font-weight: 800; }}
      #fecho-2 {{ top: 640px; display: flex; justify-content: center; gap: 26px; }}
      #fecho-2 .bt {{ font-family: "Archivo Black", sans-serif; font-size: 80px; padding: 12px 44px; border-radius: 20px; border: 6px solid #000; box-shadow: 0 10px 0 #000; color: #111; }}
      #fecho-3 {{ top: 830px; font-size: 42px; color: #cfd3d8; line-height: 1.3; }}
      #fecho-4 {{ top: 960px; font-family: "Archivo Black", sans-serif; font-size: 124px; line-height: 1; color: #ffd23a; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-width="1080" data-height="1920">
{chr(10).join(els)}
      <div id="rebobina" class="clip cartao preto" {cl("#rebobina")} data-track-index="2">
        <i class="scan"></i>
        <div class="kick" id="rebob-1">◀◀ VOLTANDO</div>
        <div class="grande amarelo" id="rebob-2">10 MINUTOS<br>ANTES</div>
      </div>
      <div id="votos" class="clip cartao preto" {cl("#votos")} data-track-index="2">
        <div class="kick" id="votos-topo">PARTE 1 · VOCÊS DECIDIRAM</div>
        {barras}
        <div id="votos-total">{total_txt}</div>
      </div>
      <div id="interroga" class="clip" data-start="{round(pal("A maioria", "Ele") - 0.05, 3)}" data-duration="{round(p04b - pal("A maioria", "Ele") + 0.05, 3)}" data-track-index="5">?</div>
      <div id="flash" class="clip" data-start="{round(p06a, 3)}" data-duration="{round(p06b - p06a, 3)}" data-track-index="5"></div>
      <div id="placa" class="clip cartao creme" {cl("#placa")} data-track-index="2">
        <div class="kick" id="placa-topo">PROBLEMA 1 · A PLACA</div>
        <div id="placa-foto"><div class="chapa"><small>BRASIL</small><b>TXI·4F1<span id="placa-7">7</span></b></div><p>foto · 01:07 · Hotel Imperial</p></div>
      </div>
      <div id="ficha" class="clip cartao creme" {cl("#ficha")} data-track-index="2">
        <div class="kick" id="ficha-topo">CENTRAL · REGISTRO DA LIGAÇÃO</div>
        <div class="ficha-linha" id="ficha-1"><i>NOME</i>RODRIGO A.</div>
        <div class="ficha-linha" id="ficha-2"><i>PARENTESCO</i>SOBRINHO DO<br>SEU ANTÔNIO</div>
      </div>
      <div id="regra" class="clip cartao preto" {cl("#regra")} data-track-index="2">
        <div class="kick" id="regra-1">O CÓDIGO DA MADRUGADA · REGRA 2</div>
        <div id="regra-riscada">1. Todo bilhete tem dois donos.</div>
        <div id="regra-2">Quem tem pressa de pegar…</div>
        <div id="regra-3">não é o dono.</div>
      </div>
      <div id="fecho" class="clip cartao preto" {cl("#fecho")} data-track-index="2"></div>
{tags}
{carimbos}
      <div id="selo-a" class="clip selo" data-start="{round(t_a - 0.05, 3)}" data-duration="{round(ini("Opção B") - t_a, 3)}" data-track-index="8"><span style="background:#fff">POSTO</span></div>
      <div id="selo-b" class="clip selo" data-start="{round(t_b - 0.05, 3)}" data-duration="{round(ini("Ou tem um terceiro") - t_b, 3)}" data-track-index="9"><span style="background:#ffd23a">LIGA</span></div>
      <div id="hud" class="clip" data-start="0" data-duration="{round(fecho_ini, 3)}" data-track-index="3">
        <div id="hud-in">
          <div class="caixa" id="cx-mala"><small>NO BANCO DE TRÁS</small><b>R$ 40.000.000</b></div>
          <div class="caixa" id="cx-bolso"><small>NO BOLSO</small><b>R$ 0</b></div>
          <div class="caixa" id="cx-risco"><small>RISCO</small><b><span id="hud-risco-n">85</span>%</b><div class="barra"><div id="hud-risco-barra"></div></div><div id="hud-delta">+0%</div></div>
        </div>
      </div>
      <div id="legendas" class="clip" data-start="0" data-duration="{round(T["total"] + 0.3, 3)}" data-track-index="4" data-track-kind="captions" style="position:absolute;inset:0">
{cap_els}
      </div>
      <div id="fecho-1" class="clip fecho" data-start="{round(fecho_ini, 3)}" data-duration="{round(DUR - fecho_ini, 3)}" data-track-index="11">Comente <span class="amarelo">uma</span> palavra</div>
      <div id="fecho-2" class="clip fecho" data-start="{round(fecho_ini, 3)}" data-duration="{round(DUR - fecho_ini, 3)}" data-track-index="12"><span class="bt" style="background:#fff">POSTO</span><span class="bt" style="background:#ffd23a">LIGA</span></div>
      <div id="fecho-3" class="clip fecho" data-start="{round(fecho_ini, 3)}" data-duration="{round(DUR - fecho_ini, 3)}" data-track-index="13">ou ache o 3º jeito escondido<br>(só vale se disser qual é)</div>
      <div id="fecho-4" class="clip fecho" data-start="{round(fecho_ini, 3)}" data-duration="{round(DUR - fecho_ini, 3)}" data-track-index="14">PARTE 3<br>AMANHÃ</div>
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
print("ok", len(caps), "legendas ·", DUR, "s · placar:", ", ".join(f'{p["opcao"]} {p["pct"]}%' for p in placar))
