# O BILHETE · Parte 2 — os três caminhos (escrevo a final quando a votação fechar)

A Parte 2 sai do resultado real dos comentários: `estudio/tools/comentarios.py` gera `build/votacao.json`.
O ramo vencedor vira roteiro final, narração na voz fixa, cenas e render. Duração alvo: 85–95 s.

## Abertura comum (igual nos três ramos, cerca de 25 s)
1. **Gancho (0–5 s):** "O Clóvis tem quarenta milhões no banco de trás… e um homem de terno vindo na direção dele."
2. **Vocês decidiram (5–12 s):** tela preta com o placar em barras (ACELERA X% · ESPERA Y% · 3º JEITO · O RECIBO Z%). Narração: "X% de vocês mandaram…, Y mandaram… e Z% acharam o recibo."
3. **Crédito ao público (12–18 s):** cartão "1º A ACHAR · N MIN · @fulano", mais o balão do comentário mais curtido com o selo **ANOTADO ✓** (ou **GUARDA ESSA 👀**, se a ideia for usada depois).
4. **Corridas da madrugada (18–25 s):** a tela do app do Clóvis com o histórico de corridas e o @ dos **Passageiros da madrugada** que pagaram, cada um com horário e destino. Narração: "E a central registrou mais dez corridas essa noite. Os nomes tão aí na tela. Quer o seu na próxima? São só dez vagas, o link tá na bio."

## A virada da Parte 2 (vale para qualquer ramo)
O homem de terno é **Rodrigo**, sobrinho do Seu Antônio. O tio ganhou na loteria e contou só para ele. Rodrigo tirou o bilhete da carteira do velho e foi ao Hotel Imperial vender para um "comprador de bilhete" pela metade do valor. Ele esqueceu o bilhete no táxi.
- **Pista visual:** o crachá do hotel / a chave do quarto com o nome "RODRIGO A." aparece na cena.
- **Regra 2 do Código da Madrugada:** *"Quem tem pressa de pegar… não é o dono."*

## Ramo A — ACELERA venceu
- O Clóvis arranca. No retrovisor, o Rodrigo **fotografa a placa** (final 7).
- Dez minutos depois, o rádio da central chama: "Clóvis, um passageiro do Imperial quer falar com você. Disse que é **urgente** e pediu o seu nome. Eu passei." *(o problema 2 da Parte 1 cobra a conta)*
- No sinal vermelho, uma **SUV preta** encosta do lado. O vidro desce devagar…
- **Risco:** 85 → 95%.
- **Escolha:** **POSTO** (entrar num posto 24 h cheio de gente e esperar) × **LIGA** (ligar para o número atrás do bilhete).
- **3º jeito escondido:** a viatura de polícia parada na esquina, no fundo da cena do sinal.

## Ramo B — ESPERA venceu
- O Rodrigo chega sorrindo: "Meu bilhete, campeão." Ele oferece **R$ 5 mil** "pela honestidade", o que é rápido demais e generoso demais.
- O Clóvis pergunta o nome. "Antônio." Mas o **cartão-chave do hotel** no bolso do terno diz **RODRIGO A.** (pista visual).
- O porteiro chama: "Seu Rodrigo, o seu comprador chegou." Uma SUV preta para atrás do táxi.
- **Risco:** 85 → 90%.
- **Escolha:** **ENTREGA** (pega os R$ 5 mil e vai embora) × **MENTE** ("que bilhete? não tinha nada").
- **3º jeito escondido:** a câmera de segurança do hotel, apontada para o táxi, com a luz vermelha piscando.

## Ramo C — o 3º JEITO venceu (o recibo)
- O Clóvis dirige até a **Rua das Acácias, 51**. A casa está escura e o portão aberto.
- A vizinha, de bobe e roupão, sai na janela: "O Seu Antônio passou mal à tarde. Foi pro Hospital São Lucas. Quem levou foi o sobrinho… o **Rodrigo**. Levou a carteira dele também."
- No fim da rua, a SUV preta do comprador apaga o farol.
- **Risco:** 85 → 70% (ele está do lado certo, mas o perigo chegou).
- **Escolha:** **HOSPITAL** (ir ao Seu Antônio agora) × **VIZINHA** (deixar o bilhete com ela e sumir).
- **3º jeito escondido:** a placa da SUV refletida no vidro do táxi, igual à que estava na frente do hotel na Parte 1.

## Fecho comum
"O que a gente faz agora? Opção A… Comente X. Opção B… Comente Y. Ou tem um terceiro jeito escondido nessa parte. Só vale se você disser qual é. A maioria escreve a parte três amanhã."

## Passageiros da madrugada (quem pagou R$ 9,90)
Lista em `build/passageiros.json` no formato abaixo. Cada pessoa aparece na tela "Corridas da madrugada" e entra na legenda do Reel:
```json
[{ "arroba": "@fulano", "numero": 1, "hora": "00:41", "destino": "Centro" }]
```
