"""Cenas novas da Parte 2 (o resto vem de tools/cenas.py, copiado da Parte 1).

s01  sinal fechado: o carro preto colado no táxi · a viatura apagada na esquina (o 3º jeito)
s06  Clóvis dirigindo (pose oficial) com o rádio da central aceso
s07  close do rádio da central, com as barras de voz
s08  Clóvis olhando o retrovisor (pose oficial)
s12  close do vidro do carro preto descendo
s14  posto 24 h cheio de gente
s15  Clóvis no telefone (pose oficial)
"""
import random

from cenas import K, O, O4, chuva, gotas, pose, svg, taxi_lado

VIATURA = (850, 905, 0.36)  # (x, y, escala) da viatura escondida em s01; o círculo do 3º jeito usa isso


def suv(cid="suv"):
    """Carro preto grande de perfil, frente para a esquerda. O vidro da frente desce (id <cid>-vidro)."""
    return f'''<g id="{cid}">
  <ellipse cx="350" cy="250" rx="360" ry="22" fill="#000" opacity="0.55"/>
  <polygon id="{cid}-farol" points="20,150 -420,90 -420,290 20,190" fill="#ffe7a8" opacity="0.16"/>
  <clipPath id="{cid}-janela"><path d="M168 92 L 218 26 L 335 26 L 335 92 Z"/></clipPath>
  <g clip-path="url(#{cid}-janela)">
    <rect x="160" y="20" width="190" height="80" fill="#040405"/>
    <circle id="{cid}-brasa" cx="292" cy="70" r="5" fill="#ff7a2a"/><circle cx="292" cy="70" r="16" fill="#ff7a2a" opacity="0.25"/>
    <g id="{cid}-vidro"><rect x="160" y="20" width="190" height="80" fill="#262d3a"/><path d="M190 30 L 230 30 L 200 88 L 175 88 Z" fill="#fff" opacity="0.12"/></g>
  </g>
  <path d="M20 205 L 20 125 C 20 104 40 94 70 92 L 160 90 L 208 22 C 214 14 222 10 234 10 L 600 10 C 642 10 662 30 668 62 L 684 122 L 684 232 L 20 232 Z M168 92 L 218 26 L 335 26 L 335 92 Z" fill="#15171c" fill-rule="evenodd" {O}/>
  <path d="M350 26 L 560 26 C 590 26 610 44 618 92 L 350 92 Z" fill="#1d222c" {O4}/>
  <path d="M335 26 L 335 92 M343 26 L 343 200" stroke="{K}" stroke-width="6"/>
  <path d="M40 140 L 680 140" stroke="#2c313b" stroke-width="5"/>
  <path d="M28 168 L 80 168" stroke="#ffe0a0" stroke-width="16" stroke-linecap="round"/>
  <rect x="660" y="150" width="22" height="34" rx="4" fill="#c4231a" {O4}/>
  <circle id="{cid}-freio" cx="672" cy="166" r="70" fill="url(#vermelho)" opacity="0"/>
  <path d="M240 28 L 300 28" stroke="#fff" stroke-width="5" opacity="0.18"/>
  <g><circle cx="150" cy="232" r="58" fill="#0b0c0f" {O}/><circle cx="150" cy="232" r="27" fill="#5d646d" {O4}/></g>
  <g><circle cx="560" cy="232" r="58" fill="#0b0c0f" {O}/><circle cx="560" cy="232" r="27" fill="#5d646d" {O4}/></g>
</g>'''


def viatura(x, y, s, cid="viatura"):
    """Viatura parada com as luzes apagadas (o 3º jeito da Parte 2)."""
    return f'''<g id="{cid}" transform="translate({x} {y}) scale({s})">
  <ellipse cx="300" cy="240" rx="320" ry="20" fill="#000" opacity="0.5"/>
  <path d="M10 170 C 10 120 40 110 90 105 L 190 100 C 230 40 280 25 360 25 L 470 25 C 520 25 560 60 590 105 L 620 110 C 650 115 660 140 660 175 L 660 215 L 10 215 Z" fill="#e9ecef" {O}/>
  <path d="M10 150 L 660 150 L 660 215 L 10 215 Z" fill="#1d2433"/>
  <path d="M215 100 C 245 55 285 45 345 45 L 350 100 Z M370 45 L 460 45 C 500 45 530 70 555 100 L 370 100 Z" fill="#273246" {O4}/>
  <rect x="290" y="0" width="140" height="28" rx="8" fill="#3a1f24" {O4}/><rect x="292" y="2" width="68" height="24" rx="6" fill="#5a2a30"/><rect x="362" y="2" width="66" height="24" rx="6" fill="#26355a"/>
  <text x="335" y="192" font-family="Archivo Black, sans-serif" font-size="40" fill="#ffffff" text-anchor="middle">POLÍCIA</text>
  <circle cx="150" cy="215" r="55" fill="#141518" {O}/><circle cx="150" cy="215" r="24" fill="#8a929c" {O4}/>
  <circle cx="520" cy="215" r="55" fill="#141518" {O}/><circle cx="520" cy="215" r="24" fill="#8a929c" {O4}/>
</g>'''


def s01():
    vx, vy, vs = VIATURA
    r = random.Random(3)
    janelas = "".join(f'<rect x="{x}" y="{y}" width="46" height="60" fill="{r.choice(["#ffcf7a", "#3a4560", "#3a4560"])}" {O4}/>' for x in range(30, 1060, 90) for y in (330, 440, 550))
    cabeca = pose("rosto-preocupado", 240, 32, 96)
    return svg(f'''
<rect width="1080" height="1920" fill="url(#noite)"/>
<rect x="0" y="260" width="1080" height="760" fill="#1b1f2c" {O4}/>
{janelas}
<rect x="760" y="640" width="320" height="380" fill="#232838" {O4}/>
<rect x="800" y="700" width="90" height="110" fill="#ffcf7a" opacity="0.8"/>
<path d="M0 1020 L 1080 1020 L 1080 1920 L 0 1920 Z" fill="#10141c"/>
<path d="M0 1020 L 1080 1020" stroke="#3a3f49" stroke-width="10"/>
{viatura(vx, vy, vs)}
<circle id="circulo-viatura" cx="{vx + 300 * vs:.0f}" cy="{vy + 130 * vs:.0f}" r="150" fill="none" stroke="#ffd23a" stroke-width="16" opacity="0"/>
<path d="M0 1300 L 1080 1300" stroke="#e8e3c8" stroke-width="10" stroke-dasharray="90 70" opacity="0.5"/>
<g transform="translate(150 1040) scale(0.88)">{taxi_lado(0, 0, 1.0, "taxi1", cabeca)}</g>
<g id="suv-pos" transform="translate(-20 1230) scale(1.6)">{suv()}</g>
<g id="semaforo">
  <rect x="96" y="0" width="18" height="760" fill="#2a2e36" {O4}/>
  <rect x="40" y="300" width="130" height="330" rx="22" fill="#141619" {O}/>
  <circle cx="105" cy="365" r="42" fill="#ff2b20"/><circle id="sinal-glow" cx="105" cy="365" r="120" fill="url(#vermelho)"/>
  <circle cx="105" cy="465" r="42" fill="#3a2c12"/><circle cx="105" cy="565" r="42" fill="#11301c"/>
</g>
<rect x="0" y="1020" width="1080" height="900" fill="#ff2b20" opacity="0.06"/>
{chuva("chuva", 90, 21)}
''')


def s06():
    luzes = "".join(f'<circle class="poste-passa" cx="{x}" cy="{y}" r="16" fill="#ffd9a0" opacity="0.8"/>' for x, y in ((180, 330), (520, 300), (860, 340)))
    return svg(f'''
<rect width="1080" height="1920" fill="#07090e"/>
<path d="M0 160 L 1080 160 L 1080 620 L 0 620 Z" fill="#132037"/>
<g id="luzes">{luzes}</g>
{gotas("gotas6", (40, 180, 1040, 600), 30, 6)}
<path d="M0 620 L 1080 620" stroke="{K}" stroke-width="10"/>
<rect x="0" y="620" width="1080" height="1300" fill="#0d1017"/>
<circle cx="760" cy="1300" r="420" fill="url(#verde)" opacity="0.6"/>
{pose("dirigindo", 20, 700, 1040)}
<g id="radio6" transform="translate(620 1520)"><rect x="0" y="0" width="380" height="150" rx="18" fill="#16181d" {O}/>
  <rect x="24" y="24" width="250" height="70" rx="8" fill="#0d3a24"/><text x="149" y="72" font-family="JetBrains Mono, monospace" font-weight="700" font-size="40" fill="#5dff9e" text-anchor="middle">CENTRAL</text>
  <circle id="led6" cx="320" cy="58" r="16" fill="#ff2b20"/><rect x="24" y="108" width="330" height="18" rx="9" fill="#2a2e36"/></g>
''')


def s07():
    barras = "".join(f'<rect class="onda" x="{250 + i * 48}" y="840" width="28" height="80" rx="10" fill="#5dff9e"/>' for i in range(12))
    return svg(f'''
<rect width="1080" height="1920" fill="#06080c"/>
<circle cx="540" cy="960" r="560" fill="url(#verde)" opacity="0.5"/>
<g id="terco7" transform="translate(540 0)"><path d="M0 0 C -30 200 50 340 10 520" fill="none" stroke="#8a5a32" stroke-width="12" stroke-dasharray="2 18" stroke-linecap="round"/><path d="M-16 510 h52 M10 486 v74" stroke="#8a5a32" stroke-width="16" stroke-linecap="round"/></g>
<g transform="translate(140 680)">
  <rect x="0" y="0" width="800" height="520" rx="40" fill="#16181d" {O}/>
  <rect x="50" y="50" width="700" height="220" rx="16" fill="#0b2e1d" {O4}/>
  <text x="90" y="125" font-family="JetBrains Mono, monospace" font-weight="700" font-size="46" fill="#5dff9e">CENTRAL · CH 03</text>
  <circle id="led7" cx="700" cy="100" r="22" fill="#ff2b20"/>
  <g>{''.join(f'<circle cx="{110 + c * 40}" cy="{340 + l * 40}" r="9" fill="#2a2e36"/>' for c in range(15) for l in range(4))}</g>
  <rect x="600" y="300" width="130" height="170" rx="20" fill="#2a2e36" {O4}/>
</g>
<g>{barras}</g>
''')


def s08():
    return svg(f'''
<rect width="1080" height="1920" fill="#06080c"/>
<path d="M0 0 L 1080 0 L 1080 560 L 0 560 Z" fill="#101a2b"/>
{chuva("chuva8", 40, 8, "#7fa8e0", 0.25)}
<circle cx="540" cy="1250" r="560" fill="url(#verde)" opacity="0.55"/>
{pose("retrovisor", -40, 600, 1160)}
''')


def s12():
    return svg(f'''
<rect width="1080" height="1920" fill="#07090e"/>
<rect x="0" y="0" width="1080" height="1920" fill="#ff2b20" opacity="0.07"/>
<g transform="translate(-560 540) scale(4.4)">{suv("suv12")}</g>
{chuva("chuva12b", 70, 12)}
''')


def s14():
    pessoas = "".join(f'<g transform="translate({x} 930)"><circle cx="0" cy="0" r="22" fill="#0c0d10"/><path d="M-26 30 Q 0 10 26 30 L 30 120 L -30 120 Z" fill="#0c0d10"/></g>' for x in (430, 600, 700))
    return svg(f'''
<rect width="1080" height="1920" fill="url(#noite)"/>
<rect x="300" y="760" width="720" height="300" fill="#1f2635" {O}/>
<rect x="340" y="800" width="640" height="200" fill="#fff3c4" opacity="0.85"/>
{pessoas}
<path d="M40 560 L 1040 560 L 1040 650 L 40 650 Z" fill="#e23b2e" {O}/>
<path d="M40 650 L 1040 650 L 1040 680 L 40 680 Z" fill="#f2f2f2" {O4}/>
<text x="540" y="630" font-family="Archivo Black, sans-serif" font-size="66" fill="#fff" text-anchor="middle">POSTO 24H</text>
<rect id="luz-posto" x="40" y="680" width="1000" height="560" fill="#fff6d8" opacity="0.18"/>
<g>{''.join(f'<g transform="translate({x} 860)"><rect x="0" y="0" width="90" height="200" rx="10" fill="#d8dde3" {O4}/><rect x="16" y="22" width="58" height="40" fill="#1d2433"/><rect x="34" y="200" width="22" height="30" fill="#5d646d"/></g>' for x in (120, 870))}</g>
<rect x="0" y="1240" width="1080" height="680" fill="#12161e"/>
<rect x="40" y="1240" width="1000" height="200" fill="#fff6d8" opacity="0.08"/>
<g transform="translate(-60 1180) scale(0.95)">{taxi_lado(0, 0, 1.0, "taxi14")}</g>
{chuva("chuva14", 70, 14)}
''')


def s15():
    return svg(f'''
<rect width="1080" height="1920" fill="#06080c"/>
<path d="M0 0 L 1080 0 L 1080 640 L 0 640 Z" fill="#111c30"/>
{gotas("gotas15", (40, 60, 1040, 600), 26, 15)}
<circle cx="540" cy="1300" r="560" fill="url(#verde)" opacity="0.45"/>
<g id="terco15" transform="translate(860 0)"><path d="M0 0 C -30 200 50 340 10 520" fill="none" stroke="#8a5a32" stroke-width="12" stroke-dasharray="2 18" stroke-linecap="round"/><path d="M-16 510 h52 M10 486 v74" stroke="#8a5a32" stroke-width="16" stroke-linecap="round"/></g>
{pose("telefone", 150, 760, 780)}
''')


CENAS = {"s01": s01, "s06": s06, "s07": s07, "s08": s08, "s12": s12, "s14": s14, "s15": s15}


def anim(nome, pid, t0, t1, pal, ini):
    d = round(t1 - t0, 3)
    q = lambda s: f"#{pid} {s}"
    j = []
    if nome == "s01":
        primeira = t0 < 1
        if primeira:  # o carro preto chega e para colado no táxi
            j += [f'tl.fromTo("{q("#suv")}", {{ x: 760 }}, {{ x: 0, duration: 1.6, ease: "power3.out", immediateRender: false }}, {t0});',
                  f'tl.fromTo("{q("#suv-freio")}", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.2, immediateRender: false }}, {t0 + 1.0});',
                  f'tl.fromTo("{q("#suv")}", {{ rotation: 0, transformOrigin: "50% 100%" }}, {{ rotation: -1, duration: 0.15, yoyo: true, repeat: 1, immediateRender: false }}, {t0 + 1.45});']
        j += [f'tl.fromTo("{q("#sinal-glow")}", {{ opacity: 1 }}, {{ opacity: 0.55, duration: 0.7, yoyo: true, repeat: {max(1, int(d / 0.7))}, ease: "sine.inOut", immediateRender: false }}, {t0});']
        if pid == "p18":  # o 3º jeito: zoom na viatura e círculo
            from cenas2 import VIATURA
            vx, vy, vs = VIATURA
            cx, cy = vx + 300 * vs, vy + 130 * vs
            tz = round(pal("Ou tem um terceiro", "escondido"), 3)
            j += [f'tl.fromTo("#{pid} svg", {{ scale: 1, x: 0, y: 0, transformOrigin: "0px 0px" }}, {{ scale: 2.2, x: {540 - cx * 2.2:.0f}, y: {760 - cy * 2.2:.0f}, duration: 0.7, ease: "power3.inOut", immediateRender: false }}, {round(tz - 0.35, 3)});',
                  f'tl.fromTo("{q("#circulo-viatura")}", {{ opacity: 0, scale: 1.7, transformOrigin: "50% 50%" }}, {{ opacity: 1, scale: 1, duration: 0.45, ease: "back.out(2)", immediateRender: false }}, {tz});']
    if nome == "s06":
        j += [f'tl.fromTo("{q("#luzes")}", {{ x: 0 }}, {{ x: -340, duration: 0.6, ease: "none", repeat: {max(1, int(d / 0.6))}, immediateRender: false }}, {t0});',
              f'tl.fromTo("{q("#led6")}", {{ opacity: 1 }}, {{ opacity: 0.15, duration: 0.35, yoyo: true, repeat: {int(d / 0.35)}, ease: "steps(1)", immediateRender: false }}, {round(t1 - 1.4, 3)});']
    if nome == "s07":
        j += [f'tl.fromTo("{q(".onda")}", {{ scaleY: 0.2, transformOrigin: "50% 50%" }}, {{ scaleY: 1.4, duration: 0.18, yoyo: true, repeat: {int(d / 0.18)}, stagger: {{ each: 0.05, from: "random" }}, ease: "sine.inOut", immediateRender: false }}, {t0});',
              f'tl.fromTo("{q("#led7")}", {{ opacity: 1 }}, {{ opacity: 0.2, duration: 0.3, yoyo: true, repeat: {int(d / 0.3)}, ease: "steps(1)", immediateRender: false }}, {t0});',
              f'tl.fromTo("{q("#terco7")}", {{ rotation: -5, transformOrigin: "50% 0%" }}, {{ rotation: 5, duration: 1.2, yoyo: true, repeat: {max(1, int(d / 1.2))}, ease: "sine.inOut", immediateRender: false }}, {t0});']
    if nome == "s08":
        j += [f'tl.fromTo("#{pid} image", {{ x: 0 }}, {{ x: 5, duration: 0.05, yoyo: true, repeat: 7, immediateRender: false }}, {round(pal("Problema dois", "nome"), 3)});']
    if nome == "s12":
        j += [f'tl.fromTo("{q("#suv12-vidro")}", {{ y: 0 }}, {{ y: 66, duration: 2.6, ease: "power1.inOut", immediateRender: false }}, {round(pal("O carro preto encostou", "vidro") - 0.2, 3)});',
              f'tl.fromTo("{q("#suv12-brasa")}", {{ opacity: 0.5 }}, {{ opacity: 1, duration: 0.5, yoyo: true, repeat: {max(1, int(d / 0.5))}, immediateRender: false }}, {t0});']
    if nome == "s14":
        j += [f'tl.fromTo("{q("#taxi14")}", {{ x: -300 }}, {{ x: 0, duration: 1.4, ease: "power2.out", immediateRender: false }}, {t0});',
              f'tl.fromTo("{q("#luz-posto")}", {{ opacity: 0.18 }}, {{ opacity: 0.1, duration: 0.08, yoyo: true, repeat: 3, immediateRender: false }}, {t0 + 1.8});']
    if nome == "s15":
        j += [f'tl.fromTo("#{pid} image", {{ y: 30 }}, {{ y: 0, duration: 0.8, ease: "power2.out", immediateRender: false }}, {t0});',
              f'tl.fromTo("{q("#terco15")}", {{ rotation: -5, transformOrigin: "50% 0%" }}, {{ rotation: 5, duration: 1.2, yoyo: true, repeat: {max(1, int(d / 1.2))}, ease: "sine.inOut", immediateRender: false }}, {t0});']
    import cenas
    for cid in ("chuva", "chuva8", "chuva12b", "chuva14"):
        if f'id="{cid}"' in CENAS[nome]():
            j.append(cenas.chuva_js(f"{pid} #{cid}", t0, t1))
    for gid in ("gotas6", "gotas15"):
        if f'id="{gid}"' in CENAS[nome]():
            j.append(f'tl.fromTo("#{pid} #{gid} .gota", {{ y: 0 }}, {{ y: 26, duration: {d}, ease: "power1.in", stagger: 0.03, immediateRender: false }}, {t0});')
    return j
