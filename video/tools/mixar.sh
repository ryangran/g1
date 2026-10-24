#!/usr/bin/env bash
# Junta as cenas narradas, masteriza a voz e abaixa a trilha sob a fala (ducking).
set -euo pipefail
D="${1:-build/audio}"
for i in 0 1 2 3 4 5; do echo "file '$PWD/$D/scene$i.wav'"; done > "$D/full.txt"
ffmpeg -v error -y -f concat -safe 0 -i "$D/full.txt" "$D/full.wav"
ffmpeg -v error -y -i "$D/full.wav" -af "adelay=400,apad=pad_dur=1.5,highpass=f=70,acompressor=threshold=-20dB:ratio=3:attack=5:release=120,loudnorm=I=-16:TP=-1.5:LRA=7,aresample=44100" -ac 2 "$D/narration.wav"
ffmpeg -v error -y -i "$D/music.wav" -i "$D/narration.wav" -filter_complex "[0:a]volume=-3dB[m];[m][1:a]sidechaincompress=threshold=0.05:ratio=3:attack=30:release=600[d]" -map "[d]" -ar 44100 "$D/music_ducked.wav"
mkdir -p assets/audio
ffmpeg -v error -y -i "$D/narration.wav" -c:a libmp3lame -b:a 192k assets/audio/narracao.mp3
ffmpeg -v error -y -i "$D/music_ducked.wav" -c:a libmp3lame -b:a 192k assets/audio/trilha.mp3
