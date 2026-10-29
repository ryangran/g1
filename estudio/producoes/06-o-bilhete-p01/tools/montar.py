"""Gera index.html de "O Bilhete · Parte 1" a partir de build/timing.json.

Ilustrações: assets/img/i01..i12 (.png/.jpg/.webp). A que faltar vira um quadro provisório
(assets/img/iNN.svg) com a descrição da cena, para revisar ritmo e cartões antes das imagens.
Uso (na pasta do episódio): python3 tools/narracao_google.py && python3 tools/montar.py
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cenas  # noqa: E402
import unicodedata

T = json.load(open("build/timing.json"))
F = T["frases"]
DUR = round(T["total"] + 4.2, 2)
CIRCULO = (830, 1530, 130)  # (x, y, raio) do recibo de farmácia em i02: ajuste quando a imagem chegar


def norm(w):
    w = unicodedata.normalize("NFD", w.lower())
    return "".join(c for c in w if c.isalnum() and not unicodedata.combining(c))


def fr(prefixo):
    return next(f for f in F if f["texto"].startswith(prefixo))


def ini(prefixo):
    return fr(prefixo)["ini"]


def pal(prefixo, palavra, n=0):
    """Início da n-ésima ocorrência de `palavra` na frase que começa com `prefixo`."""
    achadas = [p["ini"] for p in fr(prefixo)["palavras"] if norm(p["p"]).startswith(norm(palavra))]
    return achadas[n]


# ---------------------------------------------------------------- planos (imagem, início, movimento)
CENAS = {
    "i01": "Hotel à noite · o homem de terno se afasta · Clóvis olha o banco de trás",
    "i02": "Banco de trás · bilhete sob a luz do poste · recibo de farmácia no tapete",
    "i03": "Mãos: bilhete + celular com os 6 números",
    "i04": "Close: rosto em choque, suor, luz verde do painel",
    "i05": "Foto da filha no painel · envelope de cobrança",
    "i06": "Espelho lateral: o homem apalpa os bolsos e vira",
    "i07": "Painel: app da corrida + luz vermelha de gravação",
    "i08": "Verso do bilhete: nome e telefone à caneta",
    "i09": "Retrovisor: o homem sai do hotel correndo, ao telefone",
    "i10": "Close: homem de terno, relógio dourado, olhar frio",
    "i11": "Táxi arranca pela avenida molhada",
    "i12": "Clóvis ao lado do táxi com o bilhete · o homem vindo",
}


def imagem(nome):
    for ext in ("png", "jpg", "jpeg", "webp"):
        if os.path.exists(f"assets/img/{nome}.{ext}"):
            return f"assets/img/{nome}.{ext}"
    caminho = f"assets/img/{nome}.svg"
    import textwrap
    linhas = [l for parte in CENAS[nome].split(" · ") for l in textwrap.wrap(parte, 30)]
    texto = "".join(f'<text x="540" y="{900 + i * 70}" font-family="Inter, sans-serif" font-size="46" fill="#c9d2dc" text-anchor="middle">{l}</text>' for i, l in enumerate(linhas))
    open(caminho, "w").write(f'''<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1920" viewBox="0 0 1080 1920">
<defs><radialGradient id="g" cx="50%" cy="40%" r="75%"><stop offset="0" stop-color="#26364d"/><stop offset="1" stop-color="#0b111b"/></radialGradient></defs>
<rect width="1080" height="1920" fill="url(#g)"/><rect x="60" y="420" width="960" height="1080" rx="30" fill="none" stroke="#f29b38" stroke-width="6" stroke-dasharray="26 18"/>
<text x="540" y="760" font-family="Archivo Black, sans-serif" font-size="120" fill="#f29b38" text-anchor="middle">{nome.upper()}</text>
<text x="540" y="1380" font-family="Inter, sans-serif" font-size="34" fill="#7f8a99" text-anchor="middle">ilustração provisória · gerar no app Gemini</text>{texto}</svg>''')
    return caminho


PLANOS = [  # (id do plano, imagem ou cartão, início)
    ("p01", "i01", 0.0),
    ("p02", "i02", ini("Quando olhou") - 0.05),
    ("p03", "i03", ini("Ele conferiu") - 0.05),
    ("p04", "i04", ini("Quarenta") - 0.05),
    ("p05", "i05", ini("No banco de trás") - 0.05),
    ("p06", "#cartao-dono", ini("Agora vem") - 0.05),
    ("p07", "i06", ini("Problema um") - 0.05),
    ("p08", "#cartao-ficha", ini("E ele lembra") - 0.05),
    ("p09", "i07", ini("Problema dois") - 0.05),
    ("p10", "i08", ini("Problema três") - 0.05),
    ("p11", "i09", ini("Seu Antônio. Mas") - 0.05),
    ("p12", "i10", pal("Ele saiu do hotel", "E") - 0.05),
    ("p13", "#cartao-regra", ini("Regra número um") - 0.05),
    ("p14", "i11", ini("O que a gente faz") - 0.05),
    ("p15", "i12", ini("Opção B") - 0.05),
    ("p16", "i02", ini("Ou tem um terceiro") - 0.05),
    ("p17", "#fecho", ini("A maioria escreve") - 0.05),
]
PLANOS[0] = ("p01", "i01", 0.0)
fim = [p[2] for p in PLANOS[1:]] + [DUR]

js, els = [], []
for n, ((pid, alvo, t0), t1) in enumerate(zip(PLANOS, fim)):
    d = round(t1 - t0, 3)
    if alvo.startswith("#"):
        continue  # cartões são escritos abaixo com o mesmo tempo
    src = imagem(alvo)
    if src.endswith(".svg") and alvo in cenas.CENAS:
        # sem ilustração do Gemini: usa a cena desenhada e animada (tools/cenas.py)
        els.append(f'      <div id="{pid}" class="clip plano" data-start="{round(t0, 3)}" data-duration="{d}" data-track-index="1"><div id="{pid}-img" class="palco">{cenas.CENAS[alvo]()}</div></div>')
        js += cenas.anim(alvo, pid, round(t0, 3), round(t1, 3), pal)
    else:
        els.append(f'      <div id="{pid}" class="clip plano" data-start="{round(t0, 3)}" data-duration="{d}" data-track-index="1"><img id="{pid}-img" src="{src}" alt=""></div>')
    # Ken Burns: alterna aproximar/afastar e o lado do deslize
    a, b = (1.0, 1.09) if n % 2 == 0 else (1.1, 1.02)
    x = 22 if n % 3 == 0 else -22
    js.append(f'tl.fromTo("#{pid}-img", {{ scale: {a}, x: {-x / 2} }}, {{ scale: {b}, x: {x / 2}, duration: {d}, ease: "none", immediateRender: false }}, {round(t0, 3)});')
tempo = {p[1]: (p[2], f) for p, f in zip(PLANOS, fim) if p[1].startswith("#")}

# ---------------------------------------------------------------- painel
t_40 = ini("Quarenta")
RISCO = [(pal("E ele lembra", "tudo"), 25), (pal("Problema dois", "motorista"), 45), (pal("Problema três", "Antônio"), 60), (pal("Ele saiu do hotel", "velho"), 85)]
js.append('tl.set("#hud-risco-barra", { scaleX: 0 }, 0);')
js.append(f'tl.fromTo("#hud-mala", {{ scale: 1.18, color: "#ffd23a" }}, {{ scale: 1, color: "#ffffff", duration: 0.6, ease: "power2.out", immediateRender: false }}, {t_40 + 0.3});')
antes = 0
for tt, v in RISCO:
    js.append(f'tl.to("#hud-risco-n", {{ textContent: {v}, snap: {{ textContent: 1 }}, duration: 0.5, ease: "power1.out" }}, {tt});')
    js.append(f'tl.to("#hud-risco-barra", {{ scaleX: {v / 100}, duration: 0.5, ease: "power1.out" }}, {tt});')
    js.append(f'tl.fromTo("#hud-delta", {{ opacity: 1, y: 0 }}, {{ opacity: 0, y: -14, duration: 1.1, ease: "power1.in", immediateRender: false, onStart: () => {{}} }}, {tt});')
    js.append(f'tl.set("#hud-delta", {{ textContent: "+{v - antes}%" }}, {tt});')
    antes = v
# painel some nos cartões pretos e volta nas imagens
for alvo in ("#cartao-dono", "#cartao-ficha", "#cartao-regra"):
    a, b = tempo[alvo]
    js.append(f'tl.to("#hud-in", {{ opacity: 0, duration: 0.15 }}, {a}); tl.to("#hud-in", {{ opacity: 1, duration: 0.15 }}, {b});')

# ---------------------------------------------------------------- etiquetas de problema e carimbos
TAGS = [("tag-1", "PROBLEMA 1 · O PASSAGEIRO", ini("Problema um"), tempo["#cartao-ficha"][0]),
        ("tag-2", "PROBLEMA 2 · A CENTRAL", ini("Problema dois"), ini("Problema três")),
        ("tag-3", "PROBLEMA 3 · O VERSO", ini("Problema três"), ini("Seu Antônio. Mas"))]
CARIMBOS = [("car-lembra", "ELE LEMBRA", pal("E ele lembra", "tocando") + 0.3, tempo["#cartao-ficha"][1], 1180, -7),
            ("car-registrada", "REGISTRADA", pal("Problema dois", "motorista") + 0.1, ini("Problema três"), 1470, 6),
            ("car-nome", "TEM NOME", pal("Problema três", "Antônio") + 0.05, ini("Seu Antônio. Mas"), 1470, -6)]
for cid, _, t0, _, _, rot in CARIMBOS:
    js.append(f'tl.fromTo("#{cid} span", {{ scale: 2.4, opacity: 0, rotation: {rot} }}, {{ scale: 1, opacity: 1, rotation: {rot}, duration: 0.22, ease: "power4.in" }}, {round(t0, 3)});')
for tid, _, t0, _ in TAGS:
    js.append(f'tl.fromTo("#{tid} span", {{ x: -40, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.3, ease: "power3.out" }}, {round(t0, 3)});')

# ---------------------------------------------------------------- cartões
a, b = tempo["#cartao-dono"]
js += [f'tl.fromTo("#dono-1", {{ y: 40, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.35, ease: "power3.out" }}, {a + 0.1});',
       f'tl.fromTo("#dono-2", {{ scale: 1.6, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.25, ease: "power4.in" }}, {pal("Agora vem", "dono") - 0.05});']
a, b = tempo["#cartao-ficha"]
FICHA = [("ficha-1", pal("E ele lembra", "branco")), ("ficha-2", pal("E ele lembra", "sete")), ("ficha-3", pal("E ele lembra", "tocando"))]
js.append(f'tl.fromTo("#ficha-topo", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3 }}, {a + 0.05});')
for fid, tt in FICHA:
    js.append(f'tl.fromTo("#{fid}", {{ x: -60, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.25, ease: "power3.out" }}, {round(tt - 0.15, 3)});')
a, b = tempo["#cartao-regra"]
js += [f'tl.fromTo("#regra-1", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3 }}, {a + 0.05});',
       f'tl.fromTo("#regra-2", {{ y: 30, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.35, ease: "power3.out" }}, {pal("Regra número um", "todo") - 0.1});',
       f'tl.fromTo("#regra-3", {{ y: 30, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.35, ease: "power3.out" }}, {pal("Regra número um", "Quem") - 0.1});']
a, b = tempo["#fecho"]
js += [f'tl.fromTo("#fecho-1", {{ y: 30, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.4, ease: "power3.out" }}, {a + 0.05});',
       f'tl.fromTo("#fecho-2 .bt", {{ scale: 0.4, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.35, ease: "back.out(2.5)", stagger: 0.25 }}, {a + 0.3});',
       f'tl.fromTo("#fecho-3", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.4 }}, {a + 0.9});',
       f'tl.fromTo("#fecho-4", {{ scale: 0.5, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.45, ease: "back.out(2)" }}, {a + 1.4});']

# selos das opções e círculo do 3º jeito
t_acel, t_esp = pal("O que a gente faz", "ACELERA"), pal("Opção B", "ESPERA")
js += [f'tl.fromTo("#selo-acelera", {{ scale: 0.4, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.35, ease: "back.out(2.5)" }}, {t_acel});',
       f'tl.fromTo("#selo-espera", {{ scale: 0.4, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.35, ease: "back.out(2.5)" }}, {t_esp});']
t_circ = pal("Ou tem um terceiro", "escondido")
js.append(f'tl.fromTo("#circulo", {{ scale: 1.8, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.45, ease: "back.out(2)" }}, {t_circ});')

# ---------------------------------------------------------------- legendas palavra por palavra
DESTAQUE = {"clovis", "bilhete", "seis", "quarenta", "milhoes", "dono", "passageiro", "tudo", "central", "motorista", "antonio",
            "velho", "donos", "acelera", "espera", "terceiro", "escondido", "amanha", "nenhum"}
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
        caps.append((f"cap-{k}-{j}", round(a, 3), round(max(b - a, 0.2), 3), html))
cap_els = "\n".join(f'        <div id="{cid}" class="clip cap" data-start="{a}" data-duration="{d}" data-track-index="0"><span>{h}</span></div>' for cid, a, d, h in caps)

# ---------------------------------------------------------------- som
SFX = []
for n, ((pid, alvo, t0), t1) in enumerate(zip(PLANOS, fim)):
    if n and not alvo.startswith("#") and n % 2 == 0:
        SFX.append((f"wh-{pid}", "whoosh-short", t0 - 0.13, 0.57, 0.28))
for alvo in ("#cartao-dono", "#cartao-regra"):
    SFX.append((f"imp-{alvo[1:]}", "impact-bass-1", tempo[alvo][0] - 0.04, 2.0, 0.75))
for cid, _, t0, _, _, _ in CARIMBOS:
    SFX.append((f"car-{cid}", "impact-bass-2", t0 + 0.22 - 1.95, 2.5, 0.5))
for fid, tt in FICHA:
    SFX.append((f"clk-{fid}", "click-soft", tt - 0.19, 0.36, 0.8))
# abertura: o táxi chegando e a porta batendo quando o passageiro desce
SFX += [("chegada", "whoosh", 0.0, 0.8, 0.45), ("porta", "impact-bass-2", min(2.3, ini("Quando olhou") * 0.33) + 0.9 - 1.95, 2.5, 0.25)]
SFX += [("virada", "glitch-3", pal("Seu Antônio. Mas", "nenhum") - 0.05, 0.6, 0.35),
        ("selo-a", "pop", t_acel - 0.09, 0.7, 0.6), ("selo-b", "pop", t_esp - 0.09, 0.7, 0.6),
        ("circulo", "sparkle", t_circ, 1.8, 0.55), ("fecho", "impact-bass-1", tempo["#fecho"][0] + 1.4 - 0.04, 2.0, 0.55)]
sfx = "\n".join(f'      <audio id="sfx-{i}" class="clip" src="assets/audio/{f}.mp3" data-start="{round(max(0, s), 3)}" data-duration="{d}" data-track-index="{30 + n}" data-volume="{v}"></audio>' for n, (i, f, s, d, v) in enumerate(SFX))


def cl(alvo):
    a, b = tempo[alvo]
    return f'data-start="{round(a, 3)}" data-duration="{round(b - a, 3)}"'


tags = "\n".join(f'      <div id="{i}" class="clip tag" data-start="{round(a, 3)}" data-duration="{round(b - a, 3)}" data-track-index="6"><span>{t}</span></div>' for i, t, a, b in TAGS)
carimbos = "\n".join(f'      <div id="{i}" class="clip carimbo" style="top: {top}px" data-start="{round(a, 3)}" data-duration="{round(b - a, 3)}" data-track-index="7"><span>{t}</span></div>' for i, t, a, b, top, _ in CARIMBOS)
cx, cy, cr = CIRCULO
fecho_ini = tempo["#fecho"][0]

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
      .plano img {{ width: 100%; height: 100%; object-fit: cover; display: block; }}
      .palco, .palco svg {{ width: 1080px; height: 1920px; display: block; }}
      .cartao {{ position: absolute; inset: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; padding: 0 90px; }}
      .preto {{ background: #1c1a17; color: #fff; }}
      .creme {{ background: #efe9df; color: #1c1a17; }}
      .kick {{ font-family: "JetBrains Mono", monospace; font-weight: 700; font-size: 30px; letter-spacing: .18em; opacity: .7; margin-bottom: 40px; }}
      .grande {{ font-family: "Archivo Black", sans-serif; font-size: 118px; line-height: 1.02; }}
      .amarelo {{ color: #ffd23a; }}
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
      #hud-mala {{ display: inline-block; transform-origin: left center; }}
      /* etiqueta e carimbos */
      .tag {{ position: absolute; left: 36px; top: 330px; }}
      .tag span {{ display: inline-block; font-family: "JetBrains Mono", monospace; font-weight: 700; font-size: 30px; letter-spacing: .12em; color: #111; background: #ffd23a; padding: 6px 16px; border-radius: 8px; }}
      .carimbo {{ position: absolute; left: 0; right: 0; text-align: center; }}
      .carimbo span {{ display: inline-block; font-family: "Archivo Black", sans-serif; font-size: 96px; color: #ff3b30; border: 10px solid #ff3b30; border-radius: 16px; padding: 4px 30px; background: rgba(255,255,255,.1); }}
      .creme .carimbo span {{ background: transparent; }}
      /* ficha */
      .ficha-linha {{ font-family: "Archivo Black", sans-serif; font-size: 82px; line-height: 1.25; }}
      .ficha-linha i {{ font-style: normal; font-family: "JetBrains Mono", monospace; font-size: 40px; display: block; opacity: .55; letter-spacing: .1em; }}
      /* regra */
      .riscadas {{ font-family: "JetBrains Mono", monospace; font-size: 26px; color: #6d6a64; text-decoration: line-through; margin-bottom: 20px; }}
      #regra-2 {{ font-family: "Archivo Black", sans-serif; font-size: 84px; line-height: 1.1; }}
      #regra-3 {{ font-family: "Archivo Black", sans-serif; font-size: 72px; line-height: 1.12; color: #ffd23a; margin-top: 24px; }}
      /* legendas */
      .cap {{ position: absolute; left: 0; right: 0; top: 1300px; text-align: center; padding: 0 60px; }}
      .cap span {{ display: inline-block; font-family: "Archivo Black", sans-serif; font-size: 68px; line-height: 1.12; color: #fff; -webkit-text-stroke: 3px #000; paint-order: stroke fill; text-shadow: 0 6px 0 #000, 0 10px 24px rgba(0,0,0,.6); }}
      .dest {{ color: #ffd23a; }}
      /* selos, círculo, fecho */
      .selo {{ position: absolute; left: 0; right: 0; top: 420px; text-align: center; }}
      .selo span {{ display: inline-block; font-family: "Archivo Black", sans-serif; font-size: 96px; padding: 14px 50px; border-radius: 24px; border: 7px solid #000; box-shadow: 0 12px 0 #000; color: #111; }}
      #circulo {{ position: absolute; left: {cx - cr}px; top: {cy - cr}px; width: {2 * cr}px; height: {2 * cr}px; border: 14px solid #ffd23a; border-radius: 50%; box-shadow: 0 0 0 6px rgba(0,0,0,.5), 0 0 40px rgba(255,210,58,.6); }}
      .fecho {{ position: absolute; left: 0; right: 0; text-align: center; color: #fff; }}
      #fecho-1 {{ top: 520px; font-size: 66px; font-weight: 800; }}
      #fecho-2 {{ top: 640px; display: flex; justify-content: center; gap: 26px; }}
      #fecho-2 .bt {{ font-family: "Archivo Black", sans-serif; font-size: 70px; padding: 12px 34px; border-radius: 20px; border: 6px solid #000; box-shadow: 0 10px 0 #000; color: #111; }}
      #fecho-3 {{ top: 830px; font-size: 42px; color: #cfd3d8; line-height: 1.3; }}
      #fecho-4 {{ top: 960px; font-family: "Archivo Black", sans-serif; font-size: 124px; line-height: 1; color: #ffd23a; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-width="1080" data-height="1920">
{chr(10).join(els)}
      <div id="cartao-dono" class="clip cartao preto" {cl("#cartao-dono")} data-track-index="2">
        <div class="kick">PARTE 1 · O BILHETE</div>
        <div class="grande" id="dono-1">TODO PRÊMIO</div>
        <div class="grande amarelo" id="dono-2">TEM DONO</div>
      </div>
      <div id="cartao-ficha" class="clip cartao creme" {cl("#cartao-ficha")} data-track-index="2">
        <div class="kick" id="ficha-topo">PROBLEMA 1 · O QUE ELE LEMBRA</div>
        <div class="ficha-linha" id="ficha-1"><i>CARRO</i>TÁXI BRANCO</div>
        <div class="ficha-linha" id="ficha-2"><i>PLACA</i>FINAL 7</div>
        <div class="ficha-linha" id="ficha-3"><i>RÁDIO</i>98,1 FM</div>
      </div>
      <div id="cartao-regra" class="clip cartao preto" {cl("#cartao-regra")} data-track-index="2">
        <div class="kick" id="regra-1">O CÓDIGO DA MADRUGADA · REGRA 1</div>
        <div id="regra-2">Todo bilhete tem dois donos.</div>
        <div id="regra-3">Quem comprou… e quem tá com ele.</div>
      </div>
      <div id="fecho" class="clip cartao preto" {cl("#fecho")} data-track-index="2"></div>
{tags}
{carimbos}
      <div id="selo-acelera" class="clip selo" data-start="{round(t_acel - 0.05, 3)}" data-duration="{round(ini("Opção B") - 0.05 - t_acel + 0.05, 3)}" data-track-index="8"><span style="background:#fff">ACELERA</span></div>
      <div id="selo-espera" class="clip selo" data-start="{round(t_esp - 0.05, 3)}" data-duration="{round(ini("Ou tem um terceiro") - t_esp, 3)}" data-track-index="9"><span style="background:#ffd23a">ESPERA</span></div>
      <div id="circulo" class="clip" data-start="{round(t_circ - 0.05, 3)}" data-duration="{round(fecho_ini - t_circ, 3)}" data-track-index="10"></div>
      <div id="hud" class="clip" data-start="0" data-duration="{round(fecho_ini, 3)}" data-track-index="3">
        <div id="hud-in">
          <div class="caixa" id="cx-mala"><small>NO BANCO DE TRÁS</small><b><span id="hud-mala">R$ 40.000.000</span></b></div>
          <div class="caixa" id="cx-bolso"><small>NO BOLSO</small><b>R$ 0</b></div>
          <div class="caixa" id="cx-risco"><small>RISCO</small><b><span id="hud-risco-n">0</span>%</b><div class="barra"><div id="hud-risco-barra"></div></div><div id="hud-delta">+0%</div></div>
        </div>
      </div>
      <div id="legendas" class="clip" data-start="0" data-duration="{round(T["total"] + 0.3, 3)}" data-track-index="4" data-track-kind="captions" style="position:absolute;inset:0">
{cap_els}
      </div>
      <div id="fecho-1" class="clip fecho" data-start="{round(fecho_ini, 3)}" data-duration="{round(DUR - fecho_ini, 3)}" data-track-index="11">Comente <span class="amarelo">uma</span> palavra</div>
      <div id="fecho-2" class="clip fecho" data-start="{round(fecho_ini, 3)}" data-duration="{round(DUR - fecho_ini, 3)}" data-track-index="12"><span class="bt" style="background:#fff">ACELERA</span><span class="bt" style="background:#ffd23a">ESPERA</span></div>
      <div id="fecho-3" class="clip fecho" data-start="{round(fecho_ini, 3)}" data-duration="{round(DUR - fecho_ini, 3)}" data-track-index="13">ou ache o 3º jeito escondido<br>(só vale se disser qual é)</div>
      <div id="fecho-4" class="clip fecho" data-start="{round(fecho_ini, 3)}" data-duration="{round(DUR - fecho_ini, 3)}" data-track-index="14">PARTE 2<br>AMANHÃ</div>
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
faltam = [n for n in CENAS if imagem(n).endswith(".svg")]
print("ok", len(caps), "legendas ·", DUR, "s · cenas desenhadas (sem ilustração do Gemini):", " ".join(faltam) or "nenhuma")
