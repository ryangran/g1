#!/usr/bin/env bash
# Gera os clipes provisórios do animatic (assets/clips/cena-N.mp4): cartão com número,
# título e ação de cada cena, na duração exata. Troque pelos clipes gerados mantendo o nome.
set -euo pipefail
cd "$(dirname "$0")/.."
B=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf
R=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf
mkdir -p assets/clips build
# n | duração | cor de fundo | título | ação (linhas separadas por \n)
while IFS='|' read -r n d cor titulo acao; do
  printf '%b' "$acao" > build/acao-$n.txt
  ffmpeg -nostdin -v error -y -f lavfi -i "color=c=$cor:s=1080x1920:r=30:d=$d" -vf "\
drawtext=fontfile=$B:text='CENA $n':fontcolor=0xffffff80:fontsize=54:x=(w-tw)/2:y=330,\
drawtext=fontfile=$B:text='$titulo':fontcolor=white:fontsize=96:x=(w-tw)/2:y=420,\
drawtext=fontfile=$R:textfile=build/acao-$n.txt:fontcolor=0xffffffd0:fontsize=46:line_spacing=18:x=(w-tw)/2:y=640,\
drawtext=fontfile=$R:text='%{eif\:t+0\:d}.%{eif\:mod(t*10\,10)\:d} s':fontcolor=0xffffff70:fontsize=40:x=(w-tw)/2:y=1240" \
    -c:v libx264 -pix_fmt yuv420p -preset veryfast -crf 26 "assets/clips/cena-$n.mp4"
done <<'CENAS'
1|2.2|0x15203a|O ABAJUR|Lumi deitado na caixa de fósforos\nencara o abajur gigante, irritado\n(brilho fraco sob a meia)
2|2.4|0x2a2016|O BOTÃO|empurra o botão com o corpo todo\nos pés escorregam\nnada acontece
3|2.8|0x1a1410|O CHUTE|chute — o abajur tomba e apaga\nele comemora\nfaísca azul corre pelo fio
4|2.8|0x0d1626|A RÉGUA|pop pop pop POP\nTV, aquário, geladeira apagam\ndisjuntor desarma
5|3.0|0x101a33|O PRÉDIO|os andares apagam em onda\no letreiro morre
6|3.4|0x070b1c|A CIDADE|anel de escuridão se espalha\naté o horizonte
7|2.4|0x05060c|O CÉU|estrelas apagam uma a uma\na lua: CLIQUE\npreto absoluto
8|3.4|0x000000|A ÚLTIMA LUZ|um pontinho no escuro...\né o bumbum do Lumi\nele percebe
9|3.6|0x000000|BOA NOITE|sorriso amarelo, cobre a luz\npreto\nronco: a luz vaza 2x
CENAS
ls -la assets/clips
