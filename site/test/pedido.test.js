const test = require("node:test");
const assert = require("node:assert");
const res = () => ({ h: {}, setHeader(k, v) { this.h[k] = v; }, status(c) { this.code = c; return this; }, json(o) { this.corpo = o; } });
const pedido = () => { delete require.cache[require.resolve("../api/pedido")]; return require("../api/pedido"); };

test("valida @ e e-mail", async () => {
  const r = res(); await pedido()({ method: "POST", body: { arroba: "@a b", email: "x@y.com" } }, r); assert.equal(r.code, 400);
  const r2 = res(); await pedido()({ method: "POST", body: { arroba: "@ana", email: "sem-arroba" } }, r2); assert.equal(r2.code, 400);
});
test("sem token do Mercado Pago: pagamento em breve", async () => {
  delete process.env.MP_ACCESS_TOKEN;
  const r = res(); await pedido()({ method: "POST", body: { arroba: "ana", email: "ana@x.com" } }, r); assert.equal(r.code, 503);
});
test("cria o Pix com e-mail, @ como referência e validade de 30 min", async () => {
  process.env.MP_ACCESS_TOKEN = "APP_USR-teste";
  let enviado;
  global.fetch = async (url, op) => { enviado = { url, corpo: JSON.parse(op.body), h: op.headers };
    return { ok: true, status: 201, json: async () => ({ id: 123456789, point_of_interaction: { transaction_data: { qr_code: "000201...", qr_code_base64: "iVBOR" } } }) }; };
  const r = res(); await pedido()({ method: "POST", body: JSON.stringify({ arroba: "@Ana.Silva", email: "ana@x.com" }) }, r);
  assert.equal(r.code, 200); assert.equal(r.corpo.id, "123456789"); assert.equal(r.corpo.qr, "000201..."); assert.equal(r.corpo.qr64, "iVBOR");
  assert.match(enviado.url, /\/v1\/payments$/); assert.equal(enviado.corpo.payment_method_id, "pix");
  assert.equal(enviado.corpo.payer.email, "ana@x.com"); assert.equal(enviado.corpo.external_reference, "@Ana.Silva");
  assert.ok(enviado.h["X-Idempotency-Key"]); assert.match(enviado.corpo.date_of_expiration, /-03:00$/);
});

test("status só responde para pagamentos do passe e devolve o número de corrida", async () => {
  process.env.MP_ACCESS_TOKEN = "APP_USR-teste";
  global.fetch = async (url) => ({ ok: true, json: async () => url.includes("search")
    ? { results: [{ id: 111, external_reference: "@a" }, { id: 999, external_reference: "outra" }, { id: 123456789, external_reference: "@b" }] }
    : { id: 123456789, status: "approved", external_reference: "@b" } });
  delete require.cache[require.resolve("../api/status")];
  const r = res(); await require("../api/status")({ query: { id: "123456789" } }, r);
  assert.equal(r.code, 200); assert.equal(r.corpo.status, "approved"); assert.equal(r.corpo.numero, 2);
  global.fetch = async () => ({ ok: true, json: async () => ({ id: 5, status: "approved", external_reference: "venda-loja" }) });
  const r2 = res(); await require("../api/status")({ query: { id: "1234567" } }, r2); assert.equal(r2.code, 404);
});
