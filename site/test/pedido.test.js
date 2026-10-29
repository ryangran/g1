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
test("cria a preferência só com Pix, e-mail do pagador e o @ como referência", async () => {
  process.env.MP_ACCESS_TOKEN = "APP_USR-teste";
  let enviado;
  global.fetch = async (url, op) => { enviado = { url, corpo: JSON.parse(op.body), auth: op.headers.Authorization }; return { ok: true, status: 201, json: async () => ({ init_point: "https://mp/pagar/123" }) }; };
  const r = res(); await pedido()({ method: "POST", headers: { host: "obilhete.vercel.app" }, body: JSON.stringify({ arroba: "@Ana.Silva", email: "ana@x.com" }) }, r);
  assert.equal(r.code, 200); assert.equal(r.corpo.link, "https://mp/pagar/123");
  assert.equal(enviado.corpo.payer.email, "ana@x.com"); assert.equal(enviado.corpo.external_reference, "@Ana.Silva");
  assert.equal(enviado.corpo.items[0].unit_price, 9.9); assert.match(enviado.auth, /^Bearer /);
  assert.deepEqual(enviado.corpo.payment_methods.excluded_payment_types.map((x) => x.id), ["credit_card", "debit_card", "ticket"]);
});
