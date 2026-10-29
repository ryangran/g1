# Site da série (estilo "painel do jogo")

Site estático com uma página, pensado primeiro para o celular (o público vem do link da bio). A estrutura segue a análise em `estudio/referencias/site-orastro-analise.md`. O visual e a marca são nossos.

- **`serie.js`**: todo o conteúdo da série (textos, painel, votação, partes, capas, agentes, links, preço). Para trocar de série, edite só esse arquivo e as capas em `assets/capas/`.
- **`index.html`**: layout e lógica (contagem até a próxima parte, mural, vagas, ranking, arquivo, formulário).

## A cada parte nova
1. Adicione a parte em `partes` (capa = um quadro do render, extraído com ffmpeg) e atualize `votacao`, `painel` e `mural`.
2. Anote a decisão da parte anterior (ex.: `"Cipó · 62%"`). Use só números reais da contagem dos comentários.
3. Adicione os agentes pagos em `agentes` (`arroba`, `numero`, `partes`, `parteAtual`).

## Pagamento
`linkPagamento` vazio faz o botão mostrar "Pagamento abre em breve" (nada é cobrado). Para cobrar:
1. Crie um **Link de pagamento** de R$ 9,90 no Mercado Pago, com Pix.
2. Cole o link em `linkPagamento`.

O site **não guarda** dados de ninguém. Ele só leva o @ junto para o link de pagamento, e a conferência é feita no painel do Mercado Pago.

## Publicar
`./site/publicar.sh` sobe o site para https://obilhete.vercel.app. Na Vercel, o projeto `obilhete` já tem `IG_TOKEN`, `IG_USER_ID` e `VOTO_OPCOES`.

## Ver localmente
`npx serve site`, ou abra o `index.html` direto no navegador.
