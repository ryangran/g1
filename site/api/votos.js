// GET /api/votos → placar da votação aberta, lido dos comentários do Reel.
// Variáveis na Vercel (Settings → Environment Variables):
//   IG_TOKEN     token de acesso do Instagram (API do Instagram com login do Instagram)
//   VOTO_OPCOES  ex.: "CIPÓ,PEDRA"
//   VOTO_FECHA   ex.: "2026-10-30T15:00:00-03:00" (opcional)
//   IG_MEDIA_ID  id do Reel da votação (opcional; sem ele usa o post mais recente)
// A resposta fica em cache na CDN por 60 s: o Instagram é consultado no máximo 1 vez por minuto.
const { contar } = require("../lib/contagem");

const API = "https://graph.instagram.com/v21.0";

async function pegar(url) {
  const r = await fetch(url);
  const j = await r.json();
  if (!r.ok || j.error) throw new Error(j.error?.message || `HTTP ${r.status}`);
  return j;
}

async function comentarios(mediaId, token) {
  const todos = [];
  let url = `${API}/${mediaId}/comments?fields=id,text,username,timestamp&limit=50&access_token=${encodeURIComponent(token)}`;
  for (let pag = 0; url && pag < 40; pag++) { // até 2.000 comentários por consulta
    const j = await pegar(url);
    todos.push(...(j.data || []));
    url = j.paging?.next || null;
  }
  return todos;
}

module.exports = async (req, res) => {
  const opcoes = (process.env.VOTO_OPCOES || "CIPÓ,PEDRA").split(",").map((s) => s.trim()).filter(Boolean);
  const fecha = process.env.VOTO_FECHA || null;
  res.setHeader("Content-Type", "application/json; charset=utf-8");
  res.setHeader("Cache-Control", "public, s-maxage=60, stale-while-revalidate=300");
  const token = process.env.IG_TOKEN;
  try {
    if (!token) {
      // sem token ainda: placar de demonstração, marcado como tal
      const demo = [];
      const base = Date.now() - 3600e3;
      for (let i = 0; i < 137; i++) demo.push({ username: `demo${i}`, text: i % 5 < 3 ? opcoes[0] : opcoes[1] || opcoes[0], timestamp: new Date(base + i * 1000).toISOString() });
      for (let i = 0; i < 9; i++) demo.push({ username: `palpite${i}`, text: "acho que é o tronco", timestamp: new Date(base).toISOString() });
      return res.status(200).json({ demo: true, atualizado: new Date().toISOString(), fechaEm: fecha, ...contar(demo, opcoes, null) });
    }
    let mediaId = process.env.IG_MEDIA_ID;
    if (!mediaId) {
      const j = await pegar(`${API}/me/media?fields=id&limit=1&access_token=${encodeURIComponent(token)}`);
      mediaId = j.data?.[0]?.id;
      if (!mediaId) throw new Error("nenhum post encontrado na conta");
    }
    const lista = await comentarios(mediaId, token);
    res.status(200).json({ demo: false, atualizado: new Date().toISOString(), fechaEm: fecha, ...contar(lista, opcoes, fecha) });
  } catch (e) {
    res.setHeader("Cache-Control", "public, s-maxage=30");
    res.status(502).json({ erro: "não foi possível ler os comentários agora", detalhe: String(e.message || e) });
  }
};
