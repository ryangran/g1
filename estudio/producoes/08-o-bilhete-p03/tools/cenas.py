"""Cenas desenhadas em SVG para "O Bilhete · Parte 1" (estilo HQ noturno, contorno grosso).

Cada função devolve o SVG 1080×1920 da cena. Os grupos com id são animados em montar.py (ANIM).
Personagens seguem docs/BIBLIA.md: Clóvis (camisa azul-clara, bigode grisalho, têmporas grisalhas,
terço no retrovisor) e o homem de terno azul-marinho com relógio dourado.
"""
import random

K = "#120f0c"                       # tinta do contorno
O = f'stroke="{K}" stroke-width="7" stroke-linejoin="round" stroke-linecap="round"'
O4 = f'stroke="{K}" stroke-width="4" stroke-linejoin="round" stroke-linecap="round"'
PELE_C, PELE_C2 = "#c98b5e", "#a96e45"       # Clóvis
CAMISA, CAMISA2 = "#9cc9ec", "#6f9fc8"
BIGODE = "#9a958f"
PELE_H, PELE_H2 = "#e2b48f", "#c08d69"       # homem de terno
TERNO, TERNO2 = "#24324f", "#172036"
OURO = "#f2c14e"
BILHETE = "#f5e7a1"


def svg(corpo, defs=""):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1920" width="1080" height="1920" preserveAspectRatio="xMidYMid slice" overflow="visible">
<defs>
<radialGradient id="vinheta" cx="50%" cy="48%" r="70%"><stop offset="0.55" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity="0.7"/></radialGradient>
<linearGradient id="noite" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#070b14"/><stop offset="1" stop-color="#16233a"/></linearGradient>
<radialGradient id="poste" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#ffb661" stop-opacity="0.85"/><stop offset="1" stop-color="#ffb661" stop-opacity="0"/></radialGradient>
<radialGradient id="verde" cx="50%" cy="100%" r="80%"><stop offset="0" stop-color="#38e08a" stop-opacity="0.55"/><stop offset="1" stop-color="#38e08a" stop-opacity="0"/></radialGradient>
<radialGradient id="vermelho" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#ff3b30" stop-opacity="0.6"/><stop offset="1" stop-color="#ff3b30" stop-opacity="0"/></radialGradient>
{defs}
</defs>
{corpo}
<rect width="1080" height="1920" fill="url(#vinheta)" pointer-events="none"/>
</svg>'''


def chuva(cid, n=70, seed=1, cor="#9fc4ff", op=0.35):
    r = random.Random(seed)
    riscos = "".join(f'<path d="M{r.uniform(-100, 1180):.0f} {r.uniform(-400, 1920):.0f} l -14 60" stroke="{cor}" stroke-width="{r.choice((2, 3, 3, 4))}" opacity="{op}"/>' for _ in range(n))
    return f'<g id="{cid}">{riscos}<g transform="translate(0 -2320)">{riscos}</g></g>'


def gotas(cid, area, n=30, seed=2):
    x0, y0, x1, y1 = area
    r = random.Random(seed)
    s = []
    for i in range(n):
        x, y, rr = r.uniform(x0, x1), r.uniform(y0, y1), r.uniform(5, 13)
        s.append(f'<g class="gota"><ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{rr:.1f}" ry="{rr * 1.25:.1f}" fill="#cfe3ff" opacity="0.35"/><circle cx="{x - rr / 3:.0f}" cy="{y - rr / 3:.0f}" r="{rr / 3.5:.1f}" fill="#fff" opacity="0.7"/></g>')
    return f'<g id="{cid}">{"".join(s)}</g>'


def taxi_lado(x, y, s=1.0, cid="taxi", cabeca=""):
    """Sedã branco de perfil, frente para a esquerda (igual à folha: luminoso vermelho, adesivo verde na porta)."""
    roda = lambda n, cx: f'<g id="{cid}-roda{n}"><circle cx="{cx}" cy="215" r="58" fill="#1b1d22" {O}/><circle cx="{cx}" cy="215" r="28" fill="#9aa3ad" {O4}/><path d="M{cx - 26} 215 h52 M{cx} 189 v52" stroke="#5d646d" stroke-width="7"/></g>'
    return f'''<g id="{cid}" transform="translate({x} {y}) scale({s})">
  <ellipse cx="330" cy="268" rx="350" ry="24" fill="#000" opacity="0.5"/>
  <polygon id="{cid}-farol" points="10,150 -420,90 -420,300 10,190" fill="#ffe7a8" opacity="0.18"/>
  <clipPath id="{cid}-vidro"><path d="M215 100 C 245 55 285 45 345 45 L 350 100 Z"/></clipPath>
  <path d="M215 100 C 245 55 285 45 345 45 L 350 100 Z" fill="#1b2a40"/>
  <g clip-path="url(#{cid}-vidro)">{cabeca}</g>
  <path d="M10 170 C 10 120 40 110 90 105 L 190 100 C 230 40 280 25 360 25 L 470 25 C 520 25 560 60 590 105 L 620 110 C 650 115 660 140 660 175 L 660 215 L 10 215 Z M215 100 C 245 55 285 45 345 45 L 350 100 Z M370 45 L 460 45 C 500 45 530 70 555 100 L 370 100 Z" fill="#eef1f4" fill-rule="evenodd" {O}/>
  <path d="M370 45 L 460 45 C 500 45 530 70 555 100 L 370 100 Z" fill="#1b2a40" {O4}/>
  <path d="M215 100 L 560 100 M360 100 L 362 200" stroke="{K}" stroke-width="5"/>
  <path d="M230 60 L 260 52" stroke="#fff" stroke-width="6" opacity="0.35"/>
  <rect x="300" y="-8" width="120" height="34" rx="6" fill="#e23b2e" {O4}/>
  <text x="360" y="18" font-family="Archivo Black, sans-serif" font-size="24" fill="#fff" text-anchor="middle">TÁXI</text>
  <g transform="translate(250 125)"><rect x="0" y="0" width="56" height="38" fill="#fff" {O4}/><rect x="0" y="0" width="56" height="14" fill="#2fae6a"/><rect x="0" y="26" width="56" height="12" fill="#e23b2e"/></g>
  <path d="M10 160 L 60 160" stroke="#ffd98a" stroke-width="16" stroke-linecap="round"/>
  <rect x="628" y="150" width="30" height="20" rx="4" fill="#e23b2e" {O4}/>
  <circle id="{cid}-freio" cx="650" cy="160" r="70" fill="url(#vermelho)" opacity="0"/>
  <path d="M30 185 L 640 185" stroke="#c9cfd6" stroke-width="6"/>
  <path d="M60 130 C 120 128 160 140 200 170" stroke="#b9c0c8" stroke-width="4" fill="none" opacity="0.7"/>
  {roda(1, 150)}{roda(2, 520)}
</g>'''


def clovis_cabeca(ids="c", sorriso=False):
    """Cabeça do Clóvis de frente (folha docs/clovis-folha.jpg): rosto largo e redondo, papada, cabelo preto curto
    com as laterais grisalhas, sobrancelhas grossas, olheiras, nariz largo e bigode grisalho bem grosso."""
    return f'''<g id="{ids}-cabeca">
  <path d="M-152 -30 C -170 -45 -182 -5 -172 30 C -164 58 -146 62 -136 46 Z" fill="{PELE_C}" {O}/>
  <path d="M152 -30 C 170 -45 182 -5 172 30 C 164 58 146 62 136 46 Z" fill="{PELE_C}" {O}/>
  <path d="M-146 -70 C -152 -180 152 -180 146 -70 C 162 10 156 95 118 140 C 82 182 -82 182 -118 140 C -156 95 -162 10 -146 -70 Z" fill="{PELE_C}" {O}/>
  <path d="M10 175 C 70 168 120 130 140 50 C 150 110 120 160 80 172 C 50 180 30 178 10 175 Z" fill="{PELE_C2}" opacity="0.55"/>
  <path d="M-150 -62 C -166 -176 -72 -220 8 -210 C 98 -212 170 -168 150 -62 C 142 -112 112 -138 72 -144 C 22 -154 -40 -152 -92 -138 C -126 -126 -143 -98 -150 -62 Z" fill="#1c1a1a" {O}/>
  <path d="M-150 -62 C -154 -100 -142 -126 -116 -136 L -100 -30 C -122 -36 -140 -46 -150 -62 Z" fill="#a9a6a2" {O4}/>
  <path d="M150 -62 C 154 -100 142 -126 116 -136 L 100 -30 C 122 -36 140 -46 150 -62 Z" fill="#a9a6a2" {O4}/>
  <path d="M-58 -108 Q 0 -118 58 -108 M-44 -92 Q 0 -100 44 -92" fill="none" stroke="{PELE_C2}" stroke-width="5" stroke-linecap="round"/>
  <path id="{ids}-sobr-e" d="M-110 -60 Q -74 -80 -30 -64" fill="none" stroke="{K}" stroke-width="17" stroke-linecap="round"/>
  <path id="{ids}-sobr-d" d="M30 -64 Q 74 -80 110 -60" fill="none" stroke="{K}" stroke-width="17" stroke-linecap="round"/>
  <g id="{ids}-olhos">
    <ellipse cx="-64" cy="-30" rx="26" ry="18" fill="#fff" {O4}/><ellipse cx="64" cy="-30" rx="26" ry="18" fill="#fff" {O4}/>
    <g id="{ids}-pupilas"><circle cx="-61" cy="-29" r="10" fill="#2a1a10"/><circle cx="67" cy="-29" r="10" fill="#2a1a10"/>
      <circle cx="-58" cy="-32" r="3.5" fill="#fff"/><circle cx="70" cy="-32" r="3.5" fill="#fff"/></g>
    <rect id="{ids}-palp-e" x="-94" y="-52" width="60" height="22" fill="{PELE_C}" {O4}/>
    <rect id="{ids}-palp-d" x="34" y="-52" width="60" height="22" fill="{PELE_C}" {O4}/>
  </g>
  <path d="M-92 -4 Q -64 8 -38 -2 M38 -2 Q 64 8 92 -4 M-86 8 Q -64 16 -44 10 M44 10 Q 64 16 86 8" fill="none" stroke="{PELE_C2}" stroke-width="5" stroke-linecap="round"/>
  <path d="M-12 -24 C -16 6 -40 28 -32 50 C -22 66 22 66 32 50 C 40 28 16 6 12 -24" fill="{PELE_C}" {O}/>
  <path d="M-22 52 Q -14 46 -6 54 M6 54 Q 14 46 22 52" fill="none" stroke="{K}" stroke-width="4"/>
  <path d="M-74 40 C -96 70 -96 110 -76 140 M74 40 C 96 70 96 110 76 140" fill="none" stroke="{PELE_C2}" stroke-width="5" stroke-linecap="round"/>
  <g id="{ids}-boca">{'<path d="M-36 120 Q 0 142 36 120" fill="#5a1a14" '+O4+'/>' if sorriso else '<path d="M-30 124 Q 0 116 30 124" fill="none" stroke="'+K+'" stroke-width="6" stroke-linecap="round"/>'}</g>
  <ellipse id="{ids}-boca-o" cx="0" cy="126" rx="18" ry="20" fill="#3a0c0a" {O4} opacity="0"/>
  <path d="M-104 100 C -92 58 -34 50 0 66 C 34 50 92 58 104 100 C 94 110 76 112 60 104 C 40 94 20 92 0 98 C -20 92 -40 94 -60 104 C -76 112 -94 110 -104 100 Z" fill="{BIGODE}" {O}/>
  <path d="M-74 74 L -66 92 M-50 66 L -44 88 M-24 64 L -20 86 M24 64 L 20 86 M50 66 L 44 88 M74 74 L 66 92" stroke="#77736e" stroke-width="4" stroke-linecap="round"/>
  <path d="M-62 160 Q 0 182 62 160" fill="none" stroke="{PELE_C2}" stroke-width="5" stroke-linecap="round"/>
</g>'''


def clovis_busto(x, y, s=1.0, ids="c"):
    """Busto do Clóvis: ombros largos, pescoço grosso, camisa azul-clara de gola aberta com caneta no bolso."""
    return f'''<g id="{ids}" transform="translate({x} {y}) scale({s})">
  <path d="M-310 560 C -310 340 -230 255 -86 236 L 86 236 C 230 255 310 340 310 560 Z" fill="{CAMISA}" {O}/>
  <path d="M-200 320 C -170 420 -170 500 -190 560 M200 320 C 170 420 170 500 190 560" fill="none" stroke="{CAMISA2}" stroke-width="6"/>
  <path d="M-62 236 L 0 320 L 62 236 L 50 180 L -50 180 Z" fill="{PELE_C}" {O}/>
  <path d="M-86 236 L -24 300 L -62 345 L -128 262 Z M86 236 L 24 300 L 62 345 L 128 262 Z" fill="#cfe4f6" {O4}/>
  <rect x="110" y="360" width="96" height="76" fill="{CAMISA2}" {O4}/>
  <rect x="140" y="318" width="15" height="76" rx="5" fill="#1f4d9e" {O4}/>
  <path d="M0 320 L 0 560" stroke="{CAMISA2}" stroke-width="6"/>
  <circle cx="-12" cy="400" r="7" fill="#fff" {O4}/><circle cx="-12" cy="480" r="7" fill="#fff" {O4}/>
  {clovis_cabeca(ids)}
</g>'''


def homem_busto(x, y, s=1.0, ids="h", telefone=True):
    return f'''<g id="{ids}" transform="translate({x} {y}) scale({s})">
  <path d="M-260 520 C -260 330 -190 255 -70 235 L 70 235 C 190 255 260 330 260 520 Z" fill="{TERNO}" {O}/>
  <path d="M-70 235 L 0 360 L 70 235 L 40 205 L -40 205 Z" fill="#f4f4f2" {O}/>
  <path d="M-70 235 L -10 360 L -100 520 L -150 300 Z M70 235 L 10 360 L 100 520 L 150 300 Z" fill="{TERNO2}" {O4}/>
  <path d="M-38 165 L -38 235 L 38 235 L 38 165 Z" fill="{PELE_H}" {O}/>
  <g id="{ids}-cabeca">
    <path d="M-125 -50 C -135 -175 135 -175 125 -50 C 132 60 100 140 0 155 C -100 140 -132 60 -125 -50 Z" fill="{PELE_H}" {O}/>
    <path d="M-20 150 C 50 140 105 90 118 20 C 125 90 95 140 0 155 Z" fill="{PELE_H2}" opacity="0.55"/>
    <path d="M-130 -40 C -150 -170 -40 -210 20 -200 C 110 -195 160 -150 130 -40 C 120 -110 60 -150 -10 -150 C -70 -148 -110 -110 -130 -40 Z" fill="#0d0d10" {O}/>
    <path d="M-60 -170 C -20 -185 40 -185 80 -165 M -40 -150 C 0 -165 50 -160 90 -140" fill="none" stroke="#3a3d48" stroke-width="5"/>
    <path id="{ids}-sobr-e" d="M-92 -50 L -26 -40" stroke="{K}" stroke-width="12" stroke-linecap="round"/>
    <path id="{ids}-sobr-d" d="M26 -40 L 92 -50" stroke="{K}" stroke-width="12" stroke-linecap="round"/>
    <g id="{ids}-olhos"><path d="M-88 -16 Q -58 -36 -28 -16 Q -58 -4 -88 -16 Z" fill="#fff" {O4}/><path d="M28 -16 Q 58 -36 88 -16 Q 58 -4 28 -16 Z" fill="#fff" {O4}/>
      <circle cx="-56" cy="-18" r="9" fill="#101010"/><circle cx="60" cy="-18" r="9" fill="#101010"/></g>
    <path d="M-4 -10 C -10 30 -24 46 -12 54 C 0 58 10 56 18 52" fill="none" stroke="{K}" stroke-width="6" stroke-linecap="round"/>
    <path id="{ids}-boca" d="M-40 96 Q 10 112 48 88" fill="none" stroke="{K}" stroke-width="7" stroke-linecap="round"/>
  </g>
  {f'<g id="{ids}-tel"><path d="M150 40 C 150 -20 175 -40 205 -40 L 225 -40 L 225 160 L 205 160 C 175 160 150 140 150 100 Z" fill="{PELE_H}" {O}/><rect x="110" y="-60" width="70" height="150" rx="16" fill="#1a1a1e" {O}/><rect x="182" y="150" width="70" height="40" rx="8" fill="{OURO}" {O4}/></g>' if telefone else ''}
</g>'''


def homem_corpo(x, y, s=1.0, ids="hc", tel=False):
    """Homem de terno de corpo inteiro, de pé (perfil 3/4)."""
    return f'''<g id="{ids}"><g transform="translate({x} {y}) scale({s})">
  <ellipse cx="0" cy="600" rx="110" ry="18" fill="#000" opacity="0.5"/>
  <g id="{ids}-perna-e"><path d="M-35 300 L -55 590 L -10 590 L 5 310 Z" fill="{TERNO2}" {O}/><path d="M-60 585 L 0 585 L 5 605 L -70 605 Z" fill="#0b0b0d" {O4}/></g>
  <g id="{ids}-perna-d"><path d="M10 300 L 30 590 L 75 590 L 50 300 Z" fill="{TERNO2}" {O}/><path d="M25 585 L 85 585 L 90 605 L 20 605 Z" fill="#0b0b0d" {O4}/></g>
  <path d="M-85 70 C -95 180 -80 260 -60 320 L 70 320 C 90 260 100 180 85 70 C 60 45 -60 45 -85 70 Z" fill="{TERNO}" {O}/>
  <path d="M-25 60 L 0 140 L 25 60 Z" fill="#f4f4f2" {O4}/>
  <g id="{ids}-braco-e"><path d="M-80 80 C -110 150 -110 220 -95 280" fill="none" stroke="{K}" stroke-width="40" stroke-linecap="round"/><path d="M-80 80 C -110 150 -110 220 -95 280" fill="none" stroke="{TERNO}" stroke-width="27" stroke-linecap="round"/><circle cx="-95" cy="290" r="18" fill="{PELE_H}" {O4}/></g>
  {f'<g id="{ids}-braco-d"><path d="M80 80 C 120 120 120 40 70 -10" fill="none" stroke="{K}" stroke-width="40" stroke-linecap="round"/><path d="M80 80 C 120 120 120 40 70 -10" fill="none" stroke="{TERNO}" stroke-width="27" stroke-linecap="round"/><rect x="40" y="-60" width="34" height="62" rx="8" fill="#1a1a1e" {O4}/><rect x="80" y="20" width="30" height="18" rx="4" fill="{OURO}" {O4}/></g>' if tel else f'<g id="{ids}-braco-d"><path d="M80 80 C 110 150 110 220 95 280" fill="none" stroke="{K}" stroke-width="40" stroke-linecap="round"/><path d="M80 80 C 110 150 110 220 95 280" fill="none" stroke="{TERNO}" stroke-width="27" stroke-linecap="round"/><circle cx="95" cy="290" r="18" fill="{PELE_H}" {O4}/><rect x="80" y="250" width="30" height="16" rx="4" fill="{OURO}" {O4}/></g>'}
  <path d="M-22 20 L -22 60 L 22 60 L 22 20 Z" fill="{PELE_H}" {O4}/>
  <ellipse cx="0" cy="-20" rx="52" ry="60" fill="{PELE_H}" {O}/>
  <path d="M-55 -30 C -62 -95 40 -100 56 -40 C 40 -70 -20 -75 -55 -30 Z" fill="#0d0d10" {O4}/>
  <path d="M-25 -20 L -8 -18 M 10 -18 L 28 -20" stroke="{K}" stroke-width="6" stroke-linecap="round"/>
  <path d="M-14 22 Q 6 30 22 18" fill="none" stroke="{K}" stroke-width="5" stroke-linecap="round"/>
</g></g>
'''


def clovis_corpo(x, y, s=1.0, ids="cc"):
    """Clóvis de pé, gordinho (folha): barriga, manga curta, calça cinza-escura, sapato preto, relógio marrom.
    A mão direita (lado direito da tela) ergue o bilhete."""
    return f'''<g id="{ids}"><g transform="translate({x} {y}) scale({s})">
  <ellipse cx="0" cy="600" rx="130" ry="18" fill="#000" opacity="0.5"/>
  <path d="M-80 300 L -78 588 L -16 588 L -4 330 L 4 330 L 16 588 L 78 588 L 80 300 Z" fill="#4b4e57" {O}/>
  <path d="M-4 340 L 0 588" stroke="#36383f" stroke-width="5"/>
  <path d="M-86 584 L -12 584 L -8 606 L -94 606 Z M12 584 L 86 584 L 94 606 L 8 606 Z" fill="#17171a" {O4}/>
  <path d="M-108 74 C -140 150 -150 240 -112 312 L 112 312 C 150 240 140 150 108 74 C 76 46 -76 46 -108 74 Z" fill="{CAMISA}" {O}/>
  <path d="M-110 230 C -60 268 60 268 110 230" fill="none" stroke="{CAMISA2}" stroke-width="6"/>
  <path d="M-30 52 L 0 100 L 30 52 Z" fill="{PELE_C}" {O4}/><path d="M-40 52 L -6 92 L -26 108 L -56 66 Z M40 52 L 6 92 L 26 108 L 56 66 Z" fill="#cfe4f6" {O4}/>
  <rect x="32" y="120" width="42" height="36" fill="{CAMISA2}" {O4}/><rect x="44" y="102" width="8" height="40" rx="3" fill="#1f4d9e"/>
  <path d="M-112 300 L 112 300" stroke="#1c1c22" stroke-width="18"/>
  <path d="M-104 84 C -128 110 -136 140 -134 160" fill="none" stroke="{K}" stroke-width="48" stroke-linecap="round"/><path d="M-104 84 C -128 110 -136 140 -134 160" fill="none" stroke="{CAMISA}" stroke-width="35" stroke-linecap="round"/>
  <path d="M-134 168 C -138 210 -132 250 -124 278" fill="none" stroke="{K}" stroke-width="36" stroke-linecap="round"/><path d="M-134 168 C -138 210 -132 250 -124 278" fill="none" stroke="{PELE_C}" stroke-width="24" stroke-linecap="round"/>
  <circle cx="-122" cy="290" r="20" fill="{PELE_C}" {O4}/>
  <g id="{ids}-braco"><path d="M104 84 C 136 70 152 50 160 30" fill="none" stroke="{K}" stroke-width="48" stroke-linecap="round"/><path d="M104 84 C 136 70 152 50 160 30" fill="none" stroke="{CAMISA}" stroke-width="35" stroke-linecap="round"/>
    <path d="M162 22 C 170 -10 168 -40 160 -66" fill="none" stroke="{K}" stroke-width="36" stroke-linecap="round"/><path d="M162 22 C 170 -10 168 -40 160 -66" fill="none" stroke="{PELE_C}" stroke-width="24" stroke-linecap="round"/>
    <rect x="148" y="-48" width="30" height="16" rx="4" fill="#7a4a22" {O4}/>
    <g transform="translate(160 -112) rotate(-8)"><rect x="-44" y="-38" width="88" height="54" rx="4" fill="{BILHETE}" {O4}/><path d="M-30 -22 h60 M-30 -6 h44" stroke="#555" stroke-width="5"/></g>
    <circle cx="160" cy="-76" r="21" fill="{PELE_C}" {O4}/></g>
  <path d="M-34 24 L -34 62 L 34 62 L 34 24 Z" fill="{PELE_C}" {O4}/>
  <g transform="translate(0 -42) scale(0.38)">{clovis_cabeca(ids)}</g>
</g></g>
'''


def mao(x, y, rot=0, s=1.0, cid=""):
    """Mão estilizada segurando (polegar por cima)."""
    return f'''<g {f'id="{cid}"' if cid else ''} transform="translate({x} {y}) rotate({rot}) scale({s})">
  <path d="M-120 80 C -140 20 -110 -40 -40 -50 L 90 -60 C 120 -60 125 -30 100 -25 L 40 -20 L 120 -10 C 150 -5 150 25 120 28 L 50 30 L 110 45 C 135 52 130 80 105 80 L 45 75 L 90 92 C 110 100 100 125 80 122 L -20 120 C -70 120 -105 110 -120 80 Z" fill="{PELE_C}" {O}/>
  <path d="M-60 -40 C -20 -80 30 -95 70 -90 C 95 -86 95 -60 70 -58 C 30 -55 0 -45 -20 -30" fill="{PELE_C}" {O}/>
  <path d="M-170 140 L -110 40 L -40 130 Z" fill="{CAMISA}" {O}/>
</g>'''


def pose(nome, x, y, largura, cid="", noite=True):
    """Pose oficial do Clóvis (assets/clovis/, recortada das folhas em docs/). x, y = canto superior esquerdo."""
    from PIL import Image
    arq = f"assets/clovis/{nome}{'-noite' if noite else ''}.png"
    w, h = Image.open(arq).size
    alt = round(largura * h / w)
    return f'<g {f"id={chr(34)}{cid}{chr(34)}" if cid else ""}><image href="{arq}" x="{x}" y="{y}" width="{largura}" height="{alt}" preserveAspectRatio="none"/></g>'


# ================================================================ CENAS

def i01():
    """O táxi chega, freia em frente ao Hotel Imperial e o passageiro desce do lado da calçada (atrás do carro)
    e anda até a porta. Escala real: porta 2,4 m ≈ 310 px, pessoa 1,75 m ≈ 220 px, carro 4,5 m ≈ 560 px."""
    janelas = "".join(f'<rect x="{x}" y="{y}" width="74" height="96" fill="{c}" {O4}/>' for x in (110, 240, 370, 630, 760, 890) for y, c in ((330, "#ffcf7a" if x in (240, 630, 890) else "#3a4560"), (470, "#ffcf7a" if x in (110, 370, 760) else "#3a4560")))
    cabeca = f'<g id="clovis-janela">{pose("rosto-sorriso", 246, 40, 92)}</g>'
    return svg(f'''
<rect width="1080" height="1920" fill="url(#noite)"/>
<rect x="40" y="150" width="1000" height="1040" fill="#2c2433" {O}/>
<path d="M40 150 L 1040 150 L 1040 190 L 40 190 Z" fill="#1d1823"/>
{janelas}
<rect x="40" y="590" width="1000" height="34" fill="#1d1823" {O4}/>
<g id="neon-hotel"><rect x="230" y="640" width="620" height="96" rx="12" fill="#1a1018" {O4}/>
<text x="540" y="709" font-family="Archivo Black, sans-serif" font-size="64" fill="#ff5a7a" text-anchor="middle" letter-spacing="10">IMPERIAL</text></g>
<rect id="brilho-neon" x="180" y="600" width="720" height="180" fill="url(#vermelho)"/>
<path d="M560 790 L 940 790 L 990 880 L 510 880 Z" fill="#6b1d2c" {O}/>
<path d="M510 880 L 990 880 L 990 898 L 510 898 Z" fill="#4a1220" {O4}/>
<rect x="620" y="898" width="260" height="284" fill="#ffd27a" {O}/>
<path d="M750 898 L 750 1182 M620 960 L 880 960" stroke="{K}" stroke-width="6"/>
<rect x="636" y="976" width="100" height="196" fill="#ffe7b0" opacity="0.6"/><rect x="764" y="976" width="100" height="196" fill="#ffe7b0" opacity="0.6"/>
<g transform="translate(560 1090)"><rect x="-26" y="40" width="52" height="54" rx="6" fill="#5a3a22" {O4}/><circle cx="0" cy="20" r="44" fill="#2f7a46" {O4}/><circle cx="-24" cy="-6" r="26" fill="#3a9a56" {O4}/><circle cx="20" cy="-10" r="28" fill="#3a9a56" {O4}/></g>
<g id="porteiro" transform="translate(940 975)"><rect x="-30" y="56" width="60" height="150" rx="16" fill="#5a1626" {O}/><circle cx="0" cy="28" r="28" fill="#8a5a3c" {O4}/><rect x="-30" y="-4" width="60" height="16" fill="#2a0e14" {O4}/><path d="M-30 206 h26 M4 206 h26" stroke="{K}" stroke-width="8"/></g>
<rect x="0" y="1182" width="1080" height="80" fill="#3a3f49" {O4}/>
<path d="M0 1262 L 1080 1262" stroke="#5b616d" stroke-width="10"/>
<rect x="0" y="1268" width="1080" height="652" fill="#11161f"/>
<g opacity="0.55"><rect x="620" y="1270" width="260" height="420" fill="#ffd27a" opacity="0.16"/><rect x="230" y="1270" width="620" height="200" fill="#ff5a7a" opacity="0.08"/></g>
<path d="M0 1600 L 1080 1600" stroke="#e8e3c8" stroke-width="10" stroke-dasharray="90 70" opacity="0.6"/>
<rect x="260" y="1120" width="420" height="460" fill="url(#poste)" opacity="0.5"/>
<g id="passageiro">{homem_corpo(560, 1004, 0.33, "hc")}</g>
{taxi_lado(40, 1064, 0.85, "taxi", cabeca)}
{chuva("chuva", 90, 11)}
''')


def i02():
    return svg(f'''
<rect width="1080" height="1920" fill="#0c111b"/>
<path d="M60 160 L 1020 160 L 980 820 L 100 820 Z" fill="#1d3049" {O}/>
<circle id="poste-janela" cx="760" cy="380" r="260" fill="url(#poste)"/>
<circle cx="760" cy="380" r="40" fill="#ffe3b0"/>
{gotas("gotas", (110, 190, 970, 790), 40, 5)}
<path d="M60 820 L 1020 820" stroke="{K}" stroke-width="10"/>
<path d="M0 760 C 200 720 880 720 1080 760 L 1080 1500 L 0 1500 Z" fill="#5c6067" {O}/>
<path d="M0 780 C 200 745 880 745 1080 780 L 1080 900 C 880 870 200 870 0 900 Z" fill="#6e737b"/>
<path d="M360 760 L 340 1500 M720 760 L 740 1500" stroke="#4a4e55" stroke-width="10"/>
<path d="M0 1500 L 1080 1500 L 1080 2700 L 0 2700 Z" fill="#23262c" {O}/>
<path d="M120 1560 L 960 1560 L 1010 2100 L 70 2100 Z" fill="#2f333a" {O4}/>
<polygon points="300,820 980,820 1080,1500 520,1500" fill="#ffb661" opacity="0.12"/>
<g id="bilhete" transform="translate(560 1140) rotate(-14)">
  <rect x="-150" y="-80" width="300" height="160" rx="8" fill="{BILHETE}" {O}/>
  <rect x="-130" y="-62" width="260" height="30" fill="#e0c96a"/>
  {''.join(f'<circle cx="{-105 + i * 42}" cy="10" r="15" fill="none" stroke="#3b3b3b" stroke-width="4"/>' for i in range(6))}
  <path d="M-120 50 h240" stroke="#8b7f4a" stroke-width="5" stroke-dasharray="10 8"/>
</g>
<g id="brilho-bilhete"><path d="M560 1050 l 14 40 l 40 14 l -40 14 l -14 40 l -14 -40 l -40 -14 l 40 -14 Z" fill="#fff" opacity="0.9"/></g>
<g id="recibo" data-layout-ignore transform="translate(800 1690) rotate(-10)">
  <path d="M-150 -105 L 150 -112 L 156 100 L 120 92 L 90 104 L 60 92 L 30 104 L 0 92 L -30 104 L -60 92 L -90 104 L -120 92 L -146 100 Z" fill="#f1f0ea" {O4}/>
  <rect x="-132" y="-96" width="30" height="24" fill="#2fae6a"/><path d="M-123 -84 h12 M-117 -90 v12" stroke="#fff" stroke-width="4"/>
  <text x="-94" y="-76" font-family="Inter, sans-serif" font-weight="800" font-size="22" fill="#1d6b45">DROGARIA SÃO JORGE</text>
  <path d="M-132 -60 h264" stroke="#b7b6ae" stroke-width="2" stroke-dasharray="6 5"/>
  <text x="-132" y="-34" font-family="JetBrains Mono, monospace" font-weight="700" font-size="19" fill="#333">CLIENTE: ANTÔNIO S.</text>
  <text x="-132" y="0" font-family="JetBrains Mono, monospace" font-weight="700" font-size="19" fill="#333">R. DAS ACÁCIAS, 51</text>
  <text x="-132" y="34" font-family="JetBrains Mono, monospace" font-size="16" fill="#666">DIPIRONA 500MG</text><text x="132" y="34" font-family="JetBrains Mono, monospace" font-size="16" fill="#666" text-anchor="end">12,90</text>
  <text x="-132" y="64" font-family="JetBrains Mono, monospace" font-size="16" fill="#666">TOTAL</text><text x="132" y="64" font-family="JetBrains Mono, monospace" font-weight="700" font-size="16" fill="#333" text-anchor="end">R$ 12,90</text>
</g>
<circle id="circulo-sombra" cx="800" cy="1690" r="185" fill="none" stroke="#000" stroke-width="30" opacity="0"/>
<circle id="circulo-recibo" cx="800" cy="1690" r="185" fill="none" stroke="#ffd23a" stroke-width="16" opacity="0"/>

''')


def i03():
    nums = ["07", "13", "22", "31", "44", "58"]
    tela = "".join(f'<g id="num-{i}"><circle cx="{-150 + (i % 3) * 150}" cy="{-40 + (i // 3) * 150}" r="56" fill="#2fbf71" {O4}/><text x="{-150 + (i % 3) * 150}" y="{-22 + (i // 3) * 150}" font-family="Archivo Black, sans-serif" font-size="50" fill="#fff" text-anchor="middle">{n}</text></g>' for i, n in enumerate(nums))
    bil = "".join(f'<g><text x="{-160 + i * 64}" y="20" font-family="Archivo Black, sans-serif" font-size="42" fill="#2a2a2a" text-anchor="middle">{n}</text><circle id="risco-{i}" cx="{-160 + i * 64}" cy="5" r="30" fill="none" stroke="#e02f24" stroke-width="6"/></g>' for i, n in enumerate(nums))
    return svg(f'''
<rect width="1080" height="1920" fill="#0b0f16"/>
<circle cx="540" cy="760" r="620" fill="#173a5a" opacity="0.5"/>
<g id="celular" transform="translate(540 700)">
  <rect x="-260" y="-470" width="520" height="900" rx="60" fill="#121418" {O}/>
  <rect x="-230" y="-430" width="460" height="820" rx="36" fill="#0f2b22"/>
  <text x="0" y="-330" font-family="Inter, sans-serif" font-weight="800" font-size="40" fill="#bfe9d0" text-anchor="middle">RESULTADO</text>
  <text x="0" y="-275" font-family="Inter, sans-serif" font-size="30" fill="#7fbf9e" text-anchor="middle">concurso 2.817</text>
  <g transform="translate(0 -80)">{tela}</g>
  <text x="0" y="300" font-family="Archivo Black, sans-serif" font-size="56" fill="#ffd23a" text-anchor="middle">R$ 40 MILHÕES</text>
</g>
<rect x="0" y="0" width="1080" height="1920" fill="url(#verde)" opacity="0.5"/>
<g id="bilhete-mao" transform="translate(560 1420) rotate(-6)">
  <rect x="-240" y="-90" width="480" height="180" rx="10" fill="{BILHETE}" {O}/>
  <rect x="-220" y="-72" width="440" height="34" fill="#e0c96a"/>
  <g transform="translate(0 10)">{bil}</g>
</g>
{mao(300, 1500, -10, 1.1)}
''')


def i04():
    gotas_suor = "".join(f'<path id="suor-{i}" d="M{x} {y} c -10 18 -10 30 0 30 c 10 0 10 -12 0 -30 Z" fill="#dff3ff" {O4}/>' for i, (x, y) in enumerate([(-90, -150), (100, -130), (130, -40)]))
    return svg(f'''
<rect width="1080" height="1920" fill="#0a0d12"/>
<circle id="neon-fundo" cx="900" cy="500" r="420" fill="url(#vermelho)"/>
<rect x="0" y="0" width="1080" height="1920" fill="#0d1a2c" opacity="0.4"/>
<g id="susto">{pose("susto-suor", 20, 300, 1040)}</g>
<rect x="0" y="1000" width="1080" height="920" fill="url(#verde)"/>
<path d="M0 1700 C 300 1640 780 1640 1080 1700 L 1080 1920 L 0 1920 Z" fill="#0c0f14" {O}/>
<g id="terco4" transform="translate(170 160)"><path d="M0 0 C -20 180 40 300 10 420" fill="none" stroke="#8a5a32" stroke-width="10" stroke-dasharray="2 16" stroke-linecap="round"/><path d="M-12 410 h44 M10 390 v60" stroke="#8a5a32" stroke-width="14" stroke-linecap="round"/></g>
''')


def i05():
    return svg(f'''
<rect width="1080" height="1920" fill="#0b0f16"/>
<path d="M0 0 L 1080 0 L 1080 760 C 760 700 320 700 0 760 Z" fill="#152034"/>
{chuva("chuva5", 50, 5, "#7fa8e0", 0.25)}
<path d="M0 760 C 320 700 760 700 1080 760 L 1080 1920 L 0 1920 Z" fill="#1b1e24" {O}/>
<path d="M0 860 C 320 800 760 800 1080 860" fill="none" stroke="#2b3038" stroke-width="12"/>
<circle cx="540" cy="1150" r="400" fill="url(#verde)" opacity="0.7"/>
<g id="foto" transform="translate(300 980) rotate(-6)"><rect x="-110" y="-140" width="220" height="280" fill="#f2efe8" {O}/><rect x="-90" y="-120" width="180" height="200" fill="#e6a7a0"/>
  <circle cx="0" cy="-40" r="52" fill="#b97a52" {O4}/><path d="M-62 -40 C -70 -120 70 -120 62 -40 C 50 -80 -50 -80 -62 -40 Z" fill="#3a2214"/><path d="M-62 -40 C -80 20 -70 60 -60 80 M62 -40 C 80 20 70 60 60 80" stroke="#3a2214" stroke-width="18" fill="none"/>
  <path d="M-20 -20 q 20 14 40 0" stroke="{K}" stroke-width="4" fill="none"/><circle cx="-18" cy="-50" r="5" fill="{K}"/><circle cx="18" cy="-50" r="5" fill="{K}"/>
  <rect x="-40" y="-160" width="80" height="30" fill="#d8cfa0" opacity="0.85" transform="rotate(4)"/></g>
<g id="envelope"><g transform="translate(720 1380) rotate(8)"><rect x="-200" y="-120" width="400" height="240" fill="#e8e2d0" {O}/><path d="M-200 -120 L 0 20 L 200 -120" fill="none" {O4}/>
  <rect x="-150" y="40" width="300" height="50" fill="none" stroke="#c0392b" stroke-width="7"/><text x="0" y="78" font-family="Archivo Black, sans-serif" font-size="34" fill="#c0392b" text-anchor="middle">EM ATRASO</text></g></g>
<g id="terco5" transform="translate(540 0)"><path d="M0 0 C -30 200 50 340 10 520" fill="none" stroke="#8a5a32" stroke-width="12" stroke-dasharray="2 18" stroke-linecap="round"/><path d="M-16 510 h52 M10 486 v74" stroke="#8a5a32" stroke-width="16" stroke-linecap="round"/></g>
<g id="c5">{pose("rosto-preocupado", 560, 1180, 560)}</g>
''')


def espelho(conteudo, cid, x, y, rx, ry, rot=0):
    return f'''<g transform="translate({x} {y}) rotate({rot})">
<clipPath id="clip-{cid}"><ellipse cx="0" cy="0" rx="{rx}" ry="{ry}"/></clipPath>
<g clip-path="url(#clip-{cid})"><g transform="translate({-rx} {-ry})">{conteudo}</g></g>
<ellipse cx="0" cy="0" rx="{rx}" ry="{ry}" fill="none" stroke="#2b2f36" stroke-width="36"/>
<ellipse cx="0" cy="0" rx="{rx + 18}" ry="{ry + 18}" fill="none" {O}/>
<path d="M{-rx * 0.6} {-ry * 0.55} Q {-rx * 0.2} {-ry * 0.8} {rx * 0.2} {-ry * 0.7}" stroke="#fff" stroke-width="10" opacity="0.25" fill="none"/>
</g>'''


def i06():
    dentro = f'''<rect width="900" height="700" fill="#1a1622"/><rect x="0" y="0" width="900" height="300" fill="#2c2433"/>
<rect x="200" y="120" width="160" height="200" fill="#ffd27a"/><rect x="560" y="40" width="300" height="80" fill="#6b1d2c"/>
<rect x="0" y="520" width="900" height="180" fill="#2b2f38"/>
{homem_corpo(430, 160, 0.78, "h6")}'''
    return svg(f'''
<rect width="1080" height="1920" fill="#0b0f16"/>
<path d="M0 1100 L 1080 950 L 1080 1920 L 0 1920 Z" fill="#e9edf1" {O}/>
<path d="M0 1180 L 1080 1030" stroke="#c9cfd6" stroke-width="12"/>
<path d="M0 0 L 1080 0 L 1080 950 L 0 1100 Z" fill="#152236"/>
{chuva("chuva6", 60, 6)}
<path d="M640 1080 L 760 990 L 840 1030 L 720 1120 Z" fill="#2b2f36" {O}/>
{espelho(dentro, "e6", 520, 820, 430, 330, -6)}
''')


def i07():
    return svg(f'''
<rect width="1080" height="1920" fill="#0a0d12"/>
<path d="M0 0 L 1080 0 L 1080 640 L 0 760 Z" fill="#14213a"/>
{chuva("chuva7", 40, 7, "#7fa8e0", 0.25)}
<path d="M0 760 L 1080 640 L 1080 1920 L 0 1920 Z" fill="#1b1e24" {O}/>
<g transform="translate(540 870) rotate(-4) scale(0.9)">
  <rect x="-330" y="-430" width="660" height="860" rx="50" fill="#121418" {O}/>
  <rect x="-300" y="-395" width="600" height="790" rx="30" fill="#dfe7ee"/>
  <path d="M-300 -395 L 300 -395 L 300 -260 L -300 -260 Z" fill="#ffd23a"/>
  <text x="-260" y="-310" font-family="Inter, sans-serif" font-weight="800" font-size="44" fill="#111">CORRIDA #4471</text>
  <g opacity="0.9"><path d="M-300 -180 h600 M-300 -60 h600 M-300 60 h600 M-160 -260 v520 M80 -260 v520" stroke="#c4ced8" stroke-width="18"/></g>
  <path id="rota" d="M-200 180 C -120 60 -40 40 20 -40 C 80 -120 160 -140 200 -200" fill="none" stroke="#2f7de1" stroke-width="16" stroke-linecap="round" stroke-dasharray="700" stroke-dashoffset="700"/>
  <circle cx="-200" cy="180" r="20" fill="#2fbf71" {O4}/><circle cx="200" cy="-200" r="20" fill="#e23b2e" {O4}/>
  <rect x="-300" y="260" width="600" height="135" fill="#fff"/>
  <text x="-260" y="320" font-family="Inter, sans-serif" font-weight="800" font-size="36" fill="#111">00:58 · HOTEL IMPERIAL</text>
  <text x="-260" y="370" font-family="Inter, sans-serif" font-size="32" fill="#555">motorista: CLÓVIS F.</text>
</g>
<g transform="translate(900 300)"><rect x="-90" y="-60" width="180" height="120" rx="20" fill="#16181c" {O}/><circle cx="-10" cy="0" r="38" fill="#0a0a0c" {O4}/><circle cx="-10" cy="0" r="14" fill="#3a6ea8"/>
  <circle id="rec" cx="60" cy="-30" r="14" fill="#ff2b20"/></g>
<circle id="rec-brilho" cx="960" cy="270" r="70" fill="url(#vermelho)"/>
{mao(210, 1700, -30, 1.0)}
''')


def i08():
    return svg(f'''
<rect width="1080" height="1920" fill="#0b0f16"/>
<circle cx="540" cy="900" r="700" fill="#2a2416" opacity="0.6"/>
<g id="verso"><g transform="translate(540 900) rotate(-5)">
  <rect x="-430" y="-250" width="860" height="500" rx="14" fill="{BILHETE}" {O}/>
  <path d="M-380 -170 h760 M-380 -120 h760" stroke="#e0c96a" stroke-width="10"/>
  <text id="nome" x="-330" y="20" font-family="Georgia, serif" font-style="italic" font-size="120" fill="#1d3fa0">Seu Antônio</text>
  <text id="fone" x="-330" y="160" font-family="Georgia, serif" font-style="italic" font-size="78" fill="#1d3fa0">(11) 9 8472-…</text>
  <path d="M-340 40 C -100 60 120 30 300 50" stroke="#1d3fa0" stroke-width="5" fill="none" opacity="0.6"/>
</g></g>
{mao(200, 1260, 20, 1.4)}
''')


def i09():
    dentro = f'''<rect width="900" height="420" fill="#1a1622"/><rect x="0" y="0" width="900" height="200" fill="#2c2433"/>
<rect x="120" y="60" width="200" height="230" fill="#ffd27a"/><rect x="560" y="10" width="300" height="70" fill="#6b1d2c"/>
<g id="porteiro9" transform="translate(720 150)"><rect x="-26" y="40" width="52" height="150" rx="14" fill="#5a1626" {O4}/><circle cx="0" cy="22" r="26" fill="#8a5a3c" {O4}/><rect x="-28" y="-10" width="56" height="16" fill="#2a0e14"/></g>
<rect x="0" y="330" width="900" height="90" fill="#2b2f38"/>
{homem_corpo(330, 70, 0.62, "h9", tel=True)}'''
    return svg(f'''
<rect width="1080" height="1920" fill="#0b0f16"/>
<path d="M0 0 L 1080 0 L 1080 1300 L 0 1300 Z" fill="#101a2b"/>
{chuva("chuva9", 50, 9, "#7fa8e0", 0.25)}
<rect x="525" y="0" width="30" height="420" fill="#2b2f36" {O4}/>
<rect x="90" y="400" width="900" height="420" rx="40" fill="#2b2f36" {O}/>
<g transform="translate(110 420)"><clipPath id="clip-r9"><rect x="0" y="0" width="860" height="380" rx="26"/></clipPath><g clip-path="url(#clip-r9)">{dentro}</g></g>
<path d="M140 460 L 420 460" stroke="#fff" stroke-width="10" opacity="0.2"/>
<g id="terco9" transform="translate(540 820)"><path d="M0 0 C -30 160 40 260 6 400" fill="none" stroke="#8a5a32" stroke-width="12" stroke-dasharray="2 18" stroke-linecap="round"/><path d="M-18 392 h50 M6 368 v70" stroke="#8a5a32" stroke-width="16" stroke-linecap="round"/></g>
<path d="M0 1300 C 300 1250 780 1250 1080 1300 L 1080 1920 L 0 1920 Z" fill="#1b1e24" {O}/>
<circle cx="540" cy="1500" r="360" fill="url(#verde)" opacity="0.5"/>
''')


def i10():
    return svg(f'''
<rect width="1080" height="1920" fill="#120d16"/>
<rect x="0" y="0" width="1080" height="1100" fill="#2c2433"/>
<rect x="100" y="120" width="220" height="300" fill="#ffd27a" opacity="0.55"/><rect x="760" y="120" width="220" height="300" fill="#ffd27a" opacity="0.4"/>
<circle id="neon10" cx="540" cy="300" r="400" fill="url(#vermelho)" opacity="0.8"/>
{chuva("chuva10", 50, 10, "#ffb3c0", 0.2)}
{homem_busto(520, 1030, 1.75, "h10")}
<circle id="brilho-relogio" cx="900" cy="1380" r="90" fill="#fff3c4" opacity="0"/>
''')


def i11():
    faixas = "".join(f'<rect x="525" y="{y}" width="30" height="110" fill="#e8e3c8"/>' for y in range(900, 2200, 220))
    predios = "".join(f'<rect x="{x}" y="{y}" width="{w}" height="{1000 - y}" fill="{c}" {O4}/>' for x, y, w, c in ((0, 300, 230, "#1b2133"), (200, 420, 160, "#22283c"), (720, 360, 170, "#1e2436"), (860, 250, 220, "#191e2e")))
    return svg(f'''
<rect width="1080" height="1920" fill="url(#noite)"/>
{predios}
<rect x="40" y="380" width="70" height="40" fill="#ff5a7a" opacity="0.8"/><rect x="900" y="330" width="90" height="50" fill="#38e08a" opacity="0.7"/>
<path d="M0 1000 L 1080 1000 L 1080 1920 L 0 1920 Z" fill="#14181f"/>
<path d="M440 1000 L 640 1000 L 1080 1920 L 0 1920 Z" fill="#1c2129"/>
<g id="faixas">{faixas}</g>
<g opacity="0.5"><rect x="40" y="1000" width="70" height="900" fill="#ff5a7a" opacity="0.15"/><rect x="900" y="1000" width="90" height="900" fill="#38e08a" opacity="0.12"/></g>
<g id="taxi-tras"><g transform="translate(540 1250)">
  <ellipse cx="0" cy="250" rx="330" ry="30" fill="#000" opacity="0.5"/>
  <path d="M-300 220 L -300 60 C -300 20 -270 0 -230 -10 L -180 -120 C -160 -160 160 -160 180 -120 L 230 -10 C 270 0 300 20 300 60 L 300 220 Z" fill="#eef1f4" {O}/>
  <path d="M-160 -110 C -150 -135 150 -135 160 -110 L 190 -20 L -190 -20 Z" fill="#203046" {O4}/>
  <rect x="-60" y="-190" width="120" height="40" rx="6" fill="#e23b2e" {O4}/><text x="0" y="-160" font-family="Archivo Black, sans-serif" font-size="26" fill="#fff" text-anchor="middle">TÁXI</text>
  <rect x="-270" y="40" width="110" height="50" rx="10" fill="#ff2b20" {O4}/><rect x="160" y="40" width="110" height="50" rx="10" fill="#ff2b20" {O4}/>
  <rect x="-80" y="110" width="160" height="50" fill="#f3f3f3" {O4}/><text x="0" y="146" font-family="Archivo Black, sans-serif" font-size="32" fill="#222" text-anchor="middle">TXI·4F17</text>
  <rect x="-300" y="170" width="600" height="50" fill="#c9cfd6" {O4}/>
  <rect x="-280" y="210" width="90" height="70" rx="10" fill="#111" {O4}/><rect x="190" y="210" width="90" height="70" rx="10" fill="#111" {O4}/>
</g></g>
<g id="rastro-luz"><path d="M-160 1320 L -460 1920 L -300 1920 Z" fill="#ff2b20" opacity="0.25" transform="translate(540 0)"/><path d="M160 1320 L 460 1920 L 300 1920 Z" fill="#ff2b20" opacity="0.25" transform="translate(540 0)"/></g>
<circle cx="325" cy="1315" r="120" fill="url(#vermelho)"/><circle cx="755" cy="1315" r="120" fill="url(#vermelho)"/>
<g id="vel">{''.join(f'<path d="M{x} {y} l 0 {l}" stroke="#cfe0ff" stroke-width="5" opacity="0.35"/>' for x, y, l in ((80, 1100, 260), (190, 1300, 340), (930, 1150, 300), (1010, 1400, 260), (60, 1550, 220), (980, 1650, 240)))}</g>
{chuva("chuva11", 80, 12)}
''')


def i12():
    return svg(f'''
<rect width="1080" height="1920" fill="url(#noite)"/>
<rect x="0" y="200" width="1080" height="900" fill="#2c2433" {O}/>
<rect x="640" y="520" width="260" height="380" fill="#ffd27a" {O4}/>
<path d="M560 420 L 980 420 L 1040 500 L 500 500 Z" fill="#6b1d2c" {O4}/>
<rect id="brilho12" x="420" y="300" width="660" height="300" fill="url(#vermelho)"/>
<rect x="0" y="1100" width="1080" height="820" fill="#11161f"/>
<rect x="0" y="1100" width="1080" height="60" fill="#2b2f38" {O4}/>
{taxi_lado(-120, 1080, 1.1, "taxi12")}
{homem_corpo(820, 650, 0.78, "hc12")}
<g id="cc12">{pose("segura-bilhete", 250, 1250, 830)}</g>
<rect x="0" y="1500" width="1080" height="420" fill="#ffb661" opacity="0.06"/>
{chuva("chuva12", 90, 13)}
''')


CENAS = {f"i{n:02d}": f for n, f in enumerate([i01, i02, i03, i04, i05, i06, i07, i08, i09, i10, i11, i12], 1)}


def chuva_js(cid, t0, t1, periodo=0.9):
    reps = max(1, int((t1 - t0) / periodo))
    return f'tl.fromTo("#{cid}", {{ y: 0 }}, {{ y: 2320, duration: {periodo}, ease: "none", repeat: {reps - 1}, immediateRender: false }}, {t0});'


def anim(nome, pid, t0, t1, pal):
    """Animações próprias de cada cena (pid = id do plano, para não repetir ids entre planos)."""
    d = round(t1 - t0, 3)
    j = []
    q = lambda s: f"#{pid} {s}"
    if nome == "i01":
        chega = round(min(2.3, d * 0.33), 3)
        j += [f'tl.fromTo("{q("#taxi")}", {{ x: 1150 }}, {{ x: 0, duration: {chega}, ease: "power3.out", immediateRender: false }}, {t0});',
              f'tl.fromTo("{q("#taxi-roda1")},{q("#taxi-roda2")}", {{ rotation: 0, transformOrigin: "50% 50%" }}, {{ rotation: -900, duration: {chega}, ease: "power3.out", immediateRender: false }}, {t0});',
              f'tl.fromTo("{q("#taxi-freio")}", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.25, immediateRender: false }}, {round(t0 + chega * 0.55, 3)});',
              f'tl.to("{q("#taxi-freio")}", {{ opacity: 0.25, duration: 0.6 }}, {round(t0 + chega + 0.4, 3)});',
              f'tl.fromTo("{q("#taxi")}", {{ rotation: 0, transformOrigin: "50% 100%" }}, {{ rotation: -1.2, duration: 0.18, yoyo: true, repeat: 1, ease: "sine.out", immediateRender: false }}, {round(t0 + chega - 0.15, 3)});',
              # o passageiro levanta atrás do carro (desce pelo lado da calçada) e anda até a porta
              f'tl.set("{q("#passageiro")}", {{ opacity: 0 }}, {t0});',
              f'tl.fromTo("{q("#passageiro")}", {{ y: 150, opacity: 1 }}, {{ y: 0, opacity: 1, duration: 0.55, ease: "power2.out", immediateRender: false }}, {round(t0 + chega + 0.35, 3)});',
              f'tl.fromTo("{q("#hc")}", {{ x: 0, y: 0, scale: 1, transformOrigin: "50% 100%" }}, {{ x: 190, y: -34, scale: 0.9, duration: {round(d - chega - 1.0, 3)}, ease: "none", immediateRender: false }}, {round(t0 + chega + 0.95, 3)});',
              f'tl.fromTo("{q("#hc-perna-e")}", {{ rotation: -12, transformOrigin: "50% 0%" }}, {{ rotation: 12, duration: 0.42, yoyo: true, repeat: {int((d - chega - 1.0) / 0.42)}, ease: "sine.inOut", immediateRender: false }}, {round(t0 + chega + 0.95, 3)});',
              f'tl.fromTo("{q("#hc-perna-d")}", {{ rotation: 12, transformOrigin: "50% 0%" }}, {{ rotation: -12, duration: 0.42, yoyo: true, repeat: {int((d - chega - 1.0) / 0.42)}, ease: "sine.inOut", immediateRender: false }}, {round(t0 + chega + 0.95, 3)});',
              # o Clóvis vira a cabeça para o banco de trás
              f'tl.fromTo("{q("#clovis-janela")}", {{ x: 0, rotation: 0, transformOrigin: "50% 100%" }}, {{ x: 10, rotation: 14, duration: 0.5, ease: "power2.inOut", immediateRender: false }}, {round(t0 + d - 1.3, 3)});',
              f'tl.fromTo("{q("#brilho-neon")}", {{ opacity: 1 }}, {{ opacity: 0.35, duration: 0.08, yoyo: true, repeat: 5, immediateRender: false }}, {round(t0 + chega + 1.6, 3)});']
    if nome == "i02" and pid != "p02":
        # o 3º jeito: zoom no recibo e círculo em volta dele (dentro da cena, acompanha a câmera)
        tz = round(pal("Ou tem um terceiro", "escondido"), 3)
        j += [f'tl.fromTo("#{pid} svg", {{ scale: 1, x: 0, y: 0, transformOrigin: "0px 0px" }}, {{ scale: 2.1, x: {540 - 800 * 2.1}, y: {930 - 1690 * 2.1}, duration: 0.7, ease: "power3.inOut", immediateRender: false }}, {round(tz - 0.35, 3)});',
              f'tl.fromTo("{q("#circulo-recibo")},{q("#circulo-sombra")}", {{ opacity: 0, scale: 1.7, transformOrigin: "50% 50%" }}, {{ opacity: 1, scale: 1, duration: 0.45, ease: "back.out(2)", immediateRender: false }}, {tz});',
              f'tl.fromTo("{q("#circulo-recibo")}", {{ strokeWidth: 16 }}, {{ strokeWidth: 24, duration: 0.5, yoyo: true, repeat: 5, ease: "sine.inOut", immediateRender: false }}, {round(tz + 0.5, 3)});']
    if nome == "i02":
        j += [f'tl.fromTo("{q("#brilho-bilhete")}", {{ scale: 0, opacity: 0, transformOrigin: "50% 50%" }}, {{ scale: 1.3, opacity: 1, duration: 0.5, yoyo: true, repeat: 1, ease: "power2.out", immediateRender: false }}, {t0 + 0.6});',
              f'tl.fromTo("{q("#poste-janela")}", {{ opacity: 0.8 }}, {{ opacity: 1, duration: 1.2, yoyo: true, repeat: {max(1, int(d / 1.2))}, ease: "sine.inOut", immediateRender: false }}, {t0});']
    if nome == "i03":
        conta = [pal("Ele conferiu", "Um"), pal("Ele conferiu", "dois"), pal("Ele conferiu", "três"), pal("Ele conferiu", "seis")]
        tempos = [conta[0], conta[1], conta[2], conta[3], conta[3] + 0.15, conta[3] + 0.3]
        for i, tt in enumerate(tempos):
            j += [f'tl.fromTo("{q(f"#risco-{i}")}", {{ opacity: 0, scale: 1.8, transformOrigin: "50% 50%" }}, {{ opacity: 1, scale: 1, duration: 0.18, ease: "back.out(2)", immediateRender: false }}, {round(tt, 3)});',
                  f'tl.fromTo("{q(f"#num-{i}")}", {{ scale: 1, transformOrigin: "50% 50%" }}, {{ scale: 1.15, duration: 0.12, yoyo: true, repeat: 1, immediateRender: false }}, {round(tt, 3)});']
        j.append(f'tl.set("{q("[id^=risco-]")}", {{ opacity: 0 }}, {t0});')
    if nome in ("i04",):
        j += [f'tl.fromTo("{q("#susto")}", {{ scale: 1, transformOrigin: "50% 40%" }}, {{ scale: 1.08, duration: {d}, ease: "power1.in", immediateRender: false }}, {t0});',
              f'tl.fromTo("{q("#susto")}", {{ x: 0 }}, {{ x: 6, duration: 0.05, yoyo: true, repeat: 7, immediateRender: false }}, {round(t0 + 0.25, 3)});',
              f'tl.fromTo("{q("#neon-fundo")}", {{ opacity: 1 }}, {{ opacity: 0.4, duration: 0.07, yoyo: true, repeat: 3, immediateRender: false }}, {t0 + 0.9});',
              f'tl.fromTo("{q("#terco4")}", {{ rotation: -6, transformOrigin: "50% 0%" }}, {{ rotation: 6, duration: 1.1, yoyo: true, repeat: 2, ease: "sine.inOut", immediateRender: false }}, {t0});']
    if nome == "i05":
        j += [f'tl.fromTo("{q("#terco5")}", {{ rotation: -5, transformOrigin: "50% 0%" }}, {{ rotation: 5, duration: 1.3, yoyo: true, repeat: {max(1, int(d / 1.3))}, ease: "sine.inOut", immediateRender: false }}, {t0});',
              f'tl.fromTo("{q("#c5")}", {{ y: 40 }}, {{ y: 0, duration: 0.8, ease: "power2.out", immediateRender: false }}, {t0});',
              f'tl.fromTo("{q("#envelope")}", {{ y: 30, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.5, ease: "power2.out", immediateRender: false }}, {t0 + d * 0.45});']
    if nome == "i06":
        j += [f'tl.fromTo("{q("#h6-braco-e")}", {{ rotation: 0, transformOrigin: "50% 0%" }}, {{ rotation: 28, duration: 0.35, yoyo: true, repeat: 5, ease: "sine.inOut", immediateRender: false }}, {t0 + 0.3});',
              f'tl.fromTo("{q("#h6-braco-d")}", {{ rotation: 0, transformOrigin: "50% 0%" }}, {{ rotation: -28, duration: 0.35, yoyo: true, repeat: 5, ease: "sine.inOut", immediateRender: false }}, {t0 + 0.45});',
              f'tl.fromTo("{q("#h6")}", {{ scaleX: 1, transformOrigin: "50% 50%" }}, {{ scaleX: -1, duration: 0.35, ease: "power2.inOut", immediateRender: false }}, {t0 + d - 0.9});']
    if nome == "i07":
        j += [f'tl.fromTo("{q("#rota")}", {{ strokeDashoffset: 700 }}, {{ strokeDashoffset: 0, duration: {min(2.5, d)}, ease: "power1.inOut", immediateRender: false }}, {t0 + 0.2});',
              f'tl.fromTo("{q("#rec")},{q("#rec-brilho")}", {{ opacity: 1 }}, {{ opacity: 0.15, duration: 0.5, yoyo: true, repeat: {int(d / 0.5)}, ease: "steps(1)", immediateRender: false }}, {t0});']
    if nome == "i08":
        j += [f'tl.fromTo("{q("#verso")}", {{ scaleX: 0, opacity: 0, transformOrigin: "50% 50%" }}, {{ scaleX: 1, opacity: 1, duration: 0.5, ease: "power3.out", immediateRender: false }}, {t0 + 0.1});',
              f'tl.fromTo("{q("#nome")}", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.6, immediateRender: false }}, {round(pal("Problema três", "Seu") - 0.1, 3)});',
              f'tl.fromTo("{q("#fone")}", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.5, immediateRender: false }}, {round(pal("Problema três", "telefone") - 0.2, 3)});']
    if nome == "i09":
        j += [f'tl.fromTo("{q("#h9")}", {{ x: 0 }}, {{ x: 260, duration: {d}, ease: "power1.in", immediateRender: false }}, {t0});',
              f'tl.fromTo("{q("#h9-perna-e")}", {{ rotation: -16, transformOrigin: "50% 0%" }}, {{ rotation: 16, duration: 0.25, yoyo: true, repeat: {int(d / 0.25)}, immediateRender: false }}, {t0});',
              f'tl.fromTo("{q("#h9-perna-d")}", {{ rotation: 16, transformOrigin: "50% 0%" }}, {{ rotation: -16, duration: 0.25, yoyo: true, repeat: {int(d / 0.25)}, immediateRender: false }}, {t0});',
              f'tl.fromTo("{q("#terco9")}", {{ rotation: -4, transformOrigin: "50% 0%" }}, {{ rotation: 4, duration: 1.0, yoyo: true, repeat: {max(1, int(d))}, ease: "sine.inOut", immediateRender: false }}, {t0});']
    if nome == "i10":
        tv = pal("Ele saiu do hotel", "velho")
        j += [f'tl.fromTo("{q("#h10-olhos")}", {{ scaleY: 1, transformOrigin: "50% 50%" }}, {{ scaleY: 0.45, duration: 0.25, immediateRender: false }}, {round(tv - 0.3, 3)});',
              f'tl.fromTo("{q("#h10-sobr-e")},{q("#h10-sobr-d")}", {{ y: 0 }}, {{ y: 10, duration: 0.25, immediateRender: false }}, {round(tv - 0.3, 3)});',
              f'tl.fromTo("{q("#brilho-relogio")}", {{ opacity: 0, scale: 0.4, transformOrigin: "50% 50%" }}, {{ opacity: 0.9, scale: 1.2, duration: 0.3, yoyo: true, repeat: 1, immediateRender: false }}, {t0 + 0.4});',
              f'tl.fromTo("{q("#neon10")}", {{ opacity: 0.8 }}, {{ opacity: 0.3, duration: 0.07, yoyo: true, repeat: 3, immediateRender: false }}, {round(tv, 3)});']
    if nome == "i11":
        j += [f'tl.fromTo("{q("#faixas")}", {{ y: 0 }}, {{ y: 220, duration: 0.18, ease: "none", repeat: {int(d / 0.18)}, immediateRender: false }}, {t0});',
              f'tl.fromTo("{q("#taxi-tras")}", {{ scale: 1, y: 0, transformOrigin: "50% 100%" }}, {{ scale: 0.55, y: -260, duration: {d}, ease: "power2.in", immediateRender: false }}, {t0});',
              f'tl.fromTo("{q("#vel")}", {{ y: 0 }}, {{ y: 300, duration: 0.25, ease: "none", repeat: {int(d / 0.25)}, immediateRender: false }}, {t0});']
    if nome == "i12":
        j += [f'tl.fromTo("{q("#hc12")}", {{ x: 0 }}, {{ x: -150, duration: {d}, ease: "none", immediateRender: false }}, {t0});',
              f'tl.fromTo("{q("#hc12-perna-e")}", {{ rotation: -10, transformOrigin: "50% 0%" }}, {{ rotation: 10, duration: 0.45, yoyo: true, repeat: {int(d / 0.45)}, immediateRender: false }}, {t0});',
              f'tl.fromTo("{q("#hc12-perna-d")}", {{ rotation: 10, transformOrigin: "50% 0%" }}, {{ rotation: -10, duration: 0.45, yoyo: true, repeat: {int(d / 0.45)}, immediateRender: false }}, {t0});',
              f'tl.fromTo("{q("#cc12")}", {{ y: 0 }}, {{ y: -10, duration: 0.9, yoyo: true, repeat: {max(1, int(d / 0.9))}, ease: "sine.inOut", immediateRender: false }}, {t0});']
    for cid in ("chuva", "chuva5", "chuva6", "chuva7", "chuva9", "chuva10", "chuva11", "chuva12"):
        if f'id="{cid}"' in CENAS[nome]():
            j.append(chuva_js(f"{pid} #{cid}", t0, t1))
    if 'id="gotas"' in CENAS[nome]():
        j.append(f'tl.fromTo("#{pid} #gotas .gota", {{ y: 0 }}, {{ y: 26, duration: {d}, ease: "power1.in", stagger: 0.03, immediateRender: false }}, {t0});')
    return j
