// Contagem dos votos a partir dos comentários do Reel.
// Regras (as mesmas anunciadas no site): um voto por pessoa, vale o último comentário
// feito antes do fechamento; o comentário precisa citar exatamente uma das opções.

const normaliza = (t) => String(t || "").normalize("NFD").replace(/[̀-ͯ]/g, "").toLowerCase();

function opcaoDoComentario(texto, opcoes) {
  const t = " " + normaliza(texto).replace(/[^a-z0-9]+/g, " ") + " ";
  const achadas = opcoes.filter((o) => t.includes(" " + normaliza(o).replace(/[^a-z0-9]+/g, " ").trim() + " "));
  return achadas.length === 1 ? achadas[0] : null;
}

function contar(comentarios, opcoes, fechaEm) {
  const limite = fechaEm ? Date.parse(fechaEm) : Infinity;
  const ultimo = new Map(); // username -> { opcao, ts }
  let outros = 0;
  const ordenados = [...comentarios].sort((a, b) => Date.parse(a.timestamp) - Date.parse(b.timestamp));
  for (const c of ordenados) {
    const ts = Date.parse(c.timestamp);
    if (!c.username || !(ts <= limite)) continue;
    const opcao = opcaoDoComentario(c.text, opcoes);
    if (opcao) ultimo.set(c.username, { opcao, ts });
    else outros++;
  }
  const votos = Object.fromEntries(opcoes.map((o) => [o, 0]));
  for (const { opcao } of ultimo.values()) votos[opcao]++;
  const total = ultimo.size;
  return {
    opcoes: opcoes.map((o) => ({ opcao: o, votos: votos[o], pct: total ? Math.round((votos[o] / total) * 100) : 0 })),
    total,
    outros, // comentários sem voto válido (palpites do 3º jeito, conversa, os dois nomes juntos)
    fechada: Date.now() > limite,
  };
}

module.exports = { contar, opcaoDoComentario, normaliza };
