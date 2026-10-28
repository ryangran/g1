# Bíblia visual — 01-proibido-dancar

## Personagens (definitivos — não mudam entre cenas)

### Bolt — protagonista
- **Função:** operário que não consegue conter a vontade de dançar.
- **Idade aparente:** jovem (energia, movimentos soltos).
- **Silhueta:** RobotExpressive em escala 1,0 (altura = 1 unidade). Cabeça larga em cúpula, olhos esféricos pretos, sobrancelhas em barra, braços longos com pinças.
- **Cores (materiais):** Main `#ff7a1a` (laranja: única cor quente entre os operários), Grey `#5a5e66`, Black `#0f0f12`. Rugosidade 0,55, metal 0,2.
- **Personalidade/movimento:** inquieto. Balança a cabeça na batida (Head ±0,12 rad), congela num estalo quando é observado.
- **Expressões:** Surprised (flagrado), Sad (encolhe 10% na vertical, cabeça baixa +0,35 rad), alívio (volta a 1,0 com overshoot).
- **Desejo:** dançar. **Medo:** o chefe. **Conflito:** regra × impulso.
- **Lugar fixo:** fileira da frente, 2º da direita (x 0,55, z 0).

### Chefe — antagonista que vira mentor
- **Silhueta:** mesmo modelo em escala 1,45, para dominar o quadro.
- **Cores:** Main `#8e1b1b` (vermelho escuro), Grey `#26282d`, Black `#0a0a0c`.
- **Movimento:** passos pesados (Walking a 0,62–0,9), varredura de cabeça (Head y ±0,45), inclina o tronco ao intimidar (Torso x 0,28).
- **Expressões:** Angry 0,55 constante; Surprised ao flagrar; Angry 1,0 na aproximação; neutro ao revelar.
- **Segredo:** ama dançar, só odeia gente que dança errado.

### Operários (11)
- Mesmo modelo, escala 1,0, Main `#5c6878` (azul-acinzentado), Grey `#3b4048`.
- Idle quase parado (velocidade 0,18, fase aleatória com seed) para parecerem rígidos. Três vizinhos viram a cabeça para o Bolt aos 12,7–13,4 s.

## Cenário: galpão da fábrica
- Piso de concreto `#2a2d33` com juntas a cada 1/8 da textura; faixa de segurança amarela/preta em z 0,62.
- Parede do fundo em z −4,6 com painéis verticais `#353a42`; colunas em x ±3,6; canos em y 4,85 / 5,1 / 0,55.
- **Placa** (3,2 × 2,0) em y 2,62: fundo `#c21f1f`, borda branca, "PROIBIDO" `#ffd23f`, "DANÇAR" branco, "MAL" `#ffe14a`, este coberto por uma **tábua** `#6b5a43` com 2 parafusos.
- **Neon** "PROIBIDO PARAR" em y 4,22: invisível até 36,2 s, pisca 2× e acende rosa `#ff2a8a`.
- **Giroflex** vermelho à direita da placa (x 1,95, y 3,75): liga no flagra (19,4 s), desliga na revelação.

## Paleta
Fundo `#0c0f15` · concreto `#2a2d33` · laranja do Bolt `#ff7a1a` · vermelho do chefe `#8e1b1b` · placa `#c21f1f` · amarelo de destaque `#ffd23f` / `#ffe14a` · festa `#ff3d8b` `#3dd6ff` `#ffd23f`.

## Iluminação
- **Chave:** spot quente `#ffe2b8` de cima à direita (1,6; 5,2; 3,2) com sombra suave. Cai para 34 durante a tensão.
- **Contra:** direcional azul `#6fa0ff` do fundo à esquerda (recorte das silhuetas).
- **Ambiente:** hemisférica azul/marrom 0,75.
- **Preenchimento:** ponto quente preso à câmera (2,2) para os rostos nunca afundarem no preto.
- **Práticas:** spot da placa, giroflex, neon, 3 spots de festa que trocam de cor a cada 2 batidas, foco solitário quente no Bolt no final.
- Neblina de 7 a 17 unidades para profundidade.

## Direção de arte
Cartoon 3D low-poly de longa animada; materiais foscos; contraste alto para tela de celular; uma única cor quente (Bolt) num mar de cinza-azulado.

## Câmera
FOV 30–56° (vertical 9:16). Gancho e emoções: close/médio na altura do Bolt (0,6–0,95). Ameaça: contra-plongée baixa (0,28) com tremor de 0,004. Revelações: plano geral frontal. Movimentos sempre motivados: push-in (tensão), arco (euforia), recuo (revelação).

## Regras de continuidade
1. Bolt sempre na posição (0,55; 0; 0), olhando para +z.
2. O chefe só cruza a frente das fileiras (z 1,35) e para a 0,95 do Bolt.
3. A tábua está presente em todo quadro até 29,4 s.
4. O neon nunca aparece legível antes de 36,2 s.
5. Toda dança começa num múltiplo da batida (0,4167 s), menos a do Bolt no final, que está fora do ritmo de propósito.

## Referências reutilizáveis
`assets/modelos/RobotExpressive.glb` · cores acima · `cena.js` (PLANOS, ATUAÇÃO) · seeds 7 (piso) e 100+i (operários) · `audio/gerar_trilha.py` (BPM 144, padrão de 16 passos).
