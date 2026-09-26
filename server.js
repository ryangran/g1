import express from 'express';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { createProvider } from './src/pix/provider.js';
import { isValidCPF } from './src/cpf.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const app = express();
const provider = createProvider();

// Preco do produto em centavos. Ajuste via env PRODUCT_PRICE_CENTS.
const PRODUCT_PRICE_CENTS = Number(process.env.PRODUCT_PRICE_CENTS || 4990);
const PRODUCT_NAME =
  process.env.PRODUCT_NAME || 'Programa Livre de Apostas - Acesso completo';

app.use(express.json());

// Webhook precisa do corpo bruto para validar assinatura do provedor.
app.use('/api/webhook', express.raw({ type: '*/*' }));

app.use(express.static(path.join(__dirname, 'public')));

// Expoe dados do produto para o frontend.
app.get('/api/product', (_req, res) => {
  res.json({ name: PRODUCT_NAME, amountCents: PRODUCT_PRICE_CENTS });
});

// Cria uma cobranca PIX.
app.post('/api/charges', async (req, res) => {
  try {
    const { name, email, cpf } = req.body || {};

    if (!name || String(name).trim().length < 3) {
      return res.status(400).json({ error: 'Informe o nome completo.' });
    }
    if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      return res.status(400).json({ error: 'Informe um e-mail valido.' });
    }
    if (!isValidCPF(cpf)) {
      return res.status(400).json({ error: 'CPF invalido.' });
    }

    const charge = await provider.createCharge({
      amountCents: PRODUCT_PRICE_CENTS,
      description: PRODUCT_NAME,
      payer: {
        name: String(name).trim(),
        email: String(email).trim(),
        cpf: String(cpf).replace(/\D/g, ''),
      },
    });

    res.json(charge);
  } catch (err) {
    console.error('Erro ao criar cobranca:', err);
    res.status(500).json({ error: 'Nao foi possivel criar a cobranca.' });
  }
});

// Consulta o status de uma cobranca (usado pelo polling do frontend).
app.get('/api/charges/:id', async (req, res) => {
  try {
    const charge = await provider.getCharge(req.params.id);
    res.json(charge);
  } catch (err) {
    console.error('Erro ao consultar cobranca:', err);
    res.status(404).json({ error: 'Cobranca nao encontrada.' });
  }
});

// Webhook: o provedor chama aqui quando o pagamento muda de status.
app.post('/api/webhook', async (req, res) => {
  try {
    const rawBody = req.body?.toString('utf8') || '';
    const { chargeId, status } = await provider.parseWebhook(rawBody, req.headers);
    console.log(`Webhook recebido: cobranca ${chargeId} -> ${status}`);
    // Aqui voce libera o acesso ao produto quando status === 'paid'
    // (enviar e-mail com o material, marcar no banco, etc.).
    res.sendStatus(200);
  } catch (err) {
    console.error('Erro no webhook:', err);
    res.sendStatus(400);
  }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Checkout rodando em http://localhost:${PORT}`);
  console.log(`Provedor PIX: ${process.env.PIX_PROVIDER || 'mock'}`);
});
