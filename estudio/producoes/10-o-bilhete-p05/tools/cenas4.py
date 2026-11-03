"""Cenas novas da Parte 4 (VENDE: a mala e o segundo envelope). O resto vem de cenas.py, cenas2.py e cenas3.py.

s41  posto: mala aberta cheia de dinheiro no balcão, Clóvis e o comprador · o atendente segue filmando (3º jeito)
s42  close do comprador tirando um segundo envelope
s46  RECUSA: Clóvis empurra a mala fechada de volta
"""
from cenas import K, O, O4, pose, svg
import cenas3
from cenas3 import comprador, interior


def mala(x, y, aberta=True, mid="mala"):
    notas = "".join(f'<rect x="{x - 160 + i * 66}" y="{y - 40}" width="58" height="70" rx="4" fill="#3f8f57" {O4}/><rect x="{x - 160 + i * 66}" y="{y - 12}" width="58" height="14" fill="#f2e6b8"/>' for i in range(5))
    tampa = (f'<g id="{mid}-tampa"><path d="M{x - 185} {y - 50} L {x + 185} {y - 50} L {x + 165} {y - 230} L {x - 165} {y - 230} Z" fill="#2b2118" {O}/><path d="M{x - 160} {y - 70} L {x + 160} {y - 70} L {x + 145} {y - 210} L {x - 145} {y - 210} Z" fill="#4a3a2a"/></g>' if aberta else "")
    corpo = f'<rect x="{x - 185}" y="{y - 50}" width="370" height="130" rx="14" fill="#3a2b1f" {O}/>'
    if aberta:
        corpo += notas
    else:
        corpo = f'<path d="M{x - 40} {y - 70} q 40 -40 80 0" stroke="{K}" stroke-width="12" fill="none"/>' + corpo + f'<rect x="{x - 185}" y="{y - 50}" width="370" height="30" fill="#2b2118" {O4}/><rect x="{x - 20}" y="{y - 40}" width="40" height="22" rx="4" fill="#d9b44a" {O4}/>'
    return f'<g id="{mid}">{tampa}{corpo}</g>'


def s41():
    return interior(f'''<g id="clovis41">{pose("rosto-preocupado", 20, 860, 560)}</g>
<g id="comprador41">{comprador(800, 1000, 0.95, "cp41")}</g>''', extra=mala(700, 1420, True, "mala41"))


def s42():
    env = '<g id="env42" transform="translate(540 1560)"><rect x="-230" y="-140" width="460" height="280" rx="12" fill="#c9a46a" stroke="#111" stroke-width="8"/><path d="M-230 -140 L 0 30 L 230 -140" fill="#b38d55" stroke="#111" stroke-width="8"/><text x="0" y="110" font-family="Archivo Black, sans-serif" font-size="44" fill="#3a2b1f" text-anchor="middle">2º ENVELOPE</text></g>'
    return cenas3.s32().replace("</svg>", env + "</svg>", 1)


def s46():
    return interior(f'''<g id="clovis46">{pose("tres-quartos", 0, 860, 600)}</g>''', extra=mala(620, 1420, False, "mala46"))


CENAS = {"s41": s41, "s42": s42, "s46": s46}


def anim(nome, pid, t0, t1, pal, ini):
    d = round(t1 - t0, 3)
    q = lambda s: f"#{pid} {s}"
    j = cenas3.anim(nome, pid, t0, t1, pal, ini)  # vapor do café + REC piscando do atendente
    if nome == "s41":
        j.append(f'tl.fromTo("{q("#mala41-tampa")}", {{ scaleY: 0.05, transformOrigin: "50% 100%" }}, {{ scaleY: 1, duration: 0.5, ease: "back.out(1.6)", immediateRender: false }}, {t0 + 0.1});')
    if nome == "s42":
        j.append(f'tl.fromTo("{q("#env42")}", {{ y: 500, rotation: -6 }}, {{ y: 0, rotation: 2, duration: 0.7, ease: "power3.out", immediateRender: false }}, {round(pal("O homem guardou", "segundo") - 0.3, 3)});')
    if nome == "s46":
        j.append(f'tl.fromTo("{q("#mala46")}", {{ x: -160 }}, {{ x: 120, duration: {min(d, 1.4)}, ease: "power2.out", immediateRender: false }}, {t0 + 0.3});')
    return j
