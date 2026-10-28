# Passo a passo — gerar no plano Google AI Pro (sem API paga)

Você gera no **app Gemini** (imagens), no **Google AI Studio** (narração) e, se quiser, no **Flow** (Veo 3, usa os créditos). Depois me manda os arquivos no chat e eu monto tudo.

## 1. Personagem (app Gemini — https://gemini.google.com)
Num chat novo, cole:

> Gere uma imagem 16:9: Character reference sheet for a comic, graphic novel comic illustration style with thick black ink outlines, cel shading, saturated colors. A Brazilian taxi driver, about 45 years old, tan skin, short black hair with grey temples, thick grey-black mustache, tired kind eyes, light-blue short-sleeve button shirt with a pen in the pocket, dark trousers, simple wristwatch. Show: full body front view, 3/4 view, side view, and a row of four head close-ups with expressions: shocked, sweating nervous, tempted half-smile, worried. Plain light background, consistent proportions, no text.

Baixe a imagem como **folha.png**.

## 2. As 9 cenas (no MESMO chat, para ele manter o personagem)
Para cada cena, cole a frase abaixo, trocando o texto da cena:

> Usando exatamente o mesmo taxista da folha acima, gere uma imagem VERTICAL 9:16, graphic novel comic illustration, thick black ink outlines, cel shading, saturated colors, dramatic cinematic night lighting, Brazilian city at night, white taxi with a red roof sign "TÁXI", no other text. Cena: **[TEXTO DA CENA]**

| Arquivo | Texto da cena |
|---|---|
| **img01.png** | Wide shot from the back seat of the taxi at 1 a.m., the driver turning around looking at the back seat, a lottery ticket lying on the seat lit by a streetlight, rain drops on the window, an ID badge fallen on the floor mat (small detail, lower right) |
| **img02.png** | Extreme close-up of the driver's hand holding a lottery ticket with six numbers circled in red pen, next to a phone screen glowing with the same six numbers |
| **img03.png** | Close-up of the driver's face, eyes wide in shock, sweat drops on his forehead, lit by the green dashboard glow and red city lights |
| **img04.png** | Seen through the taxi's side mirror: a man in a wrinkled suit on the sidewalk patting his pockets, starting to turn around |
| **img05.png** | The taxi dashboard radio and a phone app screen showing a trip receipt, a small red recording light, the driver's hand frozen near it |
| **img06.png** | Close-up of the back of the lottery ticket with handwritten blue pen "Seu Antônio" and a phone number, the driver's thumb holding it |
| **img07.png** | Seen in the rear-view mirror: at the street corner an older man in a suit with both hands on his head, desperate, wet street reflecting lights |
| **img08.png** | The taxi speeding away down an empty avenue at night, motion lines, headlights streaking, the driver's tense face through the windshield |
| **img09.png** | The driver getting out of the car and crossing the wet street toward the older man, holding the lottery ticket up, the man turning with hope |

Se alguma sair com o rosto diferente, peça: *"refaça mantendo o rosto e a camisa azul-clara da folha"*.

## 3. Narração (Google AI Studio — https://aistudio.google.com/generate-speech)
O AI Studio no navegador é gratuito.
1. Em **Voice**, escolha uma voz masculina (teste **Orus**, **Charon** ou **Fenrir**).
2. Em **Style instructions**, cole: *Narrador brasileiro, masculino, voz próxima e tensa, como quem conta um segredo para um amigo; ritmo rápido, sem pausas longas.*
3. No texto, cole a narração completa (abaixo), gere e baixe como **narracao.wav**.

> Você é taxista. É uma da manhã. E o passageiro que acabou de descer esqueceu uma coisa no banco de trás. Um bilhete. Você confere os números no celular… e bate. Os seis. Quarenta milhões de reais. No seu banco de trás. Agora vem a parte difícil. Porque todo prêmio… tem dono. Problema um: o passageiro. Em dois minutos ele percebe o que esqueceu. E volta correndo. Ele lembra de tudo: táxi branco, placa final sete, a música que tava tocando. Problema dois: a central. Toda corrida fica gravada. Hora, endereço… e o seu nome. Problema três: você vira o bilhete. Tem um nome escrito à caneta. Seu Antônio. E um telefone. E aí você olha no retrovisor. Ele tá lá na esquina. Com as mãos na cabeça. Opção A: você acelera e some na madrugada. Comente GUARDA. Opção B: você desce, atravessa a rua e devolve. Comente DEVOLVE. Mas tem um terceiro jeito escondido nessa imagem. Quase ninguém vê. Comente uma palavra. A parte dois sai amanhã.

## 4. (Opcional) Movimento com Veo 3 (Flow — https://labs.google/fx/tools/flow)
Usa os seus créditos. Prefira o modo **Fast**, que gasta menos. Faça em **Frames to Video**, com a imagem como quadro inicial, 9:16, sem fala:
- **v1** (img01): *Slow push-in from the back seat toward the lottery ticket, rain drops slide on the window, streetlight flickers, ambient rain sound, no dialogue.*
- **v3** (img03): *The driver's eyes widen slowly, a sweat drop rolls down, dashboard light pulses, subtle handheld camera, heartbeat sound, no dialogue.*
- **v7** (img07): *In the mirror the man spins around looking for the taxi, hands on head, a car passes in the foreground, street ambience, no dialogue.*
- **v8** (img08): *The taxi accelerates away, camera tracking alongside, city lights streak past, engine roar, no dialogue.*

## 5. Me mande
Arraste aqui no chat: **folha.png, img01–img09.png, narracao.wav** e, se fizer, **v1/v3/v7/v8.mp4**.
Eu faço o resto: movimento nas imagens, painel de jogo, legendas palavra por palavra, cartões com carimbos, trilha, efeitos e o MP4 final.
