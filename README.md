# Checkout PIX — Programa Livre de Apostas

Checkout simples para vender um produto digital anti-vício em apostas, com
pagamento via PIX. A camada de pagamento é **plugável**: o checkout inteiro
conhece só a interface `PixProvider`, então você conecta o seu provedor
implementando um arquivo, sem tocar no frontend.

## Rodar localmente

```bash
npm install
cp .env.example .env   # ajuste o preço/nome do produto se quiser
npm start              # http://localhost:3000
```

Com `PIX_PROVIDER=mock` (padrão), a cobrança é simulada e marcada como paga
após ~8 segundos, para você testar a tela de confirmação ponta a ponta.

## Plugar o seu provedor de PIX

Quando tiver a documentação da sua API:

1. Crie `src/pix/meuProvider.js` com uma classe que implemente a interface
   descrita em `src/pix/provider.js`:
   - `createCharge({ amountCents, description, payer })` → cria a cobrança e
     devolve `{ id, status, qrCode, amountCents, ... }`.
   - `getCharge(id)` → devolve o status atual (usado pelo polling).
   - `parseWebhook(rawBody, headers)` → valida a notificação e devolve
     `{ chargeId, status }`.
2. Registre-o no `switch` de `createProvider()` em `src/pix/provider.js`.
3. Ponha as credenciais no `.env` e mude `PIX_PROVIDER`.

Me manda a doc da API que eu escrevo esse adaptador pra você.

## Estrutura

```
server.js              rotas: /api/product, /api/charges, /api/webhook
src/pix/provider.js    interface + fábrica de provedor
src/pix/mockProvider.js provedor de teste (sem banco real)
src/cpf.js             validação de dígitos do CPF (sem consulta externa)
public/                frontend do checkout
```

## Observações

- O CPF é usado **apenas** como dado de cobrança exigido pelo PIX. Nada é
  consultado em nome do cliente e nenhum dado pessoal é buscado por CPF.
- A página é honesta sobre o que vende e inclui o canal de ajuda (CVV 188).
- Configure o webhook do seu provedor para `POST /api/webhook` e libere o
  acesso ao produto quando o status for `paid`.
