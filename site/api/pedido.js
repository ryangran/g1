// POST /api/pedido { arroba, email } → cria um Pix no Mercado Pago (API de pagamentos) e devolve o QR Code.
// O @ vai como external_reference (aparece no painel do Mercado Pago); o e-mail recebe o comprovante.
// GET /api/pedido → { ativo } (se o pagamento está ligado).
// Variáveis na Vercel: MP_ACCESS_TOKEN. Opcional: PRECO (padrão 9.90).
const crypto = require("crypto");
const ARROBA = /^@[A-Za-z0-9._]{1,30}$/;
const EMAIL = /^[^@\s]+@[^@\s]+\.[^@\s]+$/;
const VALIDADE_MIN = 30;

module.exports = async (req, res) => {
  res.setHeader("Content-Type", "application/json; charset=utf-8");
  res.setHeader("Cache-Control", "no-store");
  if (req.method === "GET") return res.status(200).json({ ativo: Boolean(process.env.MP_ACCESS_TOKEN) });
  if (req.method !== "POST") return res.status(405).json({ erro: "use POST" });
  let corpo = req.body;
  if (typeof corpo === "string") { try { corpo = JSON.parse(corpo); } catch { corpo = {}; } }
  const arroba = String(corpo?.arroba || "").trim().replace(/^@*/, "@");
  const email = String(corpo?.email || "").trim();
  if (!ARROBA.test(arroba)) return res.status(400).json({ erro: "Confira seu @ do Instagram." });
  if (!EMAIL.test(email)) return res.status(400).json({ erro: "Confira seu e-mail." });
  const token = process.env.MP_ACCESS_TOKEN;
  if (!token) return res.status(503).json({ erro: "Pagamento abre em breve." });
  // o Mercado Pago exige o formato yyyy-MM-ddTHH:mm:ss.SSS-03:00
  const exp = new Date(Date.now() + VALIDADE_MIN * 60e3 - 3 * 3600e3).toISOString().replace("Z", "-03:00");
  const pagamento = {
    transaction_amount: Number(process.env.PRECO || 9.9),
    description: "Passageiro da madrugada · O Bilhete",
    payment_method_id: "pix",
    payer: { email },
    external_reference: arroba,
    metadata: { arroba },
    date_of_expiration: exp,
    statement_descriptor: "OBILHETE",
  };
  try {
    const r = await fetch("https://api.mercadopago.com/v1/payments", {
      method: "POST",
      headers: { Authorization: `Bearer ${token}`, "Content-Type": "application/json", "X-Idempotency-Key": crypto.randomUUID() },
      body: JSON.stringify(pagamento),
    });
    const j = await r.json();
    const t = j?.point_of_interaction?.transaction_data;
    if (!r.ok || !t?.qr_code) throw new Error(j.message || `HTTP ${r.status}`);
    res.status(200).json({ id: String(j.id), qr: t.qr_code, qr64: t.qr_code_base64, minutos: VALIDADE_MIN });
  } catch (e) {
    res.status(502).json({ erro: "Não deu para gerar o Pix agora. Tente de novo em instantes.", detalhe: String(e.message || e) });
  }
};
