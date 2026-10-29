# Análise do site orastro.online (referência para o nosso site)

Vi o site em 29/10/2026, no celular (420 px) e pelo HTML. Ele é o "hub" da série de reels do motoboy (`@juninho.orastro`).

## Como ele encaixa a história
O site **não conta a história**: ela vive nos reels. O site transforma a série num **jogo contínuo** e é a fonte de receita. A ordem das seções:

1. **Faixa rolante no topo:** "PARTE 10 · MENTE OU PULA · VOTE NO REEL" (o episódio atual sempre à vista).
2. **Herói:** "Ele achou R$ 8 milhões. **Você decide.**" Embaixo, uma frase explica o formato (todo dia sai uma parte e os comentários escrevem a próxima). Botões: "Seu @ no episódio · R$ 9,90" e "Assistir no Instagram".
3. **O mesmo HUD do vídeo:** NA MALA R$ 7.700.000 · SUSPEITA 99% (com barra) · contagem "PRÓXIMA PARTE EM hh:mm:ss".
4. **Quadro de investigação (cortiça):** fotos das partes presas com alfinete e linhas vermelhas, mais etiquetas "SUSPEITA 99%" e "R$ 7.700.000 enterrados". É o resumo visual da história até agora.
5. **Votação aberta:** "Daqui pra frente, você me mostra." O voto é pelo comentário do Reel (um voto por pessoa, fecha às 15h). Tem a dica "👀 Tem um 3º jeito escondido" e os botões das opções, que levam ao Reel.
6. **Passe de Agente (monetização, R$ 9,90 por Pix):** o @ da pessoa aparece **dentro da cena** (pasta, muro, tela de celular, créditos) e na legenda do Reel. Ela ganha número de agente e entra no ranking.
7. **Quadro do caso, parte seguinte:** 10 vagas em cartões de papel, com as vagas livres tracejadas.
8. **Formulário:** @ do Instagram, e-mail e aceite dos termos; Pix pelo Mercado Pago, com o QR na própria página.
9. **Ranking "Mais Procurados":** cartazes de PROCURADO com silhueta e #1, #2, #3.
10. **Arquivo do caso:** carrossel com todas as partes e **o que o público decidiu** em cada uma (ex.: "Enterrar a mala 65%").
11. **Regras reais do caso:** um cartão por parte. *Nós não usamos isso: nossas histórias são 100% ficção, sem leis.*
12. **Números do caso:** visualizações, comentários, seguidores, partes.
13. **Perguntas frequentes**, rodapé ("História fictícia… Cada centavo deixa rastro") e cookies.

## Visual
- Fundo quase preto `#14120f` com gradiente âmbar no topo e amarelo `#ffd23a` como cor de ação.
- Cartões em creme `#efe9df`, papel e cortiça, fita e alfinete vermelho.
- Fonte mono para os kickers (caixa alta espaçada) e títulos pesados sem serifa.
- Layout de uma coluna, pensado primeiro para celular, porque o público vem do link da bio.

## O que levar para o nosso site
- O **mesmo HUD e o mesmo vocabulário** do vídeo (o site é "o painel do jogo").
- **Votação apontando para o comentário do Reel**: o engajamento fica no Instagram, que é o que o algoritmo mede.
- **Arquivo com o % de cada decisão:** prova social e um motivo para maratonar.
- **Contagem regressiva** para a próxima parte.
- **"Seu @ na cena"** como produto. No HyperFrames isso é fácil: o @ vira variável (`data-var-text`) num cartaz da cena e na lista de créditos, renderizado por parte.
- Hospedagem simples: um site estático (Vercel, já conectado) e, se for cobrar, um link de pagamento pronto (Mercado Pago ou Stripe) antes de construir algo próprio.
