"""Cenas novas da Parte 7 (o bilhete volta pro dono).

s71  verso do bilhete com os dois nomes: Seu Antônio e Clóvis, "metade de cada"
s72  o Clóvis coloca o bilhete na mão do Seu Antônio (vem da Parte 6)
s73  a mala com os vinte milhões no banco de trás do táxi (vem da Parte 6)
s74  close do Clóvis entendendo o que acabou de acontecer
"""
from cenas import BILHETE, K, O, O4, mao, pose, svg
import cenas6

CENAS_BASE = {}


def s71():
    return svg(f'''
<rect width="1080" height="1920" fill="#0b0f16"/>
<circle cx="540" cy="900" r="700" fill="#2a2416" opacity="0.6"/>
<g id="verso7"><g transform="translate(540 880) rotate(-5)">
  <rect x="-430" y="-280" width="860" height="560" rx="14" fill="{BILHETE}" {O}/>
  <path d="M-380 -200 h760" stroke="#e0c96a" stroke-width="10"/>
  <text x="-330" y="-90" font-family="Georgia, serif" font-style="italic" font-size="104" fill="#1d3fa0">Seu Antônio</text>
  <g id="linha7-2"><path d="M-380 -30 h760" stroke="#e0c96a" stroke-width="10"/>
    <text id="nome-clovis" x="-330" y="70" font-family="Georgia, serif" font-style="italic" font-size="104" fill="#1d3fa0">Clóvis</text></g>
  <g id="metade7"><path d="M-380 130 h760" stroke="#e0c96a" stroke-width="6" opacity="0.6"/>
    <text x="-330" y="222" font-family="Georgia, serif" font-style="italic" font-size="76" fill="#1d3fa0">metade de cada</text></g>
  <path id="caneta7" d="M-340 100 C -100 120 120 90 300 110" stroke="#1d3fa0" stroke-width="5" fill="none" opacity="0.5"/>
</g></g>
{mao(190, 1330, 18, 1.3)}
''')


def s72():
    return cenas6.s66()


def s73():
    return cenas6.s65()


def s74():
    import re
    base = cenas6.CENAS["s61"]()
    base = re.sub(r'<g id="cel61">.*?</g></g>', "", base, flags=re.S)       # sem o celular: acabou
    base = base.replace('<g id="clovis61">', '<g id="clovis74">').replace("telefone-noite", "rosto-sorriso-noite")
    return base


CENAS = {"s71": s71, "s72": s72, "s73": s73, "s74": s74}


def anim(nome, pid, t0, t1, pal, ini):
    d = round(t1 - t0, 3)
    q = lambda s: f"#{pid} {s}"
    j = []
    if nome == "s71":
        t_nome = pal("Dois nomes", "nomes") if any(True for _ in [0]) else t0
        j += [f'tl.fromTo("{q("#verso7")}", {{ scale: 0.92, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.5, ease: "power3.out", immediateRender: false }}, {t0});',
              f'tl.fromTo("{q("#linha7-2")}", {{ opacity: 0, x: -30 }}, {{ opacity: 1, x: 0, duration: 0.45, ease: "power3.out", immediateRender: false }}, {round(t0 + 0.5, 3)});',
              f'tl.fromTo("{q("#metade7")}", {{ opacity: 0, y: 24 }}, {{ opacity: 1, y: 0, duration: 0.45, ease: "power3.out", immediateRender: false }}, {round(t0 + 1.0, 3)});']
    if nome == "s72":
        j += cenas6.anim("s66", pid, t0, t1, pal, ini)
    if nome == "s73":
        j += cenas6.anim("s65", pid, t0, t1, pal, ini)
    if nome == "s74":
        j.append(f'tl.fromTo("{q("#clovis74")}", {{ y: 26, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.5, ease: "power3.out", immediateRender: false }}, {t0});')
    return [x for x in j if x]
