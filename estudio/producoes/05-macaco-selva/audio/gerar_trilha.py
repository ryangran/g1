"""Trilha de "Macaco na selva": tensão tribal 100 BPM (tambores, marimba, shaker)
+ ambiente de selva sintetizado (insetos, pássaros, água). 30 s.

Uso (na pasta do episódio): python3 audio/gerar_trilha.py   (requer numpy, soundfile)
"""
import os
import subprocess

import numpy as np
import soundfile as sf

SR = 44100
DUR = 30.0
BPM = 100
STEP = 60 / BPM / 4
N = int(DUR * SR)
rng = np.random.default_rng(5)
t_all = np.arange(N) / SR


def lowpass(x, fc):
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    return np.fft.irfft(X / np.sqrt(1 + (f / fc) ** 4), len(x))


def bandpass(x, lo, hi):
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    return np.fft.irfft(X * ((f > lo) & (f < hi)), len(x))


def add(buf, at, sig, gain=1.0):
    i = int(at * SR)
    if i >= len(buf):
        return
    j = min(len(buf), i + len(sig))
    buf[i:j] += sig[: j - i] * gain


def env(chaves):
    return np.interp(t_all, [k[0] for k in chaves], [k[1] for k in chaves])


def tambor(freq, dur=0.45, dec=9):
    k = np.arange(int(dur * SR)) / SR
    f = freq * (1 + 0.5 * np.exp(-k * 35))
    corpo = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-k * dec)
    pele = lowpass(rng.standard_normal(len(k)), 1500) * np.exp(-k * 60) * 0.25
    return corpo + pele


def shaker():
    n = int(0.07 * SR)
    k = np.arange(n) / SR
    return bandpass(rng.standard_normal(n), 5000, 11000) * np.sin(np.pi * k / 0.07) * 0.12


def marimba(freq, dur=0.5):
    k = np.arange(int(dur * SR)) / SR
    x = np.sin(2 * np.pi * freq * k) + 0.25 * np.sin(2 * np.pi * freq * 4 * k) * np.exp(-k * 30)
    return x * np.exp(-k * 7) * np.minimum(1, k / 0.002) * 0.3


comp = 16 * STEP
GRAVE = [0, 6, 10]
MEDIO = {3: 150, 8: 130, 13: 170, 14: 150}
ESCALA = [220.0, 261.63, 293.66, 329.63, 392.0]  # lá menor pentatônica
FRASE = [(0, 0), (2, 2), (4, 1), (6, 3), (8, 0), (10, 2), (12, 4), (14, 3)]

graves = np.zeros(N); medios = np.zeros(N); shk = np.zeros(N); mar = np.zeros(N)
c = 0
while c * comp < DUR:
    t0 = c * comp
    for s in GRAVE:
        add(graves, t0 + s * STEP, tambor(62, 0.6, 6))
    for s, f in MEDIO.items():
        add(medios, t0 + s * STEP, tambor(f, 0.3, 14), 0.5)
    for s in range(16):
        add(shk, t0 + s * STEP, shaker(), 1.0 if s % 2 == 0 else 0.55)
    oit = 1.0 if c % 2 == 0 else 1.189  # sobe meio passo nos compassos ímpares = tensão
    for s, n in FRASE:
        add(mar, t0 + s * STEP, marimba(ESCALA[n] * oit))
    c += 1

# drone grave de rio e perigo
drone = lowpass(sum(2 * ((t_all * f) % 1) - 1 for f in (55, 55.3, 82.4)), 180) * 0.25

# ambiente: insetos (chiado pulsando), pássaros (piados), água
insetos = bandpass(rng.standard_normal(N), 4000, 7000) * (0.5 + 0.5 * np.sin(2 * np.pi * 18 * t_all)) * 0.05
agua = lowpass(rng.standard_normal(N), 700) * 0.06
passaros = np.zeros(N)
for t0 in np.arange(0.4, DUR, 2.3) + rng.uniform(0, 0.8, len(np.arange(0.4, DUR, 2.3))):
    k = np.arange(int(0.18 * SR)) / SR
    f0 = rng.uniform(2200, 3400)
    pio = np.sin(2 * np.pi * np.cumsum(f0 + 900 * np.sin(2 * np.pi * 14 * k)) / SR) * np.sin(np.pi * k / 0.18) * 0.06
    add(passaros, t0, pio)
    add(passaros, t0 + 0.22, pio, 0.7)

# dinâmica: entra leve, cresce nos perigos, segura na escolha, corta no fecho
g_tamb = env([(0, 0.35), (5.3, 0.45), (7.2, 0.8), (9.8, 0.85), (18.2, 1.0), (18.3, 0.5), (23.9, 0.6), (24.0, 0.0), (30, 0)])
g_med = env([(0, 0), (7.1, 0), (7.2, 0.7), (18.2, 1.0), (18.3, 0.4), (23.9, 0.4), (24.0, 0), (30, 0)])
g_mar = env([(0, 0.8), (9.8, 0.8), (18.3, 0.9), (24.0, 0.9), (24.05, 0.6), (29.0, 0.5), (30, 0)])
g_drone = env([(0, 0.2), (5.3, 0.5), (7.2, 1.0), (18.3, 0.7), (24, 0.4), (30, 0.2)])
g_amb = env([(0, 1.0), (24, 1.0), (30, 0.6)])

mix = (graves * g_tamb + medios * g_med + shk * g_tamb * 0.8 + mar * g_mar + drone * g_drone
       + (insetos + agua + passaros) * g_amb)
# fade final
mix *= env([(0, 1), (29.2, 1), (30, 0)])
st = np.stack([mix, np.roll(mix, 11)], 1)
st[:, 1] += passaros * 0.3
st = np.tanh(st * 1.3) / np.tanh(1.3)
st *= 0.85 / np.abs(st).max()
os.makedirs("build", exist_ok=True)
sf.write("build/trilha.wav", st.astype(np.float32), SR)
subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", "build/trilha.wav", "-c:a", "libmp3lame", "-b:a", "192k", "assets/audio/trilha.mp3"], check=True)
print("ok", st.shape[0] / SR)
