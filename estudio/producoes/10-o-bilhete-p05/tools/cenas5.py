"""Cenas novas da Parte 5 (VAI: a lotérica). O resto vem de cenas.py, cenas2.py, cenas3.py e cenas4.py.

s51  fachada da lotérica, chuva fina, o carro preto estacionado
s52  balcão da lotérica: Clóvis com o bilhete, tela BILHETE BLOQUEADO · celular no balcão com o vídeo do posto (o 3º jeito)
s53  Seu Antônio na fila (78 anos, boné bege, cardigã marrom, óculos grossos — ver BÍBLIA)
"""
from cenas import K, O, O4, homem_busto, pose, svg
import cenas
import cenas3

CELULAR = (870, 1600)  # centro do celular com o vídeo do posto (o 3º jeito); zoom e círculo usam isso
ZOOM5 = "p09"


def s51():
    return (cenas3.s33().replace(">POSTO 24H<", ">LOTÉRICA<", 1)
            .replace('<path d="M40 560 L 1040 560 L 1040 650 L 40 650 Z" fill="#e23b2e"', '<path d="M40 560 L 1040 560 L 1040 650 L 40 650 Z" fill="#1f5fbf"', 1))


def parede(conteudo):
    return svg(f'''
<rect width="1080" height="1920" fill="#16243a"/>
<rect x="0" y="260" width="1080" height="666" fill="#1b2c45"/>
<rect x="0" y="250" width="1080" height="16" fill="#ffd23a"/>
{"".join(f'<rect x="{60 + i * 240}" y="440" width="190" height="120" rx="10" fill="#24456f" {O4}/><text x="{155 + i * 240}" y="515" font-family="Archivo Black, sans-serif" font-size="34" fill="#ffd23a" text-anchor="middle">{t}</text>' for i, t in enumerate(("MEGA",)))}
{conteudo}
''')


def s52():
    cx, cy = CELULAR
    return parede(f'''
<g id="tela52"><rect x="560" y="420" width="460" height="260" rx="16" fill="#0b0f16" {O}/><rect x="580" y="440" width="420" height="220" fill="#3a0d0d"/>
<text x="790" y="535" font-family="Archivo Black, sans-serif" font-size="46" fill="#ff4a3d" text-anchor="middle">BILHETE</text>
<text x="790" y="600" font-family="Archivo Black, sans-serif" font-size="46" fill="#ff4a3d" text-anchor="middle">BLOQUEADO</text></g>
<rect x="0" y="926" width="1080" height="1000" fill="#121a28"/>
<g id="clovis52">{pose("segura-bilhete", 60, 860, 820)}</g>
<path d="M0 1460 L 1080 1460 L 1080 1920 L 0 1920 Z" fill="#c9ced6" {O}/>
<path d="M0 1460 L 1080 1460 L 1080 1500 L 0 1500 Z" fill="#e8ecf1" {O4}/>
<g id="celular52" transform="translate({cx} {cy}) rotate(-8)">
  <rect x="-110" y="-190" width="220" height="380" rx="26" fill="#0d0d10" {O}/><rect x="-96" y="-170" width="192" height="340" rx="14" fill="#1a2233"/>
  <rect x="-88" y="-150" width="176" height="96" rx="12" fill="#f2f2f2"/>
  <circle cx="-62" cy="-118" r="14" fill="#ff2b20"/><text x="-40" y="-112" font-family="Inter, sans-serif" font-weight="700" font-size="22" fill="#111">VÍDEO</text>
  <text x="-76" y="-76" font-family="Inter, sans-serif" font-size="20" fill="#333">do posto 24h</text>
</g>
<circle id="circulo-celular" cx="{cx}" cy="{cy - 110}" r="130" fill="none" stroke="#ffd23a" stroke-width="14" opacity="0"/>
''')


def seu_antonio(x, y, s, ids="sa"):
    b = (homem_busto(x, y, s, ids, telefone=False).replace("#24324f", "#7a5233").replace("#172036", "#5e3e26")
         .replace('fill="#f4f4f2"', 'fill="#e8e2d0"').replace('fill="#0d0d10"', 'fill="#d9d6cf"').replace("#e2b48f", "#d6a47c"))
    extra = f'''<g transform="translate({x} {y}) scale({s})">
  <path d="M-138 -70 C -140 -200 140 -200 138 -70 Z" fill="#cdb68a" {O}/><path d="M60 -80 C 140 -84 200 -70 220 -50 L 120 -50 Z" fill="#b89e6e" {O}/>
  <circle cx="-58" cy="-18" r="40" fill="none" stroke="{K}" stroke-width="10"/><circle cx="58" cy="-18" r="40" fill="none" stroke="{K}" stroke-width="10"/><path d="M-18 -18 h36" stroke="{K}" stroke-width="8"/>
  <path d="M-60 74 C -30 60 30 60 60 74 C 40 90 -40 90 -60 74 Z" fill="#eeeae2" {O4}/>
  <path d="M-80 20 q 12 10 24 0 M56 20 q 12 10 24 0" stroke="#8a5a40" stroke-width="4" fill="none"/>
</g>'''
    return b + extra


def s53():
    return parede(f'''
<rect x="0" y="926" width="1080" height="1000" fill="#121a28"/>
<path d="M60 1180 L 1020 1180" stroke="#d9b44a" stroke-width="10"/><rect x="40" y="1100" width="26" height="420" fill="#8a8f98" {O4}/><rect x="1014" y="1100" width="26" height="420" fill="#8a8f98" {O4}/>
<g id="antonio53">{seu_antonio(540, 1150, 1.5)}</g>
''')


CENAS = {"s51": s51, "s52": s52, "s53": s53}


def anim(nome, pid, t0, t1, pal, ini):
    d = round(t1 - t0, 3)
    q = lambda s: f"#{pid} {s}"
    j = []
    if nome == "s51":
        j += [f'tl.fromTo("{q("#suv33-pos")}", {{ x: 700 }}, {{ x: 0, duration: 1.6, ease: "power3.out", immediateRender: false }}, {t0});',
              cenas.chuva_js(f"{pid} #chuva14", t0, t1)]
    if nome == "s52":
        j.append(f'tl.fromTo("{q("#tela52")}", {{ opacity: 1 }}, {{ opacity: 0.35, duration: 0.25, yoyo: true, repeat: {max(1, int(d / 0.25))}, ease: "steps(1)", immediateRender: false }}, {t0});')
        if pid == ZOOM5:
            cx, cy = CELULAR
            tz = round(pal("Ou tem", "escondido"), 3)
            j += [f'tl.fromTo("#{pid} svg", {{ scale: 1, x: 0, y: 0, transformOrigin: "0px 0px" }}, {{ scale: 2.0, x: {540 - cx * 2.0:.0f}, y: {760 - (cy - 110) * 2.0:.0f}, duration: 0.7, ease: "power3.inOut", immediateRender: false }}, {round(tz - 0.35, 3)});',
                  f'tl.fromTo("{q("#circulo-celular")}", {{ opacity: 0, scale: 1.7, transformOrigin: "50% 50%" }}, {{ opacity: 1, scale: 1, duration: 0.45, ease: "back.out(2)", immediateRender: false }}, {tz});']
    if nome == "s53":
        j.append(f'tl.fromTo("{q("#antonio53")}", {{ y: 40, opacity: 0.4 }}, {{ y: 0, opacity: 1, duration: 0.9, ease: "power2.out", immediateRender: false }}, {t0});')
    if nome == "s32":
        pass
    return j
