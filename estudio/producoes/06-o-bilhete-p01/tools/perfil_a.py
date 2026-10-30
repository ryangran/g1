"""Foto de perfil (opção A): o rosto de meio sorriso da folha docs/clovis-folha.jpg, recortado do fundo cinza,
sobre azul-noite com halo amarelo. Saída: renders/perfil-instagram-a.png (1080×1080)."""
import collections
import sys
from PIL import Image, ImageDraw, ImageFilter

src = Image.open("docs/clovis-folha.jpg").convert("RGB").crop((1345, 20, 1638, 425))
w, h = src.size
px = src.load()
mask = Image.new("L", (w, h), 255)
mp = mask.load()
fila = collections.deque([(x, 0) for x in range(w)] + [(0, y) for y in range(h)] + [(w - 1, y) for y in range(h)])
visto = set()
while fila:  # fundo cinza ligado às bordas vira transparente
    x, y = fila.popleft()
    if (x, y) in visto or not (0 <= x < w and 0 <= y < h):
        continue
    visto.add((x, y))
    r, g, b = px[x, y]
    if abs(r - 212) < 20 and abs(g - 212) < 20 and abs(b - 212) < 22 and max(r, g, b) - min(r, g, b) < 14:
        mp[x, y] = 0
        fila.extend([(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)])
mask = mask.filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(1.2))
cab = src.convert("RGBA")
cab.putalpha(mask)
S = 2.6
cab = cab.resize((int(w * S), int(h * S)), Image.LANCZOS).filter(ImageFilter.UnsharpMask(2, 80, 2))
N = 1080
fundo = Image.new("RGB", (N, N), (10, 15, 24))
d = ImageDraw.Draw(fundo)
for r in range(560, 0, -4):
    t = r / 560
    d.ellipse((540 - r, 470 - r, 540 + r, 470 + r), fill=(int(42 * (1 - t) + 10 * t), int(59 * (1 - t) + 15 * t), int(86 * (1 - t) + 24 * t)))
halo = Image.new("L", (N, N), 0)
ImageDraw.Draw(halo).ellipse((140, 80, 940, 880), fill=120)
fundo.paste(Image.new("RGB", (N, N), (255, 210, 58)), (0, 0), halo.filter(ImageFilter.GaussianBlur(90)))
ImageDraw.Draw(fundo).ellipse((175, 105, 905, 835), outline=(255, 210, 58), width=12)
fundo.paste(cab, ((N - cab.width) // 2 + 20, N - cab.height + 60), cab)
fundo.save("renders/perfil-instagram-a.png")
if len(sys.argv) > 1:  # prévia redonda
    c = Image.new("RGB", (N, N), "white")
    m = Image.new("L", (N, N), 0)
    ImageDraw.Draw(m).ellipse((0, 0, N - 1, N - 1), fill=255)
    c.paste(fundo, (0, 0), m)
    c.resize((360, 360)).save(sys.argv[1])
