const test = require("node:test");
const assert = require("node:assert");
const { contar, opcaoDoComentario } = require("../lib/contagem");
const O = ["CIPÓ", "PEDRA"];

test("reconhece a opção com ou sem acento, em qualquer caixa e com emoji", () => {
  assert.equal(opcaoDoComentario("cipo!!", O), "CIPÓ");
  assert.equal(opcaoDoComentario("Vai de PEDRA 🐊", O), "PEDRA");
  assert.equal(opcaoDoComentario("Cipó", O), "CIPÓ");
});
test("ignora comentário com as duas opções ou nenhuma", () => {
  assert.equal(opcaoDoComentario("cipó ou pedra?", O), null);
  assert.equal(opcaoDoComentario("o tronco escondido", O), null);
  assert.equal(opcaoDoComentario("pedras", O), null); // palavra inteira
});
test("um voto por pessoa, vale o último antes do fechamento", () => {
  const r = contar([
    { username: "a", text: "cipó", timestamp: "2026-10-30T10:00:00-03:00" },
    { username: "a", text: "pedra", timestamp: "2026-10-30T11:00:00-03:00" },
    { username: "b", text: "cipó", timestamp: "2026-10-30T12:00:00-03:00" },
    { username: "b", text: "pedra", timestamp: "2026-10-30T16:00:00-03:00" }, // depois do fechamento
    { username: "c", text: "acho que é o tronco", timestamp: "2026-10-30T12:00:00-03:00" },
  ], O, "2026-10-30T15:00:00-03:00");
  assert.deepEqual(r.opcoes, [{ opcao: "CIPÓ", votos: 1, pct: 50 }, { opcao: "PEDRA", votos: 1, pct: 50 }]);
  assert.equal(r.total, 2);
  assert.equal(r.outros, 1);
});
