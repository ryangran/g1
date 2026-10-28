"""Trilha de "Proibido Dançar": funk eletrônico 144 BPM + efeitos sintetizados.

Gera assets/audio/trilha.mp3. Os SFX prontos (impacto, whoosh, riser, pop)
ficam como <audio> separados no index.html, editáveis no Studio.

Uso (na pasta do episódio): python3 audio/gerar_trilha.py   (requer numpy, soundfile)
"""
import os

import numpy as np
import soundfile as sf

SR = 44100
DUR = 38.5
BPM = 144
BEAT = 60 / BPM
STEP = BEAT / 4  # semicolcheia
N = int(DUR * SR)
rng = np.random.default_rng(144)
t_all = np.arange(N) / SR


def lowpass(x, fc):
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    return np.fft.irfft(X / np.sqrt(1 + (f / fc) ** 4), len(x))


def highpass(x, fc):
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    return np.fft.irfft(X * (1 - 1 / np.sqrt(1 + (f / fc) ** 4)), len(x))


def add(buf, at, sig, gain=1.0):
    i = int(at * SR)
    if i >= len(buf) or i + len(sig) <= 0:
        return
    j = min(len(buf), i + len(sig))
    buf[i:j] += sig[: j - i] * gain


# ---------- instrumentos ----------
def kick():
    k = np.arange(int(0.42 * SR)) / SR
    f = 45 + 110 * np.exp(-k * 28)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-k * 7.5) * 1.0


def clap():
    n = int(0.25 * SR)
    k = np.arange(n) / SR
    nz = highpass(lowpass(rng.standard_normal(n), 3800), 900)
    env = np.exp(-k * 22)
    for d in (0.0, 0.011, 0.022):
        env += np.exp(-np.maximum(k - d, 0) * 120) * (k >= d) * 0.6
    return nz * env * 0.5


def hat(aberto=False):
    n = int((0.16 if aberto else 0.045) * SR)
    k = np.arange(n) / SR
    return highpass(rng.standard_normal(n), 7000) * np.exp(-k * (18 if aberto else 80)) * 0.18


def tom(freq):
    k = np.arange(int(0.22 * SR)) / SR
    f = freq * (1 + 0.6 * np.exp(-k * 30))
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-k * 13) * 0.55


def baixo(freq, dur):
    n = int(dur * SR)
    k = np.arange(n) / SR
    saw = 2 * ((k * freq) % 1) - 1
    sub = np.sin(2 * np.pi * freq * k)
    env = np.minimum(1, k / 0.005) * np.exp(-k * 3.5)
    x = saw * 0.5 + sub
    a = np.exp(-k * 9)  # filtro que fecha: brilho no ataque, escuro na cauda
    return (lowpass(x, 1100) * a + lowpass(x, 260) * (1 - a)) * env * 0.42


def pluck(freq, dur):
    n = int(dur * SR)
    k = np.arange(n) / SR
    sq = np.sign(np.sin(2 * np.pi * freq * k)) * 0.5 + np.sin(2 * np.pi * freq * 2 * k) * 0.3
    a = np.exp(-k * 6)
    return (lowpass(sq, 2800) * a + lowpass(sq, 500) * (1 - a)) * np.exp(-k * 7) * 0.22


# ---------- padrão (16 semicolcheias por compasso) ----------
KICK = [0, 3, 6, 10]          # tamborzão estilizado
CLAP = [4, 12]
TOMS = {7: 180, 9: 150, 14: 120}
NOTA = {"A1": 55.0, "C2": 65.41, "D2": 73.42, "E2": 82.41, "G1": 49.0, "A2": 110.0}
BAIXO = [(0, "A1", 2), (3, "A1", 1), (6, "C2", 2), (10, "G1", 2), (13, "A1", 2)]
LEAD = [(0, 440.0), (3, 523.25), (6, 587.33), (8, 659.25), (11, 587.33), (14, 523.25)]

bateria = np.zeros(N)
baixos = np.zeros(N)
melodia = np.zeros(N)
compasso = 16 * STEP
n_comp = int(DUR / compasso) + 1
for c in range(n_comp):
    t0 = c * compasso
    for s in KICK:
        add(bateria, t0 + s * STEP, kick())
    for s in CLAP:
        add(bateria, t0 + s * STEP, clap())
    for s, f in TOMS.items():
        add(bateria, t0 + s * STEP, tom(f), 0.8)
    for s in range(0, 16, 2):
        add(bateria, t0 + s * STEP, hat(aberto=(s % 8 == 6)))
    for s, n, d in BAIXO:
        add(baixos, t0 + s * STEP, baixo(NOTA[n], d * STEP + 0.05))
    for s, f in LEAD:
        add(melodia, t0 + s * STEP, pluck(f * (1.5 if c % 2 else 1.0), 2 * STEP))

musica_cheia = bateria + baixos + melodia * 0.0
musica_lead = bateria + baixos + melodia
abafada = lowpass(bateria + baixos, 380) * 1.4


def env(chaves):
    """Envelope por chaves [(t, valor)], interpolação linear."""
    ts = np.array([k[0] for k in chaves])
    vs = np.array([k[1] for k in chaves])
    return np.interp(t_all, ts, vs)


# quem toca quando (o "na cabeça do Bolt" é a versão aberta)
g_abaf = env([(0, 0.55), (6.2, 0.55), (6.25, 0), (7.55, 0), (7.6, 0.4), (12.0, 0.4), (12.08, 0), (38.5, 0)])
g_cheia = env([(0, 0), (6.2, 0), (6.25, 0.75), (7.5, 0.75), (7.56, 0), (12.03, 0), (12.08, 0.8), (14.9, 0.85), (15.0, 0), (38.5, 0)])
g_lead = env([(0, 0), (14.95, 0), (15.0, 0.9), (18.88, 0.95), (18.9, 0), (31.2, 0), (31.25, 1.0), (37.9, 1.0), (38.45, 0)])
musica = abafada * g_abaf + musica_cheia * g_cheia + musica_lead * g_lead

# ---------- efeitos sintetizados ----------
sfx = np.zeros(N)

# arranhão de disco no flagra (18.9)
n = int(0.55 * SR)
k = np.arange(n) / SR
pitch = 900 * (1 - k / 0.55) ** 2 + 120
scr = lowpass(highpass(rng.standard_normal(n), 300), 2500) * np.sin(2 * np.pi * np.cumsum(pitch) / SR) * np.exp(-k * 4)
add(sfx, 18.88, scr, 0.9)

# passos pesados e metálicos do chefe (aproximação: 2 passos por ciclo de "Walking")
def passo(peso):
    m = int(0.5 * SR)
    q = np.arange(m) / SR
    thump = np.sin(2 * np.pi * np.cumsum(70 + 60 * np.exp(-q * 30)) / SR) * np.exp(-q * 12)
    clank = sum(np.sin(2 * np.pi * f * q) for f in (523, 811, 1307)) * np.exp(-q * 22) * 0.18
    return (thump + clank) * peso

for t0, t1, vel, peso in [(0.3, 7.0, 0.9, 0.12), (11.4, 15.6, 0.9, 0.1), (17.4, 18.75, 0.9, 0.25), (19.9, 23.35, 0.62, 0.85)]:
    t = t0
    while t < t1:
        add(sfx, t, passo(peso))
        t += 0.479 / vel

# zumbido grave de tensão (do flagra até a tábua cair)
dr = lowpass(sum(2 * ((t_all * f) % 1) - 1 for f in (55, 55.4, 82.6)), 160)
sfx += dr * env([(0, 0), (19.4, 0), (21.0, 0.10), (23.9, 0.16), (24.0, 0.05), (28.6, 0.08), (29.5, 0.0)])

# neon: chiado elétrico ao piscar e zumbido aceso
buzz = lowpass(np.sign(np.sin(2 * np.pi * 120 * t_all)) * 0.5 + highpass(rng.standard_normal(N), 3000) * 0.3, 3000)
sfx += buzz * env([(0, 0), (36.19, 0), (36.2, 0.10), (36.35, 0.10), (36.36, 0), (36.49, 0), (36.5, 0.10), (36.6, 0.10), (36.61, 0), (36.74, 0), (36.75, 0.06), (38.5, 0.05)])

mix = musica * 0.8 + sfx
mix = np.stack([mix, mix], 1)
# leve abertura estéreo nos hats/melodia
mix[:, 1] = np.roll(mix[:, 1], 9)
os.makedirs("build", exist_ok=True)
mix = np.tanh(mix * 1.2) / np.tanh(1.2)
mix *= 0.85 / np.abs(mix).max()
sf.write("build/trilha.wav", mix.astype(np.float32), SR)
import subprocess
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", "build/trilha.wav", "-c:a", "libmp3lame", "-b:a", "192k", "assets/audio/trilha.mp3"], check=True)
print("ok", mix.shape[0] / SR)
