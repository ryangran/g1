"""Trilha de "O Bilhete" (Parte 2): tensão urbana de madrugada (drone grave, pulso de coração,
tique de relógio, pad noturno, chuva fina). Segue os tempos de build/timing.json.

Uso (na pasta do episódio): /tmp/claude-0/kvenv/bin/python tools/gerar_trilha.py
"""
import json
import os
import subprocess

import numpy as np
import soundfile as sf

SR = 44100
T = json.load(open("build/timing.json"))
F = {f["texto"]: f for f in T["frases"]}
ini = lambda prefixo: next(f["ini"] for t, f in F.items() if t.startswith(prefixo))
DUR = round(T["total"] + 4.2, 2)
N = int(DUR * SR)
t = np.arange(N) / SR
rng = np.random.default_rng(7)


def lowpass(x, fc):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR)
    return np.fft.irfft(X / np.sqrt(1 + (f / fc) ** 4), len(x))


def bandpass(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR)
    return np.fft.irfft(X * ((f > lo) & (f < hi)), len(x))


def env(chaves):
    return np.interp(t, [k[0] for k in chaves], [k[1] for k in chaves])


def add(buf, at, sig, g=1.0):
    i = int(at * SR)
    if i < len(buf):
        j = min(len(buf), i + len(sig)); buf[i:j] += sig[: j - i] * g


P1, P2, P3 = ini("Problema um"), ini("Problema dois"), ini("E a central contou")
VIRA, OUVIU, REGRA = ini("Ou seja"), ini("O carro preto encostou"), ini("Regra número dois")
VOLTA = ini("Mas volta")  # o gancho é o fim da cena; "volta dez minutos" rebobina
ESC, FECHO = ini("O que a gente faz"), ini("A maioria escreve")

# drone grave (lá menor) com batimento lento
drone = lowpass(sum(2 * ((t * f) % 1) - 1 for f in (55.0, 55.35, 82.4, 110.2)), 220) * 0.22
# pad noturno: acorde menor suave com vibrato
pad = sum(np.sin(2 * np.pi * f * t + 0.6 * np.sin(2 * np.pi * 0.2 * t + k)) for k, f in enumerate((220.0, 261.6, 329.6, 392.0))) * 0.035
# chuva fina
chuva = bandpass(rng.standard_normal(N), 2500, 9000) * 0.018

# coração: 66 bpm até o problema 1, acelera até 96 na virada
bat = np.zeros(N)
def batida():
    k = np.arange(int(0.25 * SR)) / SR
    return np.sin(2 * np.pi * np.cumsum(48 + 40 * np.exp(-k * 30)) / SR) * np.exp(-k * 14)
x = 0.4
while x < FECHO:
    bpm = 104 if x < VOLTA else 66 if x < P1 else np.interp(x, [P1, VIRA, ESC], [72, 88, 96])
    add(bat, x, batida(), 0.9); add(bat, x + 0.22, batida(), 0.55)
    x += 60 / bpm

# tique de relógio (só nos problemas: o tempo correndo)
tique = np.zeros(N)
k = np.arange(int(0.03 * SR)) / SR
tq = bandpass(rng.standard_normal(len(k)), 3000, 8000) * np.exp(-k * 160)
for x in np.arange(P1, REGRA, 0.5):
    add(tique, x, tq, 0.5 if int(x * 2) % 2 else 0.3)

g_drone = env([(0, 1.0), (VOLTA - 0.05, 1.0), (VOLTA, 0.4), (P1, 0.7), (VIRA, 1.0), (REGRA, 0.8), (FECHO, 0.5), (DUR, 0.0)])
g_pad = env([(0, 0.8), (P1, 0.5), (VIRA, 0.0), (REGRA - 0.1, 0.0), (REGRA, 0.6), (DUR - 1, 0.6), (DUR, 0)])
g_bat = env([(0, 1.0), (VOLTA - 0.05, 1.0), (VOLTA, 0.3), (P1, 0.55), (VIRA, 0.8), (OUVIU, 1.0), (REGRA - 0.05, 1.0), (REGRA, 0.3), (ESC, 0.6), (FECHO, 0.0), (DUR, 0)])
mix = drone * g_drone + pad * g_pad + bat * g_bat + tique + chuva * env([(0, 1), (DUR - 1.5, 1), (DUR, 0)])
# silêncio dramático meio segundo antes da virada ("não era nenhum Antônio")
mix *= env([(0, 1), (VIRA + 1.2, 1), (VIRA + 1.35, 0.15), (VIRA + 2.3, 0.15), (VIRA + 2.5, 1), (DUR, 1)])

st = np.stack([mix, np.roll(mix, 13)], 1)
st = np.tanh(st * 1.4) / np.tanh(1.4)
st *= 0.8 / np.abs(st).max()
sf.write("build/trilha.wav", st.astype(np.float32), SR)
subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", "build/trilha.wav", "-c:a", "libmp3lame", "-b:a", "192k", "assets/audio/trilha.mp3"], check=True)
os.remove("build/trilha.wav")
print("ok", DUR)
