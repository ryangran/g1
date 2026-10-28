# 04 — Bilhete no táxi (ficção, formato "Você é…")

Formato copiado do reel de referência (`estudio/referencias/reel-motoboy-analise.md`): narração em 2ª pessoa, ilustrações estilo HQ com o mesmo personagem, **painel de jogo no topo**, legendas palavra por palavra, cartões de "problema" e **escolha nos comentários + Parte 2**.
**Tudo fictício:** nada de leis ou regras reais. Os "problemas" são da própria história.

- Vertical 1080×1920 · ~70 s · narração pt-BR (Gemini TTS) · ~12 ilustrações + 3–4 clipes Veo 3 opcionais.
- **Painel (topo):** `NO BANCO DE TRÁS R$ 40.000.000` · `NO BOLSO R$ 0` · `RISCO 0%` (o risco sobe: 0 → 15 → 35 → 60%).

## Narração (texto para o Gemini TTS)

Instrução de estilo para o TTS: *"Narrador brasileiro, masculino, voz próxima e tensa, como quem conta um segredo para um amigo; ritmo rápido, sem pausas longas; ênfase nas palavras em MAIÚSCULAS."*

| # | Texto narrado | Imagem / cartão | Painel |
|---|---|---|---|
| 1 | Você é taxista. É uma da manhã. E o passageiro que acabou de descer esqueceu uma coisa no banco de trás. | IMG01 → IMG02 | 0% |
| 2 | Um bilhete. Você confere os números no celular… e bate. Os SEIS. | IMG02 (close) | 0% |
| 3 | QUARENTA MILHÕES de reais. No seu banco de trás. | IMG03 | 0% |
| 4 | Agora vem a parte difícil. Porque todo prêmio… tem dono. | CARTÃO A: **TODO PRÊMIO TEM DONO** | 0% |
| 5 | Problema um: o passageiro. Em dois minutos ele percebe o que esqueceu. E volta correndo. | IMG04 · CARTÃO B (cronômetro 2:00 → 0:47) | 15% |
| 6 | Ele lembra de tudo: táxi branco, placa final sete, a música que tava tocando. | CARTÃO B2 (ficha "TÁXI BRANCO · FINAL 7 · RÁDIO 98,1") | 15% |
| 7 | Problema dois: a central. Toda corrida fica gravada. Hora, endereço… e o seu nome. | IMG05 · CARTÃO C (tela "CORRIDA #4471 · 00:58" + carimbo **REGISTRADA**) | 35% |
| 8 | Problema três: você vira o bilhete. Tem um nome escrito à caneta. "Seu Antônio". E um telefone. | IMG06 · CARTÃO D (carimbo **TEM NOME**) | 35% |
| 9 | E aí você olha no retrovisor. Ele tá lá na esquina. Com as mãos na cabeça. | IMG07 | 60% |
| 10 | Opção A: você acelera e some na madrugada. Comente GUARDA. | IMG08 + selo **GUARDA** | 60% |
| 11 | Opção B: você desce, atravessa a rua e devolve. Comente DEVOLVE. | IMG09 + selo **DEVOLVE** | 60% |
| 12 | Mas tem um terceiro jeito escondido nessa imagem. Quase ninguém vê. | IMG01 + círculo amarelo no crachá caído no tapete | 60% |
| 13 | Comente uma palavra. A parte dois sai amanhã. | CARTÃO FINAL: **GUARDA / DEVOLVE · ou ache o 3º jeito · PARTE 2 AMANHÃ** | — |

## Personagem fixo (folha de referência — gerar primeiro)

**Prompt FOLHA (Gemini/Imagen):**
`Character reference sheet, graphic novel comic illustration style with thick black ink outlines, cel shading, saturated colors. A Brazilian taxi driver, about 45 years old, tan skin, short black hair with grey temples, thick grey-black mustache, tired kind eyes, light-blue short-sleeve button shirt with a pen in the pocket, dark trousers, simple wristwatch. Front view, 3/4 view, side view, and four facial expressions: shocked, sweating nervous, tempted half-smile, worried. White background, consistent proportions, no text.`

**Estilo base (colar no fim de TODOS os prompts de cena):**
`— vertical 9:16, graphic novel comic illustration, thick black ink outlines, cel shading, saturated colors, dramatic cinematic night lighting, São Paulo-like Brazilian city at night, same taxi driver as the reference image (light-blue shirt, grey-black mustache), white Brazilian taxi with a red roof sign "TÁXI", no text except where specified.`

## Prompts das ilustrações

| ID | Prompt (somar o estilo base) |
|---|---|
| IMG01 | `Wide shot from the back seat of a white taxi at 1 a.m., the driver turning around looking at the back seat, a lottery ticket lying on the seat lit by a streetlight, rain drops on the window, an ID badge fallen on the floor mat (small detail, lower right).` |
| IMG02 | `Extreme close-up of the driver's hand holding a lottery ticket with six numbers circled in red pen, next to a phone screen glowing with the same six numbers, warm phone light on his fingers.` |
| IMG03 | `Close-up of the taxi driver's face, eyes wide in shock, sweat drops on his forehead, lit by the green glow of the dashboard and the red light of the city.` |
| IMG04 | `Seen through the taxi's side mirror: a man in a wrinkled suit on the sidewalk patting his pockets, starting to turn around, city lights bokeh behind him.` |
| IMG05 | `The taxi's dashboard radio and a phone app screen showing a trip receipt, a small red recording light, the driver's hand frozen near it.` |
| IMG06 | `Close-up of the back of the lottery ticket with handwritten blue pen text "Seu Antônio" and a phone number "(11) 9 8472-...", the driver's thumb holding it, shallow depth of field.` |
| IMG07 | `Seen in the taxi rear-view mirror: at the street corner an older man in a suit with both hands on his head, desperate, looking left and right, wet street reflecting lights.` |
| IMG08 | `The taxi speeding away down an empty avenue at night, motion lines, headlights streaking, the driver's tense face visible through the windshield.` |
| IMG09 | `The taxi driver getting out of the car and crossing the wet street toward the older man, holding the lottery ticket up, the man turning with hope in his eyes.` |

## Clipes Veo 3 (opcionais — dão movimento às ilustrações principais)
Use a ilustração aprovada como **imagem inicial**, 8 s, 9:16, **sem fala** (a narração entra na montagem):
- **V1 (IMG01):** `Slow push-in from the back seat toward the lottery ticket, rain drops slide on the window, streetlight flickers, ambient city rain sound, no dialogue.`
- **V2 (IMG03):** `The driver's eyes widen slowly, a sweat drop rolls down, dashboard light pulses, subtle handheld camera, heartbeat sound, no dialogue.`
- **V3 (IMG07):** `In the mirror the man spins around looking for the taxi, hands on head, car passes in the foreground, ambient street sound, no dialogue.`
- **V4 (IMG08):** `The taxi accelerates away, camera tracking alongside, city lights streak past, engine roar, no dialogue.`

## Montagem (HyperFrames — eu monto)
- Cada ilustração aparece 1,5–4 s com zoom/pan diferente (Ken Burns). Os clipes Veo substituem a imagem parada onde existirem.
- **Painel** fixo no topo (168–330 px, fora da barra do app) com contagem animada nos valores.
- **Legendas** palavra por palavra (2–4 palavras, palavra-chave em amarelo) por volta de 1150–1300 px.
- **Cartões** creme `#efe9df` e quase preto `#1c1a17`, kicker "PROBLEMA 1 · O PASSAGEIRO", números grandes e **carimbos vermelhos** com impacto sonoro.
- **Fecho:** botões GUARDA (branco) / DEVOLVE (amarelo) + "PARTE 2 AMANHÃ".
- Trilha de tensão baixa + SFX embutidos (whoosh na troca, impacto no carimbo, tique no cronômetro).

## Com a GEMINI_API_KEY no ambiente, a próxima sessão faz:
1. Gera a folha do personagem e as 9 ilustrações (modelo de imagem do Gemini/Imagen, com a folha como referência).
2. Gera a narração (Gemini TTS, pt-BR) e calcula os tempos de cada palavra para as legendas.
3. (Opcional) Gera os 4 clipes Veo 3 a partir das ilustrações.
4. Monta, revisa os quadros e renderiza.
