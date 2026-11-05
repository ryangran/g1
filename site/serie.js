// Tudo que muda de série para série fica aqui. O index.html só lê este objeto.
window.SERIE = {
  marca: "O BILHETE",
  logoLetra: "B",
  tituloPagina: "O Bilhete · Você decide o que o Clóvis faz com R$ 40 milhões",
  rodape: "História fictícia, personagens fictícios. Todo prêmio tem dono.",
  instagram: "https://www.instagram.com/clovis.obilhete/",
  reelAtual: "https://www.instagram.com/reel/DfYDe0mAdR5/",  // Reel da votação aberta
  tiktok: "", youtube: "",
  precoPasse: "R$ 9,90",
  vagasPorParte: 10,
  horaParte: 19,
  horaFechaVoto: 15,

  heroKicker: "Série interativa no Instagram",
  arroba: "@clovis.obilhete",
  heroTitulo: "Ele achou R$ 40 milhões.",
  heroDestaque: "Você decide.",
  heroTexto: "Um taxista achou um bilhete premiado no banco de trás do táxi. Todo dia sai uma parte, e os comentários escrevem a próxima.",

  painel: [
    { rotulo: "No banco de trás", valor: "R$ 40 mi" },
    { rotulo: "Na mala", valor: "R$ 20 mi" },
    { rotulo: "Risco", valor: "99%", barra: 99, alerta: true },
  ],

  votacao: {
    parte: 7,
    titulo: "Fica ou devolve?",
    chamada: "O bilhete voltou pro dono. A mala com R$ 20 milhões, não.",
    opcoes: ["FICA", "DEVOLVE"],
    dica: "",
  },

  partes: [
    { n: 1, titulo: "Todo prêmio tem dono", capa: "assets/capas/parte1.jpg", cena: "assets/capas/hotel.jpg", decisao: "Acelera · 75%", link: "https://www.instagram.com/reel/DfIm0RTin1y/" },
    { n: 2, titulo: "Quem tem pressa", capa: "assets/capas/parte2.jpg", cena: "assets/capas/carro-preto.jpg", decisao: "Posto · 100%", link: "https://www.instagram.com/reel/DfLLnsmFCrZ/" },
    { n: 3, titulo: "Todo comprador tem pressa", capa: "assets/capas/parte3.jpg", cena: "assets/capas/posto.jpg", decisao: "Vende · 100%", link: "https://www.instagram.com/reel/DfN9lWiEZp6/" },
    { n: 4, titulo: "Todo dinheiro tem dono", capa: "assets/capas/parte4.jpg", cena: "assets/capas/posto.jpg", decisao: "Vai · 100%", link: "https://www.instagram.com/reel/DfQVEBoGHRF/" },
    { n: 5, titulo: "Todo bilhete tem um nome", capa: "assets/capas/parte5.jpg", cena: "assets/capas/posto.jpg", decisao: "3º jeito · o vídeo", link: "https://www.instagram.com/reel/DfTGqr0DhBF/" },
    { n: 6, titulo: "Quem vendeu o velho", capa: "assets/capas/parte6.jpg", cena: "assets/capas/posto.jpg", decisao: "Sem votos · o estúdio escolheu", link: "https://www.instagram.com/reel/DfVeo_NHA1x/" },
    { n: 7, titulo: "Metade de cada", capa: "assets/capas/parte7.jpg", cena: "assets/capas/posto.jpg", decisao: null, link: "https://www.instagram.com/reel/DfYDe0mAdR5/" },
  ],
  // mural: 5 fotos em volta (troque por cenas de cada parte conforme forem saindo); o centro vem da última parte
  mural: [
    { capa: "assets/capas/susto.jpg", legenda: "O SUSTO" },
    { capa: "assets/capas/verso.jpg", legenda: "SEU ANTÔNIO" },
    { capa: "assets/capas/placa.jpg", legenda: "FINAL 7" },
    { capa: "assets/capas/homem.jpg", legenda: "QUEM É ELE?" },
    { capa: "assets/capas/carro-preto.jpg", legenda: "O CARRO PRETO" },
  ],
  notaMural: "O bilhete voltou pro dono. A mala, não.",
  etiquetas: ["RISCO 99%", "R$ 40.000.000 no banco de trás"],

  // a vaga paga dentro da história
  passe: {
    nav: "Entrar na corrida",
    kicker: "Passageiro da madrugada",
    titulo: "Seu @ dentro do táxi do Clóvis.",
    texto: "Cada passe vale uma parte. Seu @ aparece no histórico de corridas do Clóvis, dentro do episódio, e na legenda do Reel. A central registra tudo, inclusive você.",
    cards: [
      { ic: "🚕", t: "No app do Clóvis", p: "Seu @ aparece na tela \"Corridas da madrugada\" do celular dele, com horário e destino. Pause, ache seu nome, marque os amigos." },
      { ic: "📝", t: "Na legenda do Reel", p: "\"🚕 Passageiros da Parte 2: @você\", clicável para todo mundo que assistir." },
      { ic: "🎫", t: "Número de corrida", p: "Corrida nº 001, 002, 003… O seu é para sempre e mostra quem embarcou primeiro." },
      { ic: "⭐", t: "Passageiros VIP", p: "Quem entra em mais partes sobe no ranking. Os 3 primeiros ganham um retrato desenhado no banco de trás do táxi." },
    ],
    aceite: "Concordo em aparecer como passageiro numa história de ficção, com meu @ visível no vídeo, na legenda e neste site.",
    botao: "Entrar na corrida",
    rotulo: "CORRIDA",
    quadro: "CORRIDAS DA MADRUGADA",
    cartaz: "PASSAGEIRO VIP",
    rankNav: "Passageiros VIP",
    rankTitulo: "Passageiros VIP",
    rankTexto: "Classificados por quantas partes já embarcaram.",
    faqMais: "Pode. Cada passe vale uma parte. Quanto mais partes, mais você sobe entre os Passageiros VIP.",
  },

  agentes: [],   // passageiros pagos: { arroba: "@fulano", numero: 1, partes: 3, parteAtual: 2 }
  numeros: [],   // números reais do perfil (nunca inventar)
};
