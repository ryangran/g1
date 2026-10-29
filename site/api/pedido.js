// POST /api/pedido { arroba, email } → cria o pagamento no Mercado Pago (Checkout Pro, só Pix) e devolve o link.
// O Mercado Pago manda o comprovante para o e-mail; o @ vai como external_reference (aparece no seu painel).
// Variáveis na Vercel: MP_ACCESS_TOKEN (Credenciais de produção → Access token). Opcional: PRECO (padrão 9.90).
// Sem MP_ACCESS_TOKEN, responde 503 e o site mostra "Pagamento abre em breve".
const ARROBA = /^@[A-Za-z0-9._]{1,30}$/;
const EMAIL = /^[^@\s]+@[^@\s]+\.[^@\s]+$/;

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
  const host = req.headers?.host ? `https://${req.headers.host}` : "https://obilhete.vercel.app";
  const preferencia = {
    items: [{ title: "Passageiro da madrugada · O Bilhete", quantity: 1, currency_id: "BRL", unit_price: Number(process.env.PRECO || 9.9) }],
    payer: { email },
    external_reference: arroba,
    metadata: { arroba, email },
    payment_methods: { excluded_payment_types: [{ id: "credit_card" }, { id: "debit_card" }, { id: "ticket" }], installments: 1 },
    back_urls: { success: `${host}/?pago=1#passe`, pending: `${host}/?pago=0#passe`, failure: `${host}/?pago=0#passe` },
    auto_return: "approved",
    statement_descriptor: "OBILHETE",
  };
  try {
    const r = await fetch("https://api.mercadopago.com/checkout/preferences", {
      method: "POST", headers: { Authorization: `Bearer ${token}`, "Content-Type": "application/json" }, body: JSON.stringify(preferencia),
    });
    const j = await r.json();
    if (!r.ok || !j.init_point) throw new Error(j.message || `HTTP ${r.status}`);
    res.status(200).json({ link: j.init_point });
  } catch (e) {
    res.status(502).json({ erro: "Não deu para abrir o pagamento agora. Tente de novo em instantes.", detalhe: String(e.message || e) });
  }
};
