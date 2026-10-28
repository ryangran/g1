"""Gera vertical.html: versão 9:16 (1080x1920) do vídeo Lula x SUS, com legendas da narração.

Mesma narração e trilha da versão 16:9 (assets/audio). Tempos das frases em tools/timing.json.
Uso (na pasta video/): python3 tools/gerar_vertical.py
"""
import html
import json

T = json.load(open("tools/timing.json"))
DUR = 69
STARTS, DURS = T["seg_starts"], T["seg_durs"]

# frase narrada (como aparece na legenda) — mesma ordem de tools/narracao.py
FRASES = [
    "Lula votou contra o SUS?", "A resposta está escondida nos arquivos de 1988.",
    "22 de setembro de 1988.", "A Constituinte vota o texto final da nova Constituição.",
    "474 votos a favor.", "Apenas 15 contra.", "Todos do PT.",
    "E entre eles, estava o líder da bancada.", "Luiz Inácio Lula da Silva.", "Ele votou não.",
    "Para o partido, o texto era conservador demais.",
    "Só que foi exatamente essa Constituição que criou o SUS.", "A saúde, direito de todos e dever do Estado.",
    "Mas atenção.", "O voto foi contra o texto inteiro, não contra um artigo do SUS.",
    "E, dias depois, Lula assinou a Constituição.",
    "O veredito?", "Lula votou contra a Constituição que criou o SUS.", "Fato.",
    "Mas a história completa é mais complicada do que parece.",
]
# peso falado dos números (a voz fala por extenso)
PESO = {"1988.": 31, "1988": 31, "22": 12, "474": 35, "15": 6}

# cenas: (início, fim)
CENAS = [(0, 8.89), (8.89, 25.59), (25.59, 36.8), (36.8, 45.27), (45.27, 55.3), (55.3, DUR)]
# textos na tela: id, cena, aparece em, top (px), classe, html
TELA = [
    ("v1-kicker", 0, 0, 300, "kicker", "ELEIÇÕES 2026 · CHECAGEM"),
    ("v1-title", 0, 0, 380, "h1", "Lula votou<br>contra o SUS<br>em 1988?"),
    ("v2-date", 1, 8.89, 240, "kicker", "22 DE SETEMBRO DE 1988"),
    ("v2-desc", 1, 13.5, 310, "body", "Votação do texto final<br>da Constituição"),
    ("v2-yes", 1, 17.72, 470, "big yes", "474 SIM"),
    ("v2-no", 1, 21.47, 690, "big no", "15 NÃO"),
    ("v2-note", 1, 21.9, 920, "body", "todos da bancada do PT"),
    ("v3-name", 2, 28.69, 330, "kicker", "LULA · LÍDER DO PT<br>NA CONSTITUINTE"),
    ("v3-vote", 2, 31.22, 470, "big no", "votou<br>NÃO"),
    ("v3-why", 2, 31.8, 900, "body", "O PT criticou, entre outros<br>pontos, a reforma agrária"),
    ("v4-head", 3, 36.8, 300, "h2", "Essa Constituição<br>criou o SUS"),
    ("v4-quote", 3, 41.25, 620, "quote", "“A saúde é direito<br>de todos e dever<br>do Estado”"),
    ("v4-ref", 3, 41.9, 950, "small", "Art. 196 · Constituição de 1988"),
    ("v5-head", 4, 45.27, 290, "kicker", "O CONTEXTO"),
    ("v5-p1", 4, 46.98, 380, "body lg", "A votação foi do<br>texto completo, não<br>de um artigo do SUS"),
    ("v5-p2", 4, 50.5, 720, "body lg", "Em 5/10/1988, Lula<br>e o PT assinaram<br>a Constituição"),
    ("v6-label", 5, 55.3, 260, "kicker", "VEREDITO"),
    ("v6-v", 5, 57.06, 340, "h2", "Votou contra a<br>Constituição que<br>criou o SUS: <em>FATO</em>"),
    ("v6-ctx", 5, 62.16, 720, "body", "Mas não foi um voto<br>específico contra o SUS"),
    ("v6-src", 5, 63.6, 930, "small", "Fontes: Diário da Assembleia<br>Nacional Constituinte · g1 Fato<br>ou Fake (23/10/2026) · Fundação<br>Perseu Abramo"),
]


def grupos(frase, n=4):
    """Divide em grupos de até n palavras, quebrando na vírgula."""
    out, cur = [], []
    for w in frase.split():
        cur.append(w)
        if len(cur) >= n or w.endswith(","):
            out.append(cur)
            cur = []
    if cur:
        out.append(cur)
    # evita grupo final de 1 palavra (junta ao anterior)
    if len(out) > 1 and len(out[-1]) == 1 and len(out[-2]) < 5:
        ultimo = out.pop()
        out[-1] += ultimo
    return out


def peso(ws):
    return sum(PESO.get(w, len(w)) + 1 for w in ws)


legendas = []
for i, frase in enumerate(FRASES):
    gs = grupos(frase)
    total = sum(peso(g) for g in gs)
    t = STARTS[i]
    for j, g in enumerate(gs):
        d = DURS[i] * peso(g) / total
        ini = t - (0.08 if j == 0 else 0)  # abre um pouco antes da primeira palavra
        fim = t + d + (0.15 if j == len(gs) - 1 else 0)
        legendas.append((f"cap-{i:02d}-{j}", round(ini, 2), round(fim - ini, 2), " ".join(g)))
        t += d

els = []
for k, (eid, sc, at, top, cls, txt) in enumerate(TELA):
    a, b = CENAS[sc]
    els.append(f'      <div id="{eid}" class="clip t {cls}" style="top: {top}px" data-start="{a}" data-duration="{round(b - a, 2)}" data-track-index="{k % 6}">{txt}</div>')
caps = [f'        <div id="{cid}" class="clip cap" data-start="{s}" data-duration="{d}" data-track-index="0"><span>{html.escape(txt)}</span></div>' for cid, s, d, txt in legendas]

js = []
for eid, sc, at, *_ in TELA:
    if eid in ("v1-kicker", "v1-title"):
        continue
    js.append(f'      tl.fromTo("#{eid}", {{ opacity: 0, y: 36 }}, {{ opacity: 1, y: 0, duration: 0.55, ease: "power3.out" }}, {at});')
js.append('      tl.fromTo("#v1-title", { scale: 0.94 }, { scale: 1, duration: 8, ease: "power1.out" }, 0);')
js.append('      tl.fromTo("#v1-kicker", { y: 0 }, { y: -12, duration: 8, ease: "power1.out" }, 0);')
js.append('      tl.fromTo("#v3-vote", { scale: 1.25 }, { scale: 1, duration: 0.5, ease: "power4.out" }, 31.22);')
for i, (a, b) in enumerate(CENAS[:-1]):
    ids = ", ".join(f'"#{e[0]}"' for e in TELA if e[1] == i)
    js.append(f'      tl.to([{ids}], {{ opacity: 0, duration: 0.35 }}, {round(b - 0.35, 2)});')
js.append('      tl.fromTo("#v6-v em", { color: "#ffffff" }, { color: "#ffd166", duration: 0.3 }, 60.86);')
for cid, s, d, _ in legendas:
    js.append(f'      tl.fromTo("#{cid} span", {{ opacity: 0, y: 14 }}, {{ opacity: 1, y: 0, duration: 0.12, ease: "power2.out" }}, {s});')
js.append(f'      tl.fromTo("#bar", {{ scaleX: 0 }}, {{ scaleX: 1, duration: {DUR}, ease: "none" }}, 0);')

page = f"""<!doctype html>
<html lang="pt-BR">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="assets/lib/gsap.min.js"></script>
    <style>
      :root {{
        --ground: #0f1115;
        --ink: #ffffff;
        --muted: #c9ccd3;
        --yes: #2ec4b6;
        --no: #ef476f;
        --gold: #ffd166;
      }}
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: var(--ground); }}
      #root {{ position: relative; width: 100%; height: 100%; font-family: "Inter", sans-serif; color: var(--ink); }}
      .clip {{ position: absolute; inset: 0; }}
      .t {{ inset: auto 0 auto 0; padding: 0 90px; text-align: center; }}
      .kicker {{ font-size: 40px; font-weight: 700; letter-spacing: 0.18em; line-height: 1.35; color: var(--gold); }}
      .h1 {{ font-size: 150px; font-weight: 900; line-height: 1.02; letter-spacing: -0.03em; }}
      .h2 {{ font-size: 100px; font-weight: 900; line-height: 1.08; letter-spacing: -0.02em; }}
      .h2 em {{ font-style: normal; }}
      .big {{ font-size: 200px; font-weight: 900; line-height: 1; letter-spacing: -0.03em; }}
      .yes {{ color: var(--yes); }}
      .no {{ color: var(--no); }}
      .body {{ font-size: 58px; line-height: 1.28; color: var(--muted); }}
      .lg {{ font-size: 72px; font-weight: 700; color: var(--ink); }}
      .quote {{ font-size: 88px; font-weight: 700; font-style: italic; line-height: 1.15; color: var(--yes); }}
      .small {{ font-size: 36px; line-height: 1.4; color: var(--muted); }}
      #legendas {{ inset: 0; }}
      .cap {{ inset: auto 0 auto 0; top: 1120px; padding: 0 70px; text-align: center; }}
      .cap span {{ display: inline-block; background: rgba(0, 0, 0, 0.62); border-radius: 22px; padding: 14px 30px;
                  font-size: 62px; font-weight: 900; line-height: 1.15; color: #fff; }}
      #bar {{ inset: auto 0 auto 0; top: 1345px; height: 8px; background: var(--gold); transform-origin: left center; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-width="1080" data-height="1920">
{chr(10).join(els)}
      <div id="legendas" class="clip" data-start="0" data-duration="{DUR}" data-track-index="6" data-track-kind="captions">
{chr(10).join(caps)}
      </div>
      <div id="bar" class="clip" data-start="0" data-duration="{DUR}" data-track-index="7" data-layout-ignore></div>
      <audio id="narracao" src="assets/audio/narracao.mp3" data-start="0" data-duration="68.79" data-track-index="8" data-volume="1"></audio>
      <audio id="trilha" src="assets/audio/trilha.mp3" data-start="0" data-duration="68.29" data-track-index="9" data-volume="1"></audio>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{ paused: true }});
{chr(10).join(js)}
      window.__timelines["main"] = tl;
      tl.seek(0);
    </script>
  </body>
</html>
"""
open("vertical.html", "w").write(page)
print(len(legendas), "legendas")
