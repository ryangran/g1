const test = require("node:test");
const assert = require("node:assert");

function resFalso() {
  const r = { headers: {}, code: 0, corpo: null };
  r.setHeader = (k, v) => (r.headers[k] = v);
  r.status = (c) => ((r.code = c), r);
  r.json = (o) => (r.corpo = o);
  return r;
}

test("lê o post mais recente, segue a paginação e conta", async () => {
  process.env.IG_TOKEN = "x"; process.env.VOTO_OPCOES = "CIPÓ,PEDRA"; delete process.env.IG_MEDIA_ID; delete process.env.VOTO_FECHA;
  const chamadas = [];
  global.fetch = async (url) => {
    chamadas.push(url);
    const corpo = url.includes("/me/media") ? { data: [{ id: "123" }] }
      : url.includes("after=2") ? { data: [{ username: "b", text: "pedra", timestamp: "2026-10-30T10:00:00Z" }] }
      : { data: [{ username: "a", text: "Cipó!", timestamp: "2026-10-30T10:00:00Z" }], paging: { next: "https://graph.instagram.com/v21.0/123/comments?after=2" } };
    return { ok: true, status: 200, json: async () => corpo };
  };
  delete require.cache[require.resolve("../api/votos")];
  const res = resFalso();
  await require("../api/votos")({}, res);
  assert.equal(res.code, 200);
  assert.equal(res.corpo.demo, false);
  assert.equal(res.corpo.total, 2);
  assert.equal(chamadas.length, 3);
  assert.match(chamadas[1], /\/123\/comments/);
});

test("erro do Instagram vira 502 sem derrubar o site", async () => {
  process.env.IG_TOKEN = "x";
  global.fetch = async () => ({ ok: false, status: 400, json: async () => ({ error: { message: "token expirado" } }) });
  const res = resFalso();
  await require("../api/votos")({}, res);
  assert.equal(res.code, 502);
  assert.match(res.corpo.detalhe, /token expirado/);
});

test("token EAA (login unificado) lê pela conta em graph.facebook.com", async () => {
  process.env.IG_TOKEN = "EAAteste"; process.env.IG_USER_ID = "17841450576591219"; delete process.env.IG_MEDIA_ID;
  const chamadas = [];
  global.fetch = async (url) => {
    chamadas.push(url);
    const corpo = url.includes("/media") ? { data: [{ id: "999" }] } : { data: [{ username: "a", text: "espera", timestamp: "2026-10-30T10:00:00Z" }] };
    return { ok: true, status: 200, json: async () => corpo };
  };
  delete require.cache[require.resolve("../api/votos")];
  const res = { headers: {}, setHeader() {}, status(c) { this.code = c; return this; }, json(o) { this.corpo = o; } };
  await require("../api/votos")({}, res);
  assert.equal(res.code, 200);
  assert.match(chamadas[0], /graph\.facebook\.com\/v21\.0\/17841450576591219\/media/);
  assert.match(chamadas[1], /graph\.facebook\.com\/v21\.0\/999\/comments/);
});
