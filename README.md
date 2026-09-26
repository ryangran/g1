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

## Usar o NOMAPAY (produção)

O adaptador do NOMAPAY já está pronto em `src/pix/nomapayProvider.js`. Para ativar:

1. No `.env`:
   ```
   PIX_PROVIDER=nomapay
   NOMAPAY_PUBLIC_KEY=fsp_pk_live_...
   NOMAPAY_SECRET_KEY=fsp_sk_live_...
   NOMAPAY_POSTBACK_URL=https://seusite.com.br/api/webhook
   ```
2. No painel do NOMAPAY, cadastre o webhook apontando para `POST /api/webhook`
   do seu deploy (o mesmo valor de `NOMAPAY_POSTBACK_URL`).
3. O webhook valida a assinatura `x-nomapay-signature` (HMAC SHA-256). Por
   padrão usa a `NOMAPAY_SECRET_KEY`; se o painel gerar um segredo próprio de
   webhook, coloque-o em `NOMAPAY_WEBHOOK_SECRET`.

O adaptador mapeia os status do gateway (`WAITING_PAYMENT` → `pending`,
`PAID` → `paid`, etc.) e converte reais ↔ centavos automaticamente.

## Testar a integração NOMAPAY (do seu ambiente)

Rode isto onde as chaves live legitimamente vivem (sua máquina ou o deploy),
nunca cole a Secret Key em chats ou ferramentas de terceiros:

```bash
# .env com PIX_PROVIDER=nomapay e as chaves
npm start
# em outro terminal:
curl -s -X POST localhost:3000/api/charges \
  -H 'Content-Type: application/json' \
  -d '{"name":"Cliente Teste","email":"teste@example.com","cpf":"52998224725"}'
```

### Se voltar HTTP 403 em POST /transactions
O 403 vem do gateway (não do código). Causas mais comuns, em ordem:
1. **IP não autorizado** — muitos gateways exigem allowlist de IP para chaves
   `live`. Rode do IP do seu servidor/deploy e cadastre-o no painel.
2. **Chave inativa/regenerada** — confirme no painel que a chave em uso está
   ativa (se você regenerou depois de expor, atualize o `.env`).
3. **Conta ainda não habilitada** para transações live.
4. **Esquema de auth** — a doc aceita `Basic base64(PK:SK)` (o que usamos) ou
   `Bearer {SK}`. Se o suporte do NOMAPAY indicar Bearer, dá pra alternar.

Com o corpo do erro em mãos (`res.text()` do 403), o motivo exato aparece.

## Plugar outro provedor

Crie `src/pix/<nome>Provider.js` implementando a interface de
`src/pix/provider.js` (`createCharge`, `getCharge`, `parseWebhook`) e registre-o
no `switch` de `createProvider()`.

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
