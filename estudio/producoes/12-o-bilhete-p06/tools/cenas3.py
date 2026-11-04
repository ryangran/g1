"""Cenas novas da Parte 3 (o posto 24 h). O resto vem de cenas.py e cenas2.py.

s31  dentro do posto: Clóvis no balcão, o comprador senta do lado · o atendente filmando (o 3º jeito)
s32  close do comprador (casaco preto, óculos, barba grisalha)
s33  lá fora: o carro preto estaciona no posto
s34  FOGE: Clóvis correndo pela porta dos fundos
s35  VENDE: Clóvis segurando o bilhete no balcão
"""
from cenas import K, O, O4, homem_busto, pose, svg, taxi_lado
import cenas
import cenas2

ATENDENTE = (760, 700)  # centro do atendente filmando (o 3º jeito); o círculo usa isso
ZOOM_PID = "p09"  # plano em que o 3º jeito ganha zoom + círculo
CASACO = "#16161a"


def comprador(x, y, s, ids):
    b = homem_busto(x, y, s, ids, telefone=False).replace("#24324f", CASACO).replace("#172036", "#0c0c0f").replace('fill="#f4f4f2"', 'fill="#2a2a30"')
    oculos = f'<g transform="translate({x} {y}) scale({s})"><path d="M-95 -22 h70 v26 h-70 Z M25 -22 h70 v26 h-70 Z M-25 -12 h50" fill="#0b0b0d" opacity="0.92" stroke="{K}" stroke-width="5"/><path d="M-118 40 C -110 120 -60 150 0 152 C 60 150 110 120 118 40 C 100 90 60 110 0 112 C -60 110 -100 90 -118 40 Z" fill="#8f8a85" opacity="0.85"/></g>'
    return b + oculos


def interior(conteudo, extra=""):
    prateleiras = "".join(f'<rect x="{x}" y="{y}" width="150" height="16" fill="#3a3f49"/>' + "".join(f'<rect x="{x + 8 + i * 28}" y="{y - 46}" width="22" height="46" fill="{c}" {O4}/>' for i, c in enumerate(("#e23b2e", "#2fae6a", "#ffd23a", "#3a6ea8", "#e23b2e")))
                          for x in (30, 220, 410) for y in (420, 560))
    vx, vy = ATENDENTE
    return svg(f'''
<rect width="1080" height="1920" fill="#20242c"/>
<rect x="0" y="0" width="1080" height="160" fill="#fff6d8" opacity="0.5"/>
<rect x="0" y="160" width="1080" height="760" fill="#2a2f3a"/>
{prateleiras}
<rect x="620" y="300" width="420" height="300" rx="10" fill="#1d2a3a" {O4}/><rect x="640" y="320" width="380" height="260" fill="#aee3ff" opacity="0.25"/>
<rect x="600" y="760" width="460" height="140" fill="#3a3f49" {O4}/>
<g id="atendente">
  <rect x="{vx - 45}" y="{vy}" width="90" height="70" rx="10" fill="#e23b2e" {O4}/>
  <circle cx="{vx}" cy="{vy - 30}" r="36" fill="#b07a52" {O4}/><path d="M{vx - 38} {vy - 40} q 38 -40 76 0" fill="#2a1a10"/>
  <rect x="{vx + 12}" y="{vy - 26}" width="44" height="28" rx="5" fill="#0d0d10" {O4}/><circle id="rec-atendente" cx="{vx + 50}" cy="{vy - 20}" r="5" fill="#ff2b20"/>
  <path d="M{vx + 30} {vy + 10} l 10 -14" stroke="#b07a52" stroke-width="10" stroke-linecap="round"/>
</g>
<circle id="circulo-atendente" cx="{vx + 10}" cy="{vy - 10}" r="120" fill="none" stroke="#ffd23a" stroke-width="14" opacity="0"/>
<rect x="0" y="920" width="1080" height="1000" fill="#181b21"/>
{conteudo}
<path d="M0 1460 L 1080 1460 L 1080 1920 L 0 1920 Z" fill="#5a3a22" {O}/>
<path d="M0 1460 L 1080 1460 L 1080 1500 L 0 1500 Z" fill="#7a5233" {O4}/>
<g id="cafe1" transform="translate(300 1400)"><path d="M-40 0 L 40 0 L 30 70 L -30 70 Z" fill="#f2efe8" {O4}/><path id="vapor1" d="M-10 -10 q 10 -30 0 -60 M12 -10 q 10 -30 0 -60" stroke="#fff" stroke-width="6" fill="none" opacity="0.5"/></g>
{extra}
''')


def s31():
    return interior(f'''<g id="clovis31">{pose("rosto-preocupado", 20, 860, 560)}</g>
<g id="comprador31">{comprador(800, 1000, 0.95, "cp31")}</g>''')


def s32():
    return svg(f'''
<rect width="1080" height="1920" fill="#14161b"/>
<rect x="0" y="0" width="1080" height="1100" fill="#2a2f3a"/>
<rect x="80" y="160" width="300" height="420" fill="#fff6d8" opacity="0.18"/><rect x="700" y="160" width="300" height="420" fill="#fff6d8" opacity="0.12"/>
<circle id="neon32" cx="540" cy="360" r="420" fill="url(#vermelho)" opacity="0.6"/>
{comprador(540, 1060, 1.7, "cp32")}
''')


def s33():
    base = cenas2.s14()
    carro = f'<g id="suv33-pos" transform="translate(380 1120) scale(0.95)">{cenas2.suv("suv33")}</g>'
    return base.replace('<g id="chuva14">', carro + '<g id="chuva14">', 1)


def s34():
    return svg(f'''
<rect width="1080" height="1920" fill="#07090e"/>
<rect x="0" y="0" width="1080" height="1920" fill="#101521"/>
<rect x="640" y="580" width="340" height="660" fill="#1d2433" {O}/><rect x="690" y="640" width="240" height="560" fill="#05070b"/>
<rect x="680" y="470" width="260" height="80" rx="10" fill="#0f3a24" {O4}/><text x="810" y="526" font-family="Archivo Black, sans-serif" font-size="46" fill="#5dff9e" text-anchor="middle">SAÍDA</text>
<circle id="saida-glow" cx="810" cy="510" r="220" fill="url(#verde)"/>
<rect x="0" y="1240" width="1080" height="680" fill="#0b0e14"/>
<g id="corre">{pose("correndo", 80, 760, 640)}</g>
''')


def s35():
    return interior(f'''<g id="vende35">{pose("segura-bilhete", 140, 860, 820)}</g>''')


CENAS = {"s31": s31, "s32": s32, "s33": s33, "s34": s34, "s35": s35}


def anim(nome, pid, t0, t1, pal, ini):
    d = round(t1 - t0, 3)
    q = lambda s: f"#{pid} {s}"
    j = [f'tl.fromTo("{q("#vapor1")}", {{ y: 0, opacity: 0.5 }}, {{ y: -20, opacity: 0.1, duration: 1.2, repeat: {max(1, int(d / 1.2))}, ease: "sine.out", immediateRender: false }}, {t0});'] if nome in ("s31", "s35") else []
    if nome in ("s31", "s35", "s41", "s46"):
        j.append(f'tl.fromTo("{q("#rec-atendente")}", {{ opacity: 1 }}, {{ opacity: 0.15, duration: 0.4, yoyo: true, repeat: {int(d / 0.4)}, ease: "steps(1)", immediateRender: false }}, {t0});')
    if nome == "s31" and t0 < 1:  # gancho: o comprador chega e senta do lado
        j += [f'tl.fromTo("{q("#comprador31")}", {{ x: 520 }}, {{ x: 0, duration: 1.3, ease: "power3.out", immediateRender: false }}, {t0});',
              f'tl.fromTo("{q("#clovis31")}", {{ x: 0 }}, {{ x: -8, duration: 0.05, yoyo: true, repeat: 7, immediateRender: false }}, {t0 + 1.3});']
    if nome == "s31" and pid == ZOOM_PID:  # o 3º jeito: zoom no atendente e círculo
        vx, vy = ATENDENTE
        tz = round(pal("Ou tem", "escondido"), 3)
        j += [f'tl.fromTo("#{pid} svg", {{ scale: 1, x: 0, y: 0, transformOrigin: "0px 0px" }}, {{ scale: 2.1, x: {540 - vx * 2.1:.0f}, y: {820 - vy * 2.1:.0f}, duration: 0.7, ease: "power3.inOut", immediateRender: false }}, {round(tz - 0.35, 3)});',
              f'tl.fromTo("{q("#circulo-atendente")}", {{ opacity: 0, scale: 1.7, transformOrigin: "50% 50%" }}, {{ opacity: 1, scale: 1, duration: 0.45, ease: "back.out(2)", immediateRender: false }}, {tz});']
    if nome == "s32":
        j += [f'tl.fromTo("{q("#neon32")}", {{ opacity: 0.6 }}, {{ opacity: 0.25, duration: 0.07, yoyo: true, repeat: 3, immediateRender: false }}, {round(pal("No vídeo", "vinte"), 3)});']
    if nome == "s33":
        j += [f'tl.fromTo("{q("#suv33-pos")}", {{ x: 700 }}, {{ x: 0, duration: 1.6, ease: "power3.out", immediateRender: false }}, {t0});',
              f'tl.fromTo("{q("#suv33-freio")}", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.2, immediateRender: false }}, {t0 + 1.2});',
              cenas.chuva_js(f"{pid} #chuva14", t0, t1)]
    if nome == "s34":
        j += [f'tl.fromTo("{q("#corre")}", {{ x: 0, y: 0 }}, {{ x: 120, y: -10, duration: {d}, ease: "power1.in", immediateRender: false }}, {t0});',
              f'tl.fromTo("{q("#saida-glow")}", {{ opacity: 1 }}, {{ opacity: 0.5, duration: 0.5, yoyo: true, repeat: {max(1, int(d / 0.5))}, immediateRender: false }}, {t0});']
    if nome == "s35":
        j += [f'tl.fromTo("{q("#vende35")}", {{ y: 30 }}, {{ y: 0, duration: 0.8, ease: "power2.out", immediateRender: false }}, {t0});']
    return [x for x in j if x]
