"""Cenas novas da Parte 6 (o 3º jeito venceu: o vídeo do posto).

s61  lotérica: o Clóvis levanta o celular na frente do Seu Antônio
s62  o vídeo em tela cheia (interior do posto, o comprador oferecendo) com a interface de vídeo
s63  o vídeo continua: porta do posto, o Rodrigo falando com o comprador
s64  close do Seu Antônio assistindo
s65  pela janela da lotérica: o táxi com a mala no banco de trás (o 3º jeito desta parte)
s66  DEVOLVE: o Clóvis entrega o bilhete
s67  SEGUE: o Clóvis sai correndo atrás do Rodrigo
"""
from cenas import K, O, O4, homem_busto, pose, svg, taxi_lado
import cenas
import cenas2
import cenas3
import cenas4
import cenas5

TAXI_JANELA = (457, 1190)   # centro da mala vista pela janela (3º jeito); zoom e círculo usam isso
ZOOM6 = "p10"


def video_ui(tc="00:14", pct=0.42, cid="vd"):
    """Moldura de vídeo sendo assistido: REC, tempo e barra de progresso."""
    return f'''<g id="{cid}">
  <rect x="0" y="0" width="1080" height="170" fill="#000" opacity="0.6"/>
  <rect x="0" y="1750" width="1080" height="170" fill="#000" opacity="0.6"/>
  <circle id="{cid}-rec" cx="80" cy="92" r="18" fill="#ff2b20"/>
  <text x="124" y="106" font-family="JetBrains Mono, monospace" font-size="40" fill="#f2f2f2">VÍDEO DO POSTO</text>
  <text x="1000" y="106" font-family="JetBrains Mono, monospace" font-size="40" fill="#cfcfd6" text-anchor="end">{tc}</text>
  <rect x="60" y="1836" width="960" height="12" rx="6" fill="#ffffff" opacity="0.28"/>
  <rect id="{cid}-prog" x="60" y="1836" width="{int(960 * pct)}" height="12" rx="6" fill="#fff"/>
  <circle cx="{60 + int(960 * pct)}" cy="1842" r="16" fill="#fff"/>
</g>'''


def s61():
    cel = '''<g id="cel61"><g transform="translate(560 1330) rotate(-6)">
  <rect x="-130" y="-220" width="260" height="440" rx="30" fill="#0d0d10" stroke="#120f0c" stroke-width="7"/>
  <rect x="-112" y="-198" width="224" height="396" rx="16" fill="#2a2f3a"/>
  <rect x="-112" y="-198" width="224" height="150" fill="#1b2433"/>
  <circle cx="-72" cy="-160" r="13" fill="#ff2b20"/>
  <path d="M-30 -10 L 60 40 L -30 90 Z" fill="#f2f2f2" opacity="0.9"/>
</g></g>'''
    return cenas5.parede(f'''
<rect x="0" y="926" width="1080" height="1000" fill="#121a28"/>
<g id="clovis61">{pose("telefone", 20, 880, 580)}</g>
<g id="antonio61">{cenas5.seu_antonio(820, 1120, 1.0, "sa61")}</g>
<path d="M0 1520 L 1080 1520 L 1080 1920 L 0 1920 Z" fill="#c9ced6" {O}/>
<path d="M0 1520 L 1080 1520 L 1080 1556 L 0 1556 Z" fill="#e8ecf1" {O4}/>
{cel}
''')


def s62():
    """O vídeo: o interior do posto da Parte 3, visto pelo celular."""
    base = cenas3.s31()
    return base.replace("</svg>", video_ui("00:14", 0.42, "vd62") + "</svg>", 1)


def s63():
    """O vídeo continua: a porta do posto, o Rodrigo falando com o comprador."""
    rodrigo = f'<g id="rodrigo63">{homem_busto(330, 1180, 0.85, "rd63", telefone=False)}</g>'
    comprador = f'<g id="comp63">{cenas3.comprador(760, 1180, 0.85, "cp63")}</g>'
    base = cenas2.s14()
    base = base.replace('{chuva', '{chuva')  # mantém a chuva da cena original
    corpo = base.replace("</svg>", rodrigo + comprador + video_ui("00:41", 0.93, "vd63") + "</svg>", 1)
    return corpo


def s64():
    return cenas5.parede(f'''
<rect x="0" y="700" width="1080" height="1220" fill="#121a28"/>
<circle id="luz64" cx="540" cy="1150" r="520" fill="url(#poste)" opacity="0.25"/>
<g id="antonio64">{cenas5.seu_antonio(540, 1120, 2.0, "sa64")}</g>
''')


def s65():
    """Pela janela da lotérica: o táxi parado com a mala no banco de trás."""
    jx, jy = TAXI_JANELA
    return cenas5.parede(f'''
<rect x="0" y="926" width="1080" height="1000" fill="#121a28"/>
<rect x="90" y="860" width="900" height="620" rx="16" fill="#0a1222" stroke="#39455c" stroke-width="12"/>
<rect x="120" y="890" width="840" height="560" fill="#0e1726"/>
<g id="taxi65" transform="translate(190 1150) scale(0.58)">{taxi_lado(0, 0, 1.0, "tx65")}</g>
<g id="mala65" transform="translate({jx} {jy}) scale(0.30)">{cenas4.mala(0, 0, False, "ml65")}</g>
<circle id="brilho-mala" cx="{jx}" cy="{jy - 20}" r="120" fill="url(#poste)" opacity="0"/>
<circle id="circulo-mala" cx="{jx}" cy="{jy - 20}" r="112" fill="none" stroke="#ffd23a" stroke-width="14" opacity="0"/>
<path d="M90 1480 L 990 1480" stroke="#39455c" stroke-width="12"/>
''')


def s66():
    return cenas5.parede(f'''
<rect x="0" y="926" width="1080" height="1000" fill="#121a28"/>
<g id="clovis66">{pose("segura-bilhete", 40, 880, 700)}</g>
<g id="antonio66">{cenas5.seu_antonio(840, 1160, 1.0, "sa66")}</g>
<path d="M0 1560 L 1080 1560 L 1080 1920 L 0 1920 Z" fill="#c9ced6" {O}/>
''')


def s67():
    return cenas3.s34()


CENAS = {"s61": s61, "s62": s62, "s63": s63, "s64": s64, "s65": s65, "s66": s66, "s67": s67}


def anim(nome, pid, t0, t1, pal, ini):
    d = round(t1 - t0, 3)
    q = lambda s: f"#{pid} {s}"
    j = []
    if nome == "s61":
        j += [f'tl.fromTo("{q("#cel61")}", {{ y: 160, rotation: -16, opacity: 0 }}, {{ y: 0, rotation: -6, opacity: 1, duration: 0.6, ease: "power3.out", immediateRender: false }}, {t0});',
              f'tl.fromTo("{q("#antonio61")}", {{ x: 40, opacity: 0.5 }}, {{ x: 0, opacity: 1, duration: 0.7, ease: "power2.out", immediateRender: false }}, {t0 + 0.2});']
    if nome in ("s62", "s63"):
        cid = "vd62" if nome == "s62" else "vd63"
        j += [f'tl.fromTo("{q(f"#{cid}-rec")}", {{ opacity: 1 }}, {{ opacity: 0.15, duration: 0.45, yoyo: true, repeat: {max(1, int(d / 0.45))}, ease: "steps(1)", immediateRender: false }}, {t0});',
              f'tl.fromTo("{q(f"#{cid}-prog")}", {{ scaleX: 0.92, transformOrigin: "0% 50%" }}, {{ scaleX: 1, duration: {d}, ease: "none", immediateRender: false }}, {t0});']
    if nome == "s62":
        j.append(f'tl.fromTo("{q("#comprador31")}", {{ x: 0 }}, {{ x: -26, duration: {min(d, 2.0)}, ease: "power1.inOut", immediateRender: false }}, {t0});')
    if nome == "s63":
        j += [f'tl.fromTo("{q("#rodrigo63")}", {{ opacity: 0, x: -40 }}, {{ opacity: 1, x: 0, duration: 0.5, ease: "power3.out", immediateRender: false }}, {t0 + 0.15});',
              f'tl.fromTo("{q("#comp63")}", {{ opacity: 0, x: 40 }}, {{ opacity: 1, x: 0, duration: 0.5, ease: "power3.out", immediateRender: false }}, {t0 + 0.15});',
              cenas.chuva_js(f"{pid} #chuva14", t0, t1)]
    if nome == "s64":
        j.append(f'tl.fromTo("{q("#antonio64")}", {{ scale: 1.0, y: 20, transformOrigin: "50% 100%" }}, {{ scale: 1.06, y: 0, duration: {d}, ease: "none", immediateRender: false }}, {t0});')
    if nome == "s65":
        tz = round(pal("Ou tem", "escondido"), 3)
        jx, jy = TAXI_JANELA
        j += [f'tl.fromTo("{q("#brilho-mala")}", {{ opacity: 0 }}, {{ opacity: 0.55, duration: 0.6, yoyo: true, repeat: 3, immediateRender: false }}, {t0 + 0.2});']
        if pid == ZOOM6:
            j += [f'tl.fromTo("#{pid} svg", {{ scale: 1, x: 0, y: 0, transformOrigin: "0px 0px" }}, {{ scale: 2.0, x: {540 - jx * 2.0:.0f}, y: {860 - (jy - 20) * 2.0:.0f}, duration: 0.7, ease: "power3.inOut", immediateRender: false }}, {round(tz - 0.35, 3)});',
                  f'tl.fromTo("{q("#circulo-mala")}", {{ opacity: 0, scale: 1.7, transformOrigin: "50% 50%" }}, {{ opacity: 1, scale: 1, duration: 0.45, ease: "back.out(2)", immediateRender: false }}, {tz});']
    if nome == "s66":
        j.append(f'tl.fromTo("{q("#clovis66")}", {{ x: -40, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.5, ease: "power3.out", immediateRender: false }}, {t0});')
    if nome == "s67":
        j += [f'tl.fromTo("{q("#corre")}", {{ x: 0, y: 0 }}, {{ x: 130, y: -12, duration: {d}, ease: "power1.in", immediateRender: false }}, {t0});',
              f'tl.fromTo("{q("#saida-glow")}", {{ opacity: 1 }}, {{ opacity: 0.5, duration: 0.5, yoyo: true, repeat: {max(1, int(d / 0.5))}, immediateRender: false }}, {t0});']
    return [x for x in j if x]
