"""Gera index.html do episódio 05 (macaco na selva) a partir de build/timing.json.

Mundo em SVG (2200x1920) estilo HQ: contorno preto grosso, cores chapadas, sombras chapadas.
A câmera é o grupo #mundo (x, y, scale) animado pelo GSAP; os planos são cortes secos.
Uso (na pasta do episódio): python3 tools/narracao.py && python3 tools/montar.py
"""
import json
import random

T = json.load(open("build/timing.json"))
F = T["frases"]
DUR = 30.0
random.seed(5)
OUT = 'stroke="#14100c" stroke-width="7" stroke-linejoin="round" stroke-linecap="round"'

# ---------------------------------------------------------------- mundo SVG
def folhagem(n, y0, y1, cores, rmin, rmax, contorno=False):
    s = []
    for _ in range(n):
        x = random.uniform(-100, 2300); y = random.uniform(y0, y1); r = random.uniform(rmin, rmax)
        c = random.choice(cores)
        s.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r:.0f}" fill="{c}" {OUT if contorno else ""}/>')
    return "\n".join(s)


def folhas_grandes(n, regioes):
    s = []
    for _ in range(n):
        x0, x1, y0, y1 = random.choice(regioes)
        x = random.uniform(x0, x1); y = random.uniform(y0, y1); a = random.uniform(-60, 60); k = random.uniform(0.8, 1.4)
        c = random.choice(["#2f8a3a", "#3aa046", "#26732f"])
        s.append(f'<g transform="translate({x:.0f} {y:.0f}) rotate({a:.0f}) scale({k:.2f})"><path d="M0 0 C 40 -60 120 -60 170 0 C 120 50 40 50 0 0 Z" fill="{c}" {OUT}/><path d="M10 0 L 160 0" stroke="#1b5a24" stroke-width="5" fill="none"/></g>')
    return "\n".join(s)


banana = "\n".join(
    f'<path transform="translate({1560 + i * 22} {880 + abs(i - 2) * 10}) rotate({-30 + i * 15})" d="M0 0 C -12 60 10 120 60 150 C 30 110 22 60 26 0 Z" fill="#ffd23a" {OUT}/>'
    for i in range(5)
)

pedras = []
for i, (x, rx) in enumerate([(820, 85), (990, 70), (1185, 92), (1390, 80)]):
    if i == 2:  # a "pedra" que é crocodilo
        pedras.append(f'''<g id="pedra-croc">
  <ellipse cx="{x}" cy="1565" rx="{rx + 20}" ry="42" fill="#5f7d57" {OUT}/>
  <ellipse cx="{x - 30}" cy="1540" rx="26" ry="18" fill="#6c8c62" {OUT}/>
  <g id="olho-pedra"><ellipse cx="{x - 30}" cy="1538" rx="15" ry="11" fill="#ffd23a" stroke="#14100c" stroke-width="4"/><rect x="{x - 33}" y="1528" width="6" height="20" rx="3" fill="#14100c"/></g>
  <ellipse id="palpebra-pedra" cx="{x - 30}" cy="1538" rx="19" ry="14" fill="#6c8c62" stroke="#14100c" stroke-width="4"/>
  <circle cx="{x + 70}" cy="1552" r="6" fill="#14100c"/><circle cx="{x + 88}" cy="1556" r="6" fill="#14100c"/>
</g>''')
    else:
        pedras.append(f'<g><ellipse cx="{x}" cy="1570" rx="{rx}" ry="40" fill="#8a9592" {OUT}/><ellipse cx="{x - 20}" cy="1555" rx="{rx * 0.45:.0f}" ry="10" fill="#b7c0bc"/></g>')

macaco = '''<g id="macaco">
  <path d="M-40 60 C -120 140 -60 260 20 240 C 70 228 60 180 30 190" fill="none" stroke="#14100c" stroke-width="30" stroke-linecap="round"/>
  <path d="M-40 60 C -120 140 -60 260 20 240 C 70 228 60 180 30 190" fill="none" stroke="#8a5530" stroke-width="18" stroke-linecap="round"/>
  <path d="M-40 70 L -55 150 M 40 70 L 55 150" stroke="#14100c" stroke-width="34" stroke-linecap="round"/>
  <path d="M-40 70 L -55 150 M 40 70 L 55 150" stroke="#8a5530" stroke-width="22" stroke-linecap="round"/>
  <ellipse cx="0" cy="20" rx="72" ry="88" fill="#8a5530" ''' + OUT + '''/>
  <ellipse cx="0" cy="35" rx="44" ry="58" fill="#e8c08a"/>
  <g id="braco-d"><path d="M-55 -20 C -100 0 -110 40 -95 60" fill="none" stroke="#14100c" stroke-width="32" stroke-linecap="round"/><path d="M-55 -20 C -100 0 -110 40 -95 60" fill="none" stroke="#8a5530" stroke-width="20" stroke-linecap="round"/></g>
  <g id="braco-e"><path d="M55 -20 C 100 0 110 40 95 60" fill="none" stroke="#14100c" stroke-width="32" stroke-linecap="round"/><path d="M55 -20 C 100 0 110 40 95 60" fill="none" stroke="#8a5530" stroke-width="20" stroke-linecap="round"/></g>
  <g id="cabeca">
    <circle cx="-80" cy="-125" r="30" fill="#8a5530" ''' + OUT + '''/><circle cx="-80" cy="-125" r="15" fill="#e8b38a"/>
    <circle cx="80" cy="-125" r="30" fill="#8a5530" ''' + OUT + '''/><circle cx="80" cy="-125" r="15" fill="#e8b38a"/>
    <circle cx="0" cy="-125" r="82" fill="#8a5530" ''' + OUT + '''/>
    <path d="M-62 -140 C -62 -185 -10 -190 0 -160 C 10 -190 62 -185 62 -140 C 70 -90 40 -60 0 -62 C -40 -60 -70 -90 -62 -140 Z" fill="#e8c08a" ''' + OUT + '''/>
    <g id="olhos">
      <ellipse cx="-27" cy="-140" rx="18" ry="22" fill="#fff" stroke="#14100c" stroke-width="4"/>
      <ellipse cx="27" cy="-140" rx="18" ry="22" fill="#fff" stroke="#14100c" stroke-width="4"/>
      <g id="pupilas"><circle id="pup-e" cx="-24" cy="-138" r="10" fill="#14100c"/><circle id="pup-d" cx="30" cy="-138" r="10" fill="#14100c"/>
        <circle cx="-21" cy="-142" r="3.5" fill="#fff"/><circle cx="33" cy="-142" r="3.5" fill="#fff"/></g>
      <rect id="palp-e" x="-47" y="-164" width="40" height="24" fill="#e8c08a" stroke="#14100c" stroke-width="4"/>
      <rect id="palp-d" x="7" y="-164" width="40" height="24" fill="#e8c08a" stroke="#14100c" stroke-width="4"/>
    </g>
    <path id="sobr-e" d="M-45 -172 Q -27 -182 -10 -172" fill="none" stroke="#14100c" stroke-width="7"/>
    <path id="sobr-d" d="M10 -172 Q 27 -182 45 -172" fill="none" stroke="#14100c" stroke-width="7"/>
    <circle cx="-7" cy="-105" r="4" fill="#14100c"/><circle cx="7" cy="-105" r="4" fill="#14100c"/>
    <path id="boca-riso" d="M-30 -88 Q 0 -58 30 -88 Z" fill="#7a1f1f" stroke="#14100c" stroke-width="5"/>
    <ellipse id="boca-o" cx="0" cy="-80" rx="13" ry="17" fill="#3a0d0d" stroke="#14100c" stroke-width="5" opacity="0"/>
    <path id="boca-medo" d="M-26 -80 Q -13 -90 0 -80 Q 13 -70 26 -80" fill="none" stroke="#14100c" stroke-width="6" opacity="0"/>
  </g>
</g>'''

raios = "\n".join(f'<polygon points="{x},0 {x + 140},0 {x + 520},1900 {x + 260},1900" fill="#eaffb5" opacity="0.07"/>' for x in (300, 900, 1500))
ondas = "\n".join(f'<path d="M{x} {y} q 30 -12 60 0" fill="none" stroke="#bff3ff" stroke-width="5" opacity="0.35" stroke-linecap="round"/>' for x, y in [(random.uniform(640, 1560), random.uniform(1380, 1880)) for _ in range(40)])
juncos = "\n".join(f'<path d="M{x} 1900 Q {x + random.uniform(-25, 25):.0f} {1820 - h / 2:.0f} {x + random.uniform(-40, 40):.0f} {1900 - h:.0f}" fill="none" stroke="#14100c" stroke-width="16" stroke-linecap="round"/><path d="M{x} 1900 Q {x:.0f} {1820 - h / 2:.0f} {x + 10:.0f} {1900 - h:.0f}" fill="none" stroke="#4fa646" stroke-width="9" stroke-linecap="round"/>'
                 for x, h in [(random.uniform(1500, 1720), random.uniform(150, 260)) for _ in range(28)])

mundo = f'''
<defs>
  <linearGradient id="g-ceu" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0b3326"/><stop offset="0.55" stop-color="#1c6b43"/><stop offset="1" stop-color="#2d8a50"/></linearGradient>
  <linearGradient id="g-rio" gradientUnits="userSpaceOnUse" x1="0" y1="1330" x2="0" y2="2150"><stop offset="0" stop-color="#156a6e"/><stop offset="1" stop-color="#0a343b"/></linearGradient>
  <radialGradient id="g-brilho"><stop offset="0" stop-color="#fff3a0" stop-opacity="0.9"/><stop offset="1" stop-color="#ffd23a" stop-opacity="0"/></radialGradient>
</defs>
<rect x="-400" y="-600" width="3000" height="4200" fill="url(#g-ceu)"/>
{folhagem(40, -150, 700, ["#0f3d2a", "#124632"], 90, 200)}
{raios}
{folhagem(30, 500, 1250, ["#185c38", "#1b6a40"], 70, 150)}
<!-- margens -->
<path d="M-200 1330 L 640 1330 C 700 1500 640 1700 700 2150 L -200 2150 Z" fill="#4a3220" {OUT}/>
<path d="M-200 1330 L 640 1330 L 650 1360 L -200 1365 Z" fill="#3e9a44" {OUT}/>
<path d="M1580 1330 L 2400 1330 L 2400 2150 L 1540 2150 C 1600 1700 1540 1500 1580 1330 Z" fill="#4a3220" {OUT}/>
<path d="M1578 1330 L 2400 1330 L 2400 1365 L 1572 1360 Z" fill="#3e9a44" {OUT}/>
<!-- rio -->
<path d="M640 1330 L 1580 1330 C 1540 1500 1600 1700 1540 2150 L 700 2150 C 640 1700 700 1500 640 1330 Z" fill="url(#g-rio)" {OUT}/>
{ondas}
<!-- tronco escondido nos juncos (o 3º jeito) -->
<g id="tronco"><rect x="1330" y="1770" width="330" height="58" rx="29" fill="#7a5233" {OUT}/><circle cx="1360" cy="1799" r="22" fill="#b9875a" {OUT}/><path d="M1400 1786 L 1620 1786 M 1420 1812 L 1600 1812" stroke="#5a3a22" stroke-width="5"/></g>
{juncos}
{"".join(pedras)}
<!-- crocodilo (olhos saindo da água) -->
<g id="croc">
  <path d="M960 1465 C 1000 1425 1180 1425 1230 1462 Z" fill="#4d7a3a" {OUT}/>
  <g id="croc-olhos"><ellipse cx="1010" cy="1440" rx="30" ry="24" fill="#4d7a3a" {OUT}/><ellipse cx="1080" cy="1440" rx="30" ry="24" fill="#4d7a3a" {OUT}/>
  <ellipse cx="1010" cy="1438" rx="16" ry="12" fill="#ffd23a" stroke="#14100c" stroke-width="4"/><rect x="1007" y="1427" width="6" height="22" rx="3" fill="#14100c"/>
  <ellipse cx="1080" cy="1438" rx="16" ry="12" fill="#ffd23a" stroke="#14100c" stroke-width="4"/><rect x="1077" y="1427" width="6" height="22" rx="3" fill="#14100c"/></g>
  <circle cx="1200" cy="1448" r="6" fill="#14100c"/><circle cx="1216" cy="1450" r="6" fill="#14100c"/>
  <rect x="930" y="1462" width="330" height="60" fill="url(#g-rio)"/>
</g>
<!-- árvore da esquerda e galho do macaco -->
<path d="M60 -200 L 330 -200 L 350 1340 L 40 1340 Z" fill="#5a3a22" {OUT}/>
<path d="M120 0 L 140 1300 M 250 100 L 270 1250" stroke="#3e2615" stroke-width="10"/>
<path d="M320 980 C 450 960 620 950 780 930 L 785 975 C 620 995 450 1010 330 1030 Z" fill="#6a4529" {OUT}/>
<!-- árvore da direita e cacho de banana -->
<path d="M1870 -200 L 2140 -200 L 2160 1340 L 1850 1340 Z" fill="#5a3a22" {OUT}/>
<path d="M1880 840 C 1760 830 1640 820 1520 800 L 1515 845 C 1640 862 1760 875 1875 890 Z" fill="#6a4529" {OUT}/>
<circle id="brilho-banana" cx="1610" cy="960" r="200" fill="url(#g-brilho)"/>
<path d="M1600 845 L 1610 890" stroke="#14100c" stroke-width="14"/>
<g id="banana">{banana}</g>
<!-- cipó atravessando o rio -->
<g id="cipo">
  <path d="M700 260 C 900 1180 1300 1150 1525 815" fill="none" stroke="#14100c" stroke-width="34" stroke-linecap="round"/>
  <path d="M700 260 C 900 1180 1300 1150 1525 815" fill="none" stroke="#4f8a2e" stroke-width="20" stroke-linecap="round"/>
  {folhas_grandes(9, [(760, 1300, 500, 1000)])}
  <g id="racha" opacity="0"><path d="M1085 1030 l 18 -22 l 6 26 l 20 -20 l 4 24" fill="none" stroke="#f3e3b5" stroke-width="7" stroke-linecap="round"/><path d="M1080 1050 l -20 18 M1140 1040 l 24 14" stroke="#f3e3b5" stroke-width="5"/></g>
</g>
{folhas_grandes(26, [(-150, 2350, -150, 250), (-150, 300, 300, 1300), (1950, 2350, 300, 1300)])}
<!-- mato em primeiro plano (preenche a parte de baixo nos planos abertos) -->
<rect x="-400" y="2100" width="3000" height="1500" fill="#0d2e1d"/>
{folhagem(60, 2020, 2300, ['#1d5c33', '#226b3b', '#184f2c'], 90, 170, contorno=True)}
{folhagem(50, 2300, 3300, ['#123d26', '#0f3421'], 120, 220)}
<g id="macaco-wrap" transform="translate(560 860)">{macaco}</g>
<circle id="circulo" cx="1500" cy="1800" r="150" fill="none" stroke="#ffd23a" stroke-width="14" opacity="0"/>
'''

# ---------------------------------------------------------------- câmera (planos)
def cam(fx, fy, s):
    return {"x": round(540 - fx * s, 1), "y": round(900 - fy * s, 1), "scale": s}

ini = {x["texto"]: x["ini"] for x in F}
PLANOS = [  # (t0, de, para, ease)
    (0.0, cam(560, 980, 0.95), cam(1500, 960, 0.95), "power2.inOut", 5.2),
    (5.2, cam(1500, 960, 0.95), cam(1110, 1380, 0.78), "power2.inOut", 7.2),
    (7.2, cam(1100, 1440, 1.9), cam(1100, 1440, 2.15), "none", 8.7),
    (8.7, cam(560, 760, 3.2), cam(560, 760, 3.45), "none", 9.86),
    (9.86, cam(1120, 1000, 1.7), cam(1120, 1010, 1.95), "none", 13.69),
    (13.69, cam(1090, 1565, 1.85), cam(1170, 1550, 2.6), "power2.inOut", 18.29),
    (18.29, cam(1100, 1000, 0.49), cam(1100, 1000, 0.5), "none", 24.0),
    (24.0, cam(1100, 1000, 0.5), cam(1100, 1000, 0.52), "none", DUR),
]
js = []
for t0, de, para, ez, t1 in PLANOS:
    js.append(f'tl.fromTo("#mundo", {json.dumps(de)}, {{ ...{json.dumps(para)}, duration: {round(t1 - t0, 3)}, ease: "{ez}", immediateRender: false }}, {t0});')
js.insert(0, 'gsap.set("#mundo", { svgOrigin: "0 0" });')

# ---------------------------------------------------------------- personagem e cena
js += [
    # expressões do macaco: feliz olhando a banana → susto → medo → desconfiado → sorriso
    'tl.set("#pupilas", { x: 6 }, 0);',
    'tl.fromTo("#palp-e,#palp-d", { scaleY: 0.25, transformOrigin: "50% 0%" }, { scaleY: 0.25, duration: 0.01 }, 0);',
    'tl.fromTo("#cabeca", { rotation: 0, svgOrigin: "0 -60" }, { rotation: 6, duration: 1.2, ease: "sine.inOut", yoyo: true, repeat: 3 }, 0);',
    f'tl.set("#boca-riso", {{ opacity: 0 }}, {ini["O rio tem crocodilo."] + 0.6}); tl.set("#boca-o", {{ opacity: 1 }}, {ini["O rio tem crocodilo."] + 0.6});',
    f'tl.to("#palp-e,#palp-d", {{ scaleY: 0.01, duration: 0.12 }}, {ini["O rio tem crocodilo."] + 0.6});',
    f'tl.to("#pupilas", {{ x: 0, scale: 0.7, svgOrigin: "3 -140", duration: 0.12 }}, {ini["O rio tem crocodilo."] + 0.6});',
    f'tl.to("#sobr-e", {{ y: -10, rotation: -12, svgOrigin: "-27 -175", duration: 0.12 }}, {ini["O rio tem crocodilo."] + 0.6});',
    f'tl.to("#sobr-d", {{ y: -10, rotation: 12, svgOrigin: "27 -175", duration: 0.12 }}, {ini["O rio tem crocodilo."] + 0.6});',
    f'tl.fromTo("#macaco", {{ y: 0 }}, {{ y: -14, duration: 0.08, yoyo: true, repeat: 5 }}, {ini["O rio tem crocodilo."] + 1.5});',
    # croc sobe
    f'tl.fromTo("#croc-olhos", {{ y: 55 }}, {{ y: 0, duration: 1.1, ease: "power2.out" }}, {ini["O rio tem crocodilo."]});',
    # racha no cipó
    f'tl.fromTo("#racha", {{ opacity: 0, scale: 0.4, svgOrigin: "1110 1035" }}, {{ opacity: 1, scale: 1, duration: 0.25, ease: "back.out(3)" }}, {ini["Mas ele tá rachando."] + 0.5});',
    f'tl.fromTo("#cipo", {{ y: 0 }}, {{ y: 6, duration: 0.06, yoyo: true, repeat: 7 }}, {ini["Mas ele tá rachando."] + 0.5});',
    # a pedra pisca
    f'tl.fromTo("#palpebra-pedra", {{ scaleY: 1, svgOrigin: "1155 1526" }}, {{ scaleY: 0.05, duration: 0.15 }}, {ini["Só que uma delas... piscou."] + 1.2});',
    f'tl.to("#palpebra-pedra", {{ scaleY: 1, duration: 0.15 }}, {ini["Só que uma delas... piscou."] + 1.75});',
    # macaco volta a sorrir nos planos abertos (escolha)
    'tl.set("#boca-o", { opacity: 0 }, 18.29); tl.set("#boca-riso", { opacity: 1 }, 18.29);',
    'tl.set("#palp-e,#palp-d", { scaleY: 0.25 }, 18.29); tl.set("#pupilas", { x: 6, scale: 1 }, 18.29);',
    'tl.set("#sobr-e,#sobr-d", { y: 0, rotation: 0 }, 18.29);',
    # banana brilha, ondas
    'tl.fromTo("#brilho-banana", { opacity: 0.5 }, { opacity: 1, duration: 1.5, yoyo: true, repeat: 19, ease: "sine.inOut" }, 0);',
    # círculo no tronco escondido
    f'tl.fromTo("#circulo", {{ opacity: 0, scale: 1.6, svgOrigin: "1500 1800" }}, {{ opacity: 1, scale: 1, duration: 0.45, ease: "back.out(2)" }}, {ini["E tem um terceiro jeito escondido nessa imagem."] + 1.4});',
]

# ---------------------------------------------------------------- painel (HUD)
perigo = [(0, 0), (ini["O rio tem crocodilo."] + 0.6, 40), (ini["Mas ele tá rachando."] + 0.5, 65), (ini["Só que uma delas... piscou."] + 1.2, 90)]
js.append('tl.set("#hud-perigo-barra", { scaleX: 0 }, 0);')
for t, v in perigo[1:]:
    js.append(f'tl.to("#hud-perigo-n", {{ textContent: {v}, snap: {{ textContent: 1 }}, duration: 0.5, ease: "power1.out" }}, {t});')
    js.append(f'tl.to("#hud-perigo-barra", {{ scaleX: {v / 100}, duration: 0.5, ease: "power1.out" }}, {t});')
    js.append(f'tl.fromTo("#hud-perigo", {{ scale: 1.12 }}, {{ scale: 1, duration: 0.35, ease: "power2.out", immediateRender: false }}, {t});')
js.append(f'tl.to("#hud-energia-n", {{ textContent: 72, snap: {{ textContent: 1 }}, duration: 10, ease: "none" }}, 2);')

# ---------------------------------------------------------------- legendas (palavra por palavra, 2–3 palavras)
DESTAQUE = {"macaco.", "banana", "rio.", "crocodilo.", "cipó.", "rachando.", "pedras.", "piscou.", "CIPÓ", "PEDRA.", "terceiro", "escondido", "amanhã."}
caps = []
for k, fr in enumerate(F):
    ws = fr["texto"].split()
    grupos, g = [], []
    for w in ws:
        g.append(w)
        if len(g) == 3 or w.endswith((".", ":", "?")):
            grupos.append(g); g = []
    if g:
        grupos.append(g)
    tot = sum(len(" ".join(x)) for x in grupos)
    t = fr["ini"]
    for j, g in enumerate(grupos):
        d = (fr["fim"] - fr["ini"]) * len(" ".join(g)) / tot
        a, b = t - (0.06 if j == 0 else 0), t + d + (0.12 if j == len(grupos) - 1 else 0)
        html = " ".join(f'<b class="dest">{w}</b>' if w in DESTAQUE else w for w in g)
        caps.append((f"cap-{k}-{j}", round(a, 3), round(b - a, 3), html))
        t += d

# ---------------------------------------------------------------- carimbos, escolha, fecho
CAR = [("car-racha", "RACHANDO", ini["Mas ele tá rachando."] + 0.55, 13.69, 620, -8),
       ("car-piscou", "UMA PISCOU", ini["Só que uma delas... piscou."] + 1.25, 18.29, 620, 7)]
for cid, _, t0, _, _, rot in CAR:
    js.append(f'tl.fromTo("#{cid} span", {{ scale: 2.4, opacity: 0, rotation: {rot} }}, {{ scale: 1, opacity: 1, rotation: {rot}, duration: 0.22, ease: "power4.in" }}, {t0});')
t_opc = ini["Comente CIPÓ ou PEDRA."]
js += [
    f'tl.fromTo("#opc-cipo", {{ scale: 0.4, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.35, ease: "back.out(2.5)" }}, {t_opc + 0.25});',
    f'tl.fromTo("#opc-pedra", {{ scale: 0.4, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.35, ease: "back.out(2.5)" }}, {t_opc + 1.1});',
    'tl.fromTo("#escurece", { opacity: 0 }, { opacity: 0.72, duration: 0.4 }, 24.0);',
    'tl.fromTo("#fecho-1", { y: 30, opacity: 0 }, { y: 0, opacity: 1, duration: 0.4, ease: "power3.out" }, 24.1);',
    'tl.fromTo("#fecho-2 .bt", { scale: 0.4, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.35, ease: "back.out(2.5)", stagger: 0.25 }, 24.35);',
    'tl.fromTo("#fecho-3", { opacity: 0 }, { opacity: 1, duration: 0.4 }, 25.0);',
    'tl.fromTo("#fecho-4", { scale: 0.5, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.45, ease: "back.out(2)" }, 25.6);',
]

els = []
for cid, a, d, html in caps:
    baixo = ' style="top: 1520px"' if a >= 18.2 else ''
    els.append(f'        <div id="{cid}" class="clip cap"{baixo} data-start="{a}" data-duration="{d}" data-track-index="0"><span>{html}</span></div>')
carimbos = "\n".join(f'      <div id="{cid}" class="clip carimbo" style="top: {top}px" data-start="{round(t0, 3)}" data-duration="{round(t1 - t0, 3)}" data-track-index="5"><span>{txt}</span></div>' for cid, txt, t0, t1, top, _ in CAR)

SFX = [  # id, arquivo, início (pico 1 quadro depois da imagem), duração, volume
    ("whoosh-1", "whoosh-short", 7.2 - 0.13, 0.57, 0.55), ("whoosh-2", "whoosh-short", 9.86 - 0.13, 0.57, 0.45),
    ("whoosh-3", "whoosh-short", 13.69 - 0.13, 0.57, 0.5), ("whoosh-4", "whoosh", 18.29 - 0.2, 0.57, 0.45),
    ("croc", "impact-bass-1", ini["O rio tem crocodilo."] + 0.6 - 0.04, 2.0, 0.9),
    ("racha", "glitch-3", ini["Mas ele tá rachando."] + 0.5, 0.6, 0.5),
    ("carimbo-1", "impact-bass-2", ini["Mas ele tá rachando."] + 0.55 + 0.22 - 1.95, 2.5, 0.55),
    ("pisca", "click-soft", ini["Só que uma delas... piscou."] + 1.2 - 0.04, 0.36, 0.9),
    ("carimbo-2", "impact-bass-1", ini["Só que uma delas... piscou."] + 1.25 + 0.22 - 0.04, 2.0, 0.8),
    ("opc-1", "pop", t_opc + 0.25 - 0.09, 0.7, 0.7), ("opc-2", "pop", t_opc + 1.1 - 0.09, 0.7, 0.7),
    ("circulo", "sparkle", ini["E tem um terceiro jeito escondido nessa imagem."] + 1.4, 1.8, 0.6),
    ("fecho", "impact-bass-1", 25.6 - 0.04, 2.0, 0.6),
]
sfx = "\n".join(f'      <audio id="sfx-{i}" class="clip" src="assets/audio/{f}.mp3" data-start="{round(max(0, s), 3)}" data-duration="{d}" data-track-index="{20 + n}" data-volume="{v}"></audio>' for n, (i, f, s, d, v) in enumerate(SFX))

page = f'''<!doctype html>
<html lang="pt-BR">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="assets/lib/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: #0b2a1f; }}
      #root {{ position: relative; width: 100%; height: 100%; font-family: "Inter", sans-serif; }}
      #cena {{ position: absolute; inset: 0; }}
      #cena svg {{ width: 1080px; height: 1920px; display: block; }}
      #legendas {{ position: absolute; inset: 0; }}
      #escurece {{ position: absolute; inset: 0; background: #07120d; }}
      /* painel de jogo */
      #hud {{ position: absolute; left: 40px; right: 40px; top: 190px; display: flex; gap: 14px; }}
      .caixa {{ flex: 1; background: rgba(10, 14, 12, 0.82); border: 3px solid rgba(255, 255, 255, 0.18); border-radius: 18px; padding: 12px 16px; color: #fff; }}
      .caixa small {{ display: block; font-size: 28px; font-weight: 700; letter-spacing: 0.12em; color: #a9b8ae; }}
      .caixa b {{ display: block; font-family: "Archivo Black", sans-serif; font-size: 40px; line-height: 1.1; }}
      #hud-perigo b {{ color: #ff5a4a; }}
      .barra {{ height: 8px; background: rgba(255,255,255,0.15); border-radius: 4px; margin-top: 6px; overflow: hidden; }}
      #hud-perigo-barra {{ height: 100%; width: 100%; background: #ff5a4a; transform-origin: left center; }}
      /* legendas */
      .cap {{ position: absolute; left: 0; right: 0; top: 1190px; text-align: center; padding: 0 60px; }}
      .cap span {{ display: inline-block; font-family: "Archivo Black", sans-serif; font-size: 70px; line-height: 1.12; color: #fff;
                  -webkit-text-stroke: 3px #000; paint-order: stroke fill; text-shadow: 0 6px 0 #000, 0 10px 24px rgba(0,0,0,0.6); }}
      .dest {{ color: #ffd23a; }}
      /* carimbos */
      .carimbo {{ position: absolute; left: 0; right: 0; text-align: center; }}
      .carimbo span {{ display: inline-block; font-family: "Archivo Black", sans-serif; font-size: 92px; color: #ff3b30; border: 10px solid #ff3b30;
                      border-radius: 16px; padding: 4px 30px; background: rgba(255, 255, 255, 0.08); text-shadow: 0 0 1px #000; }}
      /* escolha */
      .opc {{ position: absolute; top: 470px; font-family: "Archivo Black", sans-serif; font-size: 84px; padding: 14px 42px; border-radius: 22px;
              border: 6px solid #000; box-shadow: 0 10px 0 #000; }}
      #opc-cipo {{ left: 90px; background: #fff; color: #111; }}
      #opc-pedra {{ right: 90px; background: #ffd23a; color: #111; }}
      /* fecho */
      .fecho {{ position: absolute; left: 0; right: 0; text-align: center; color: #fff; }}
      #fecho-1 {{ top: 470px; font-size: 66px; font-weight: 900; }}
      #fecho-2 {{ top: 590px; display: flex; justify-content: center; gap: 28px; }}
      #fecho-2 .bt {{ font-family: "Archivo Black", sans-serif; font-size: 76px; padding: 12px 40px; border-radius: 20px; border: 6px solid #000; box-shadow: 0 10px 0 #000; }}
      #fecho-3 {{ top: 780px; font-size: 46px; color: #cfd8d2; }}
      #fecho-4 {{ top: 880px; font-family: "Archivo Black", sans-serif; font-size: 120px; line-height: 1; color: #ffd23a; -webkit-text-stroke: 4px #000; paint-order: stroke fill; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-width="1080" data-height="1920">
      <div id="cena" class="clip" data-start="0" data-duration="{DUR}" data-track-index="1" data-layout-allow-overflow data-layout-ignore>
        <svg viewBox="0 0 1080 1920" xmlns="http://www.w3.org/2000/svg"><g id="mundo">{mundo}</g></svg>
      </div>
      <div id="escurece" class="clip" data-start="24.0" data-duration="{round(DUR - 24.0, 2)}" data-track-index="2" data-layout-ignore></div>
      <div id="hud" class="clip" data-start="0" data-duration="24.0" data-track-index="3">
        <div class="caixa"><small>BANANAS</small><b>0</b></div>
        <div class="caixa"><small>ENERGIA</small><b><span id="hud-energia-n">100</span>%</b></div>
        <div class="caixa" id="hud-perigo"><small>PERIGO</small><b><span id="hud-perigo-n">0</span>%</b><div class="barra"><div id="hud-perigo-barra"></div></div></div>
      </div>
      <div id="legendas" class="clip" data-start="0" data-duration="26.2" data-track-index="4" data-track-kind="captions">
{chr(10).join(els)}
      </div>
{carimbos}
      <div id="opc-cipo" class="clip opc" data-start="{round(t_opc, 3)}" data-duration="{round(24.0 - t_opc, 3)}" data-track-index="6">CIPÓ</div>
      <div id="opc-pedra" class="clip opc" data-start="{round(t_opc, 3)}" data-duration="{round(24.0 - t_opc, 3)}" data-track-index="7">PEDRA</div>
      <div id="fecho-1" class="clip fecho" data-start="24.0" data-duration="{round(DUR - 24, 2)}" data-track-index="8">Comente uma palavra</div>
      <div id="fecho-2" class="clip fecho" data-start="24.0" data-duration="{round(DUR - 24, 2)}" data-track-index="9"><span class="bt" style="background:#fff;color:#111">CIPÓ</span><span class="bt" style="background:#ffd23a;color:#111">PEDRA</span></div>
      <div id="fecho-3" class="clip fecho" data-start="24.0" data-duration="{round(DUR - 24, 2)}" data-track-index="10">ou ache o 3º jeito escondido</div>
      <div id="fecho-4" class="clip fecho" data-start="24.0" data-duration="{round(DUR - 24, 2)}" data-track-index="11">PARTE 2<br>AMANHÃ</div>
      <audio id="narracao" class="clip" src="assets/audio/narracao.mp3" data-start="0" data-duration="{T['total']:.2f}" data-track-index="12" data-volume="1"></audio>
      <audio id="trilha" class="clip" src="assets/audio/trilha.mp3" data-start="0" data-duration="{DUR}" data-track-index="13" data-volume="0.5"></audio>
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
print("ok", len(caps), "legendas")
