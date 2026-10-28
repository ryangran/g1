"""Áudio de "Apagão": música (pizzicato sorrateiro) e foley sintetizado + vozes.

Saída: assets/audio/musica.mp3 e assets/audio/foley.mp3 (alinhados ao tempo do vídeo, 26 s).
Vozes: build/voz/*.wav do Kokoro (pf_dora), aceleradas para virar voz de inseto.
Uso (na pasta do episódio): python3 audio/gerar_audio.py
"""
import os
import subprocess

import numpy as np
import soundfile as sf

SR = 44100
DUR = 26.0
N = int(DUR * SR)
rng = np.random.default_rng(1)
T = np.arange(N) / SR


def add(buf, at, sig, g=1.0):
    i = int(at * SR)
    if i >= len(buf) or i + len(sig) < 0:
        return
    a = max(0, -i); i = max(0, i)
    j = min(len(buf), i + len(sig) - a)
    buf[i:j] += sig[a:a + j - i] * g


def lp(x, fc):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR)
    return np.fft.irfft(X / np.sqrt(1 + (f / fc) ** 4), len(x))


def hp(x, fc):
    return x - lp(x, fc)


def env(n, a=0.005, d=0.2):
    k = np.arange(n) / SR
    return np.minimum(1, k / a) * np.exp(-k / d)


# ---------------- música ----------------
BPM = 100; B = 60 / BPM
musica = np.zeros(N)


def pizz(f, dur=0.35, g=0.3):
    n = int(dur * SR); k = np.arange(n) / SR
    s = np.sin(2 * np.pi * f * k) + 0.4 * np.sin(2 * np.pi * 2 * f * k) + 0.2 * np.sin(2 * np.pi * 3 * f * k)
    return lp(s, 2500) * env(n, 0.003, 0.09) * g


def fagote(f, dur, g=0.12):
    n = int(dur * SR); k = np.arange(n) / SR
    s = 2 * ((k * f) % 1) - 1
    return lp(s, 900) * np.minimum(1, k / 0.02) * np.minimum(1, (dur - k) / 0.04) * g


def cordas(f, dur, g):
    n = int(dur * SR); k = np.arange(n) / SR
    s = sum(2 * ((k * f * d + i * 0.3) % 1) - 1 for i, d in enumerate((1, 1.004, 0.996, 2.002)))
    trem = 0.7 + 0.3 * np.sin(2 * np.pi * 9 * k)
    return lp(s, 2200) * trem * g


nota = lambda n: 293.66 * 2 ** (n / 12)  # D4 = 0
INI, FIM = 6.45, 18.6
# baixo e melodia "na ponta dos pés" (D menor), colcheias
baixo = [-12, -5, -12, -5, -14, -7, -10, -5]
mel = [0, None, 3, 5, None, 3, 0, None, 7, 5, 3, None, 2, 3, 2, None]
t = INI; i = 0
while t < FIM - 0.05:
    if i % 2 == 0:
        add(musica, t, pizz(nota(baixo[(i // 2) % 8]) , 0.4, 0.42))
    m = mel[i % 16]
    if m is not None and t < 13.2:
        add(musica, t, pizz(nota(m + 12), 0.25, 0.22))
    if t >= 10.2 and i % 4 == 0:  # fagote entra com o prédio
        add(musica, t, fagote(nota(baixo[(i // 2) % 8] - 12 + 12), B * 1.6))
    t += B / 2; i += 1
# crescendo de cordas da cidade ao céu (13,2 → 18,6), corte seco no clique da lua
for f, g in ((nota(-12), 0.05), (nota(-5), 0.04), (nota(0), 0.035), (nota(3), 0.03)):
    seg = cordas(f, FIM - 13.2, g)
    seg *= np.linspace(0.15, 1.6, len(seg)) ** 1.5
    add(musica, 13.2, seg)
musica[int(FIM * SR):] = 0
# "plim" final de 2 notas
add(musica, 25.7, pizz(nota(12), 0.4, 0.35)); add(musica, 25.82, pizz(nota(19), 0.6, 0.35))

# ---------------- foley ----------------
foley = np.zeros(N)
# zumbido da lâmpada + tic-tac (0–6,3: até o abajur apagar)
hum = lp(np.sin(2 * np.pi * 120 * T) + 0.4 * np.sin(2 * np.pi * 240 * T), 600) * 0.025
foley += hum * (T < 6.3)
for k in range(13):
    tt = k * 0.5
    if tt < 6.3:
        n = int(0.03 * SR); add(foley, tt, hp(rng.standard_normal(n), 3000) * env(n, 0.001, 0.008) * 0.12)


def farfalhar(dur):
    n = int(dur * SR); k = np.arange(n) / SR
    return lp(hp(rng.standard_normal(n), 800), 5000) * np.sin(np.pi * k / dur) * 0.12


add(foley, 0.85, farfalhar(0.5)); add(foley, 1.35, farfalhar(0.35))
add(foley, 23.1, farfalhar(0.6))
# rangido de borracha do botão (3,2–4,2)
n = int(0.9 * SR); k = np.arange(n) / SR
rang = np.sin(2 * np.pi * np.cumsum(420 + 140 * np.sin(2 * np.pi * 7 * k)) / SR) * (0.5 + 0.5 * np.sin(2 * np.pi * 13 * k)) * np.sin(np.pi * k / 0.9)
add(foley, 3.2, lp(rang, 1800) * 0.08)
# "tunc" por andar apagando (10,4 + 0,16·k)
for j in range(8):
    n = int(0.35 * SR); k = np.arange(n) / SR
    s = np.sin(2 * np.pi * np.cumsum(55 + 50 * np.exp(-k * 25)) / SR) * np.exp(-k * 10)
    add(foley, 10.4 + j * 0.16, s * (0.55 + 0.04 * j))
# cidade desligando: zumbido grave descendente (13,4 → 16,4)
n = int(3.0 * SR); k = np.arange(n) / SR
f = 110 * np.exp(-k * 0.6)
vu = lp(np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR)) * 0.5 + np.sin(2 * np.pi * np.cumsum(f * 0.5) / SR), 700) * np.minimum(1, k / 0.3) * np.exp(-k * 0.5)
add(foley, 13.4, vu * 0.22)
# ronquinho agudo ×2 (24,8 e 25,4)
for tt in (24.8, 25.4):
    n = int(0.5 * SR); k = np.arange(n) / SR
    s = lp(rng.standard_normal(n), 1800) * 0.5 + np.sin(2 * np.pi * np.cumsum(900 + 400 * k) / SR) * 0.25
    add(foley, tt, s * np.sin(np.pi * k / 0.5) ** 2 * 0.22)


# vozes do Kokoro aceleradas (×1,8 = voz de inseto)
def voz(nome, at, g=1.0, corte=None):
    src = f"build/voz/{nome}.wav"
    if not os.path.exists(src):
        return
    out = f"build/voz/{nome}-inseto.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-af", "silenceremove=start_periods=1:start_threshold=-40dB,asetrate=24000*1.8,aresample=44100,highpass=f=300", "-ac", "1", out], check=True)
    x, sr = sf.read(out)
    if corte:
        x = x[: int(corte * sr)]
    x = x * np.minimum(1, np.linspace(0, len(x) / sr, len(x)) / 0.01)
    add(foley, at, x / (np.abs(x).max() + 1e-9) * 0.5 * g)


voz("hmpf", 1.75, 0.9, 0.45)
voz("esforco", 3.05, 0.9, 1.0)
voz("hup", 5.3, 0.9, 0.3)


def salvar(x, nome):
    x = np.tanh(x * 1.2) / np.tanh(1.2)
    x *= 0.89 / (np.abs(x).max() + 1e-9)
    os.makedirs("build", exist_ok=True)
    sf.write(f"build/{nome}.wav", np.stack([x, x], 1).astype(np.float32), SR)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"build/{nome}.wav", "-c:a", "libmp3lame", "-b:a", "192k", f"assets/audio/{nome}.mp3"], check=True)


salvar(musica, "musica")
salvar(foley, "foley")
print("ok")
