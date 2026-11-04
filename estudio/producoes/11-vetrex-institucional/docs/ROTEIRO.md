# Vetrex — institucional (38 s, 9:16)

Referência de estilo: vídeo da Axye enviado pelo cliente (fundo preto, ondas roxas, texto cinético
sincronizado com a narração, cards de interface, fecho com a marca).

Voz: Gemini TTS **Orus** (a voz do estúdio), com instrução de locutor de comercial (`tools/estilo.txt`).
Trilha: gerada em `tools/gerar_trilha.py` (sub + hat + pad, cresce até o fecho).

| # | Narração | Tela |
|---|---|---|
| 1 | Você mandou sua divulgação. Pra três grupos. E parou por aí. | 3 grupos no WhatsApp com poucas visualizações |
| 2 | A Vetrex existe pra isso não acontecer. | marca surgindo, wordmark em wipe |
| 3 | Sua mensagem sai todo dia, no automático, em grupos e no status do WhatsApp. | celular com status + lista de grupos, números subindo |
| 4 | Você escreve uma vez. O bot cuida do resto. | fluxo de 4 passos |
| 5 | Escolheu. Pagou. Disparou. | três palavras grandes |
| 6 | Dez reais o dia. E quanto mais dias você pega, menor fica o valor. | "R$ 10 por dia" em tela cheia, depois as barras (1, 7, 15, 30) |
| 7 | Precisa de público novo? Tem venda de link de grupo também. | cards de link de grupo |
| 8 | Tudo dentro do Telegram. Num bot só. | menu do bot no Telegram |
| 9 | Sem painel complicado. Sem instalar nada. | lista do que NÃO precisa + "só o bot no Telegram" |
| 10 | Vetrex. O seu recado onde o seu público já está. | logo + slogan + t.me/vetrexzapbot |

## A conferir com o cliente
- **Preços reais por faixa de dias.** Só o "R$ 10 por dia" veio do cliente; as outras faixas aparecem
  como barras decrescentes ("menos por dia"), sem número inventado. Mandando a tabela, entram os valores.
- Nomes de grupos, contagens e visualizações das telas são **exemplos de interface**, não dados reais.

## Decisões da versão 2 (pedido do cliente em 04/11)
- A voz fala **só "Vetrex"**, nunca "Vetrex Networking"; a logo em tela usa só a marca + "vetrex"
  (`assets/img/wordmark-sm.png`, recortada sem a linha NETWORKING).
- **12 cenas** em vez de 7, com corte marcado: faixa roxa cruzando a tela + whoosh + impacto grave.
- **Legendas em blocos de até 3 palavras** que trocam a cada ~0,7 s, com entrada em escala e saída
  para cima. Nenhum bloco divide a tela com outro (foi o que sobrepunha no começo da v1).
- **Zonas fixas:** interface de 250 a 1340 px, legenda a partir de 1440 px. Nunca se encostam.
- Nas cenas "Escolheu. Pagou. Disparou." e no fecho a legenda some, porque o texto já está grande na tela.
- Som: 66 efeitos (impacto a cada corte, cliques nas listas, riser antes do bloco de três palavras,
  glitch na marca, ping e chime no fim) + trilha com pulso que cresce.
