"""Trilha de "Um dia na vida": marimba + baixo + bateria leve, 1 compasso por pose.

Gera assets/audio/trilha.mp3 (intermediário em build/). Uso: python3 audio/gerar_trilha.py
"""
import os
import subprocess

import numpy as np
import soundfile as sf

SR = 44100
COMPASSO = 2.65            # uma pose = um compasso de 4 tempos
BEAT = COMPASSO / 4        # ≈ 90,6 BPM
DUR = 21.6
N = int(DUR * SR)
rng = np.random.default_rng(6)
t_all = np.arange(N) / SR


def add(buf, at, sig, g=1.0):
    i = int(at * SR)
    if i >= len(buf):
        return
    j = min(len(buf), i + len(sig))
    buf[i:j] += sig[: j - i] * g


def lowpass(x, fc):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR)
    return np.fft.irfft(X / np.sqrt(1 + (f / fc) ** 4), len(x))


def marimba(freq, dur=0.9):
    k = np.arange(int(dur * SR)) / SR
    s = np.sin(2 * np.pi * freq * k) * np.exp(-k * 5) + 0.35 * np.sin(2 * np.pi * freq * 4 * k) * np.exp(-k * 18) + 0.15 * np.sin(2 * np.pi * freq * 10 * k) * np.exp(-k * 40)
    return s * np.minimum(1, k / 0.002) * 0.32


def pad(freqs, dur):
    k = np.arange(int(dur * SR)) / SR
    s = sum(np.sin(2 * np.pi * f * k + i) + 0.3 * np.sin(2 * np.pi * f * 2.003 * k) for i, f in enumerate(freqs))
    env = np.minimum(1, k / 0.5) * np.minimum(1, (dur - k) / 0.5)
    return lowpass(s, 1800) * env * 0.05


def baixo(freq, dur):
    k = np.arange(int(dur * SR)) / SR
    return np.sin(2 * np.pi * freq * k) * np.exp(-k * 2.5) * np.minimum(1, k / 0.01) * 0.38


def kick():
    k = np.arange(int(0.35 * SR)) / SR
    return np.sin(2 * np.pi * np.cumsum(48 + 100 * np.exp(-k * 30)) / SR) * np.exp(-k * 9) * 0.8


def clap():
    k = np.arange(int(0.2 * SR)) / SR
    return lowpass(rng.standard_normal(len(k)), 4000) * np.exp(-k * 25) * 0.25


def shaker():
    k = np.arange(int(0.07 * SR)) / SR
    x = rng.standard_normal(len(k)); x = x - lowpass(x, 5000)
    return x * np.exp(-k * 60) * 0.08


def nota(n):  # n = semitons a partir de C4
    return 261.63 * 2 ** (n / 12)


# C – Am – F – G – C – Am – F – G(→C)
ACORDES = [(0, [0, 4, 7]), (-3, [-3, 0, 4]), (-7, [-7, -3, 0]), (-5, [-5, -1, 2])] * 2
MELODIA = [[7, 4, 7, 9], [9, 7, 4, 2], [0, 2, 4, 5], [7, 5, 4, 2], [7, 9, 12, 9], [7, 4, 7, 12], [9, 12, 14, 12], [12, 16, 19, 24]]

musica = np.zeros(N)
for c, ((raiz, acorde), mel) in enumerate(zip(ACORDES, MELODIA)):
    t0 = c * COMPASSO
    add(musica, t0, pad([nota(x) for x in acorde], COMPASSO + 0.3))
    for b, n in enumerate(mel):  # marimba em colcheias: nota do tempo + arpejo no contratempo
        add(musica, t0 + b * BEAT, marimba(nota(n + 12)))
        add(musica, t0 + b * BEAT + BEAT / 2, marimba(nota(acorde[b % 3] + 12)), 0.55)
    if c >= 2:  # o dia começa de verdade às 8h
        add(musica, t0, baixo(nota(raiz - 24), BEAT * 2))
        add(musica, t0 + BEAT * 2, baixo(nota(raiz - 24 + 7), BEAT * 2))
        for b in range(4):
            add(musica, t0 + b * BEAT, kick(), 1.0 if b in (0, 2) else 0.0)
            add(musica, t0 + b * BEAT, clap(), 1.0 if b in (1, 3) else 0.0)
        for s in range(8):
            add(musica, t0 + s * BEAT / 2, shaker())
# final: acorde de C sustentado e brilho
fim = 7 * COMPASSO
add(musica, fim + COMPASSO, pad([nota(x) for x in (0, 4, 7, 12)], 2.0), 2.0)
for n in (12, 16, 19, 24):
    add(musica, fim + COMPASSO, marimba(nota(n + 12), 1.8), 0.8)
add(musica, fim + COMPASSO, kick())

env = np.interp(t_all, [0, 0.05, 2.0, 2.65, DUR - 0.6, DUR], [0.55, 0.55, 0.55, 0.85, 0.9, 0])  # madrugada mais baixa
mix = musica * env
mix = np.tanh(mix * 1.3) / np.tanh(1.3)
mix *= 0.8 / np.abs(mix).max()
os.makedirs("build", exist_ok=True)
sf.write("build/trilha.wav", np.stack([mix, np.roll(mix, 7)], 1).astype(np.float32), SR)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", "build/trilha.wav", "-c:a", "libmp3lame", "-b:a", "192k", "assets/audio/trilha.mp3"], check=True)
print("ok")
