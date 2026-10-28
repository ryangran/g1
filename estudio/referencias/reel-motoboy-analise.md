# Análise do reel de referência ("Você é motoboy…")

Arquivo analisado: vídeo enviado pelo usuário (WhatsApp, 28/10/2026). 576×1024, 30 fps, **1 min 45 s**, áudio −14,5 LUFS. Quadros revisados a cada 1,5 s.

## O formato em uma frase
Narração em 2ª pessoa ("Você é motoboy. São três da manhã…") que coloca o espectador num **dilema**, e então explica com **dados reais** por que cada saída é difícil (peso, câmeras, banco, lei). No fim, pede que a pessoa **escolha nos comentários** e promete a **Parte 2 amanhã**.

## Estrutura (beats e tempos)
| Tempo | Beat | O que aparece |
|---|---|---|
| 0–8 s | Gancho: a situação | "Você é motoboy. São três da manhã. E você acabou de achar milhões de reais na estrada." Ilustração: motoboy, carro capotado fumegando, malas de dinheiro abertas |
| 8–15 s | Complicação | "Um carro preto… o motorista sumiu no mato… as malas ficaram. Agora vem a parte difícil." Close do rosto suado |
| 16–17 s | Título/tema | Cartão preto: **CADA CENTAVO DEIXA RASTRO** (kicker "PARTE 1 · OITENTA QUILOS") |
| 18–38 s | Problema 1: o peso | Infográfico: 1 nota de R$100 ≈ 1 g → grade de cédulas (80.000 cédulas = **80 KG**; com notas de 50 = **100+ KG**) → baú da moto aguenta 20 kg → **4 VIAGENS** |
| 39–56 s | Problema 2: câmeras | Pórtico com câmeras → close de câmera lendo a placa → cartão "RND-4E21 · ~6 mil pontos de leitura de placa · **ALERTA EM 2 s**" → "1× ENTREGA, 4× **PADRÃO**" (carimbo) |
| 57–67 s | Problema 3: dinheiro vivo | Motoboy em casa com a mala; no banco com segurança → cartão "Movimentar R$ 50 mil ou mais em espécie → comunicação automática → **COAF NOTIFICADO**" (carimbo) |
| 67–73 s | Virada legal | Close do rosto → "Ficar com dinheiro achado **É CRIME** · Art. 169 Código Penal · prazo de 15 dias para devolver" |
| 73–77 s | Regra | "Regra número um: **Nunca leve tudo de uma vez.**" |
| 78–98 s | Pressão + escolha | Farol de carro chegando lá atrás. "Opção A: **VIAGEM**" (4 viagens até o sol nascer) / "Opção B: **ENTERRA**" (enterra 3 malas, leva só uma). "Comente VIAGEM / Comente ENTERRA" |
| 98–102 s | Gancho extra | Círculo amarelo destaca um reboque escondido: "tem um terceiro jeito escondido nessa imagem" |
| 102–105 s | Fecho | "Comente uma palavra: VIAGEM / ENTERRA · ou ache o 3º jeito escondido · **PARTE 2 AMANHÃ**" |

**Ritmo:** troca de imagem a cada 1,5–4 s (cerca de 35 planos). Nunca fica mais de 4 s sem algo novo.

## Camadas visuais
1. **Ilustrações estilo HQ/graphic novel:** contorno preto grosso, cel shading, cores saturadas, luz dramática (farol, lanterna, poste). O **mesmo personagem** em todas: motoboy negro, jaqueta amarela refletiva, capacete preto, moto vermelha com baú vermelho, placa RND-4E21. Cerca de 15 ilustrações diferentes, cada uma reaproveitada em 2–3 planos com zoom/pan diferente (Ken Burns) e leve movimento (fumaça, luz).
2. **HUD fixo no topo**, como em jogo: `NA MALA R$ 8.000.000 · NO BANCO R$ 0 · SUSPEITA 0%`. A suspeita sobe ao longo da história (0% → 6% → 11%), e um relógio "03:20" aparece na parte final. Isso cria a sensação de "partida" e de risco crescente.
3. **Legendas palavra por palavra** no meio-baixo da tela: brancas, negrito e com sombra, mostrando 2–4 palavras por vez, com a palavra-chave em **amarelo**.
4. **Cartões de infográfico** em dois fundos: creme `#efe9df` (dados) e quase preto `#1c1a17` (alertas e títulos). Têm kicker em caixa alta pequena ("PROBLEMA 1 · O PESO"), números enormes, ícones simples, **carimbos vermelhos inclinados** ("ALERTA EM 2 s", "PADRÃO", "COAF NOTIFICADO", "ART. 169") e notas de fonte em letra miúda.
5. **Fecho interativo:** botões "VIAGEM" (branco) e "ENTERRA" (amarelo), mais o "PARTE 2 AMANHÃ".

## Áudio
Narração masculina brasileira, energética e próxima ("você"), sem pausas mortas. Trilha de tensão baixa por baixo. SFX nos carimbos e nas trocas de cartão.

## Por que funciona (hipóteses)
- **Segunda pessoa + dilema:** o espectador se imagina na situação e quer decidir.
- **Dados reais e surpreendentes** (80 kg, 6 mil câmeras, COAF, Art. 169): dão vontade de salvar e compartilhar.
- **HUD de jogo:** transforma a história numa partida, com a pergunta "e a suspeita vai subir?".
- **Comentário com uma palavra:** pedido de engajamento com custo baixíssimo, além de dividir o público entre as opções.
- **"3º jeito escondido na imagem":** faz a pessoa reassistir e olhar a imagem com atenção.
- **"Parte 2 amanhã":** cria uma série e faz a pessoa seguir o perfil.

## O que muda no nosso fluxo
| Etapa | Como fazer |
|---|---|
| Roteiro (dilema + dados verificados + escolha) | Eu, com pesquisa e checagem das fontes |
| Ilustrações HQ consistentes (~15 por episódio) | **Gerador de imagem** (Gemini/Imagen no mesmo plano do Veo 3, ou Midjourney) com folha de personagem como referência. Eu escrevo todos os prompts |
| Movimento nas ilustrações | **Veo 3** (imagem → vídeo de 8 s, ex.: fumaça, farol, moto andando) **ou** Ken Burns que eu faço no HyperFrames |
| Narração pt-BR expressiva | Gravar a própria voz (melhor), **Google AI Studio (Gemini TTS)**, ElevenLabs, ou o Veo 3 (menos controle). A Kokoro daqui é robótica para esse formato |
| HUD, legendas palavra por palavra, cartões, carimbos, fecho | **Eu, no HyperFrames** (é exatamente o forte dele) |
| Trilha e SFX | SFX embutidos + trilha de tensão de banco (Pixabay / biblioteca do Instagram) |
