"""Trilha do institucional da Vetrex: pulso eletrônico limpo (sub, hat, pad) que cresce até o fecho.

Uso (na pasta do projeto): /tmp/claude-0/kvenv/bin/python tools/gerar_trilha.py
"""
import json
import subprocess

import numpy as np
import soundfile as sf

SR = 44100
T = json.load(open("build/timing.json"))
F = T["frases"]
DUR = round(T["total"] + 2.6, 2)
N = int(DUR * SR)
t = np.arange(N) / SR
rng = np.random.default_rng(11)

T_MARCA = F[1]["ini"]          # entra o pulso
T_PULSO = F[4]["ini"]          # "Escolheu. Pagou. Disparou." — entra o hat
T_FECHO = F[9]["ini"]          # acorde final

BPM = 120.0
BEAT = 60.0 / BPM


def lowpass(x, fc):
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    return np.fft.irfft(X / np.sqrt(1 + (f / fc) ** 4), len(x))


def env(ini, dur, ataque, queda):
    """Envelope simples a partir de um instante."""
    e = np.zeros(N)
    i0 = int(ini * SR)
    n = min(int(dur * SR), N - i0)
    if n <= 0:
        return e
    x = np.arange(n) / SR
    e[i0:i0 + n] = np.minimum(x / max(ataque, 1e-3), 1.0) * np.exp(-np.maximum(x - ataque, 0) / queda)
    return e


def rampa(ini, subida):
    return np.clip((t - ini) / subida, 0, 1)


# --------------------------------------------------------------- pad (lá menor → fá)
def nota(freq, detune=0.0):
    ph = 2 * np.pi * (freq + detune) * t
    return 0.6 * np.sin(ph) + 0.25 * np.sin(2 * ph) + 0.12 * np.sin(3 * ph)


acorde_a = sum(nota(f, d) for f, d in ((110.0, 0.0), (164.81, 0.15), (261.63, -0.2), (329.63, 0.25)))
acorde_b = sum(nota(f, d) for f, d in ((87.31, 0.0), (130.81, 0.15), (261.63, -0.2), (349.23, 0.25)))
troca = (np.sin(2 * np.pi * t / 8.0) > 0).astype(float)
troca = lowpass(troca, 2.0)
pad = lowpass(acorde_a * (1 - troca) + acorde_b * troca, 900) * 0.05
pad *= 0.45 + 0.55 * rampa(T_MARCA, 2.0)
pad *= 1.0 - 0.35 * np.clip((t - (DUR - 2.4)) / 2.4, 0, 1)

# --------------------------------------------------------------- sub + hat
sub = np.zeros(N)
hat = np.zeros(N)
clave = np.zeros(N)
k = 0
while k * BEAT < DUR:
    inicio = k * BEAT
    if inicio >= T_MARCA - 0.2:
        f0 = 55.0 if k % 4 else 41.2
        e = env(inicio, 0.5, 0.004, 0.11)
        sub += np.sin(2 * np.pi * f0 * t + 1.2 * np.cumsum(e) / SR) * e * 0.5
    if inicio >= T_PULSO - 0.2 and k % 2 == 1:
        e = env(inicio, 0.18, 0.001, 0.028)
        hat += rng.normal(0, 1, N) * e * 0.06
    if inicio >= T_PULSO - 0.2 and k % 8 == 4:
        e = env(inicio, 0.6, 0.002, 0.14)
        clave += np.sin(2 * np.pi * 1760 * t) * e * 0.03
    k += 1
hat = hat - lowpass(hat, 5200)

# --------------------------------------------------------------- riser e impacto do fecho
riser = np.zeros(N)
i0, i1 = int((T_PULSO - 1.6) * SR), int(T_PULSO * SR)
if i1 > i0:
    x = np.linspace(0, 1, i1 - i0)
    riser[i0:i1] = rng.normal(0, 1, i1 - i0) * (x ** 3) * 0.05
    riser[i0:i1] = riser[i0:i1] * np.sin(2 * np.pi * np.cumsum(400 + 3000 * x) / SR)

impacto = np.sin(2 * np.pi * 48 * t) * env(T_FECHO, 3.0, 0.005, 0.9) * 0.35
impacto += lowpass(rng.normal(0, 1, N), 2500) * env(T_FECHO, 2.2, 0.004, 0.5) * 0.05

mix = pad + sub * 0.9 + hat + clave + riser + impacto
mix *= 1 - np.clip((t - (DUR - 1.2)) / 1.2, 0, 1)        # fade final
mix /= max(1.0, np.abs(mix).max() / 0.85)
sf.write("build/trilha.wav", np.column_stack([mix, mix]).astype(np.float32), SR)
subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", "build/trilha.wav",
                "-af", "loudnorm=I=-26:TP=-6:LRA=9,aresample=44100", "-c:a", "libmp3lame", "-b:a", "192k",
                "assets/audio/trilha.mp3"], check=True)
print("trilha ok", round(DUR, 2), "s")
