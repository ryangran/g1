"""Recorta as poses oficiais do Clóvis (docs/clovis-folha.jpg e docs/clovis-poses.webp) em assets/clovis/*.png.

O fundo cinza liso ligado às bordas vira transparente. Cada pose sai em duas versões:
  <nome>.png        cores originais (capas, site)
  <nome>-noite.png  com a correção de cor da madrugada usada nas cenas (mais escuro e mais frio)
Uso (na pasta do episódio): python3 tools/recortar_clovis.py
"""
import collections
from PIL import Image, ImageEnhance, ImageFilter

FOLHAS = {
    "docs/clovis-folha.jpg": {  # 2000×1116
        "frente-susto": (40, 60, 560, 1090),
        "tres-quartos": (600, 60, 1040, 1090),
        "lado": (1080, 60, 1360, 1090),
        "rosto-sorriso": (1345, 20, 1638, 425),
        "rosto-preocupado": (1660, 20, 1995, 425),
    },
    "docs/clovis-poses.webp": {  # 1024×572
        "dirigindo": (0, 0, 425, 300),
        "retrovisor": (420, 0, 724, 214),
        "susto-suor": (705, 22, 1024, 572),
        "segura-bilhete": (18, 300, 256, 572),
        "telefone": (262, 262, 524, 572),
        "correndo": (500, 218, 742, 548),
    },
}


def recortar(src, fundo):
    w, h = src.size
    px = src.load()
    mask = Image.new("L", (w, h), 255)
    mp = mask.load()
    fila = collections.deque([(x, 0) for x in range(w)] + [(x, h - 1) for x in range(w)] + [(0, y) for y in range(h)] + [(w - 1, y) for y in range(h)])
    visto = set()
    while fila:
        x, y = fila.popleft()
        if (x, y) in visto or not (0 <= x < w and 0 <= y < h):
            continue
        visto.add((x, y))
        r, g, b = px[x, y]
        if abs(r - fundo) < 22 and abs(g - fundo) < 22 and abs(b - fundo) < 24 and max(r, g, b) - min(r, g, b) < 16:
            mp[x, y] = 0
            fila.extend([(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)])
    mask = limpar(mask.filter(ImageFilter.MinFilter(3)))
    mask = mask.filter(ImageFilter.GaussianBlur(1.0))
    out = src.convert("RGBA")
    out.putalpha(mask)
    return out.crop(out.getbbox())


def limpar(mask, minimo=0.15):
    """Mantém só as partes grandes (o personagem e seus objetos); tira pedaços das poses vizinhas que entraram no recorte."""
    w, h = mask.size
    mp = mask.load()
    vistos, partes = set(), []
    for y0 in range(0, h, 2):
        for x0 in range(0, w, 2):
            if mp[x0, y0] < 128 or (x0, y0) in vistos:
                continue
            fila, parte = collections.deque([(x0, y0)]), []
            vistos.add((x0, y0))
            while fila:
                x, y = fila.popleft()
                parte.append((x, y))
                for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                    if 0 <= nx < w and 0 <= ny < h and (nx, ny) not in vistos and mp[nx, ny] >= 128:
                        vistos.add((nx, ny))
                        fila.append((nx, ny))
            partes.append(parte)
    maior = max(len(p) for p in partes)
    novo = Image.new("L", (w, h), 0)
    np_ = novo.load()
    for p in partes:
        if len(p) >= minimo * maior:
            for x, y in p:
                np_[x, y] = 255
    return novo


def noite(img):
    rgb = ImageEnhance.Brightness(img.convert("RGB")).enhance(0.74)
    r, g, b = rgb.split()
    rgb = Image.merge("RGB", (r.point(lambda v: v * 0.86), g.point(lambda v: v * 0.93), b.point(lambda v: min(255, v * 1.06 + 6))))
    rgb = ImageEnhance.Contrast(rgb).enhance(1.08)
    out = rgb.convert("RGBA")
    out.putalpha(img.getchannel("A"))
    return out


for arq, poses in FOLHAS.items():
    folha = Image.open(arq).convert("RGB")
    fundo = folha.getpixel((5, folha.height - 5))[0]
    for nome, caixa in poses.items():
        p = recortar(folha.crop(caixa), fundo)
        if nome == "segura-bilhete":  # cobre o "LOTTERY" em inglês com a cor do papel do bilhete
            from PIL import ImageDraw
            ImageDraw.Draw(p).polygon([(171, 128), (212, 123), (214, 138), (172, 142)], fill=(238, 226, 170, 255))
        p.save(f"assets/clovis/{nome}.png")
        noite(p).save(f"assets/clovis/{nome}-noite.png")
        print(nome, p.size)
