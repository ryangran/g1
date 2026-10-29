// GET /api/status?id=<pagamento> → { status, numero? }. Só responde para pagamentos do passe (external_reference = @).
// Quando aprovado, "numero" é a ordem do pagamento entre todos os passes aprovados (o número de corrida).
const pegar = async (url, token) => {
  const r = await fetch(url, { headers: { Authorization: `Bearer ${token}` } });
  return { ok: r.ok, j: await r.json() };
};

module.exports = async (req, res) => {
  res.setHeader("Content-Type", "application/json; charset=utf-8");
  res.setHeader("Cache-Control", "no-store");
  const id = String(req.query?.id || new URL(req.url || "/", "http://x").searchParams.get("id") || "");
  const token = process.env.MP_ACCESS_TOKEN;
  if (!/^\d{6,20}$/.test(id) || !token) return res.status(400).json({ erro: "pedido inválido" });
  try {
    const { ok, j } = await pegar(`https://api.mercadopago.com/v1/payments/${id}`, token);
    if (!ok || !String(j.external_reference || "").startsWith("@")) return res.status(404).json({ erro: "não encontrado" });
    const saida = { status: j.status };
    if (j.status === "approved") {
      const busca = await pegar("https://api.mercadopago.com/v1/payments/search?status=approved&sort=date_approved&criteria=asc&limit=1000", token);
      const passes = (busca.j.results || []).filter((p) => String(p.external_reference || "").startsWith("@"));
      const i = passes.findIndex((p) => String(p.id) === id);
      if (i >= 0) saida.numero = i + 1;
    }
    res.status(200).json(saida);
  } catch (e) {
    res.status(502).json({ erro: "tente de novo" });
  }
};
