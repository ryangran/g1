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
