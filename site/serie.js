// Tudo que muda de série para série fica aqui. O index.html só lê este objeto.
window.SERIE = {
  marca: "O BILHETE",
  logoLetra: "B",
  tituloPagina: "O Bilhete · Você decide o que o Clóvis faz com R$ 40 milhões",
  rodape: "História fictícia, personagens fictícios. Todo prêmio tem dono.",
  instagram: "https://www.instagram.com/clovis.obilhete/",
  reelAtual: "https://www.instagram.com/clovis.obilhete/",  // trocar pelo link do Reel da votação aberta
  tiktok: "", youtube: "",
  linkPagamento: "",  // Link de pagamento do Mercado Pago (R$ 9,90, Pix). Vazio = botão mostra "em breve".
  precoPasse: "R$ 9,90",
  vagasPorParte: 10,
  horaParte: 19,
  horaFechaVoto: 15,

  heroKicker: "Série interativa no Instagram",
  heroTitulo: "Ele achou R$ 40 milhões no banco de trás.",
  heroDestaque: "Você decide.",
  heroTexto: "Uma da manhã. O Clóvis, taxista há 22 anos, achou um bilhete premiado no táxi. Todo dia sai uma parte, e os comentários escrevem a próxima.",

  painel: [
    { rotulo: "No banco de trás", valor: "R$ 40 mi" },
    { rotulo: "No bolso", valor: "R$ 0" },
    { rotulo: "Risco", valor: "85%", barra: 85, alerta: true },
  ],

  votacao: {
    parte: 1,
    titulo: "Acelera ou espera?",
    chamada: "Daqui pra frente, você decide.",
    opcoes: ["ACELERA", "ESPERA"],
    dica: "Tem um 3º jeito escondido no banco de trás. Só vale se você disser qual é.",
  },

  partes: [
    { n: 1, titulo: "Todo prêmio tem dono", capa: "assets/capas/parte1.jpg", decisao: null, link: "" },
  ],
  mural: [
    { capa: "assets/capas/susto.jpg", legenda: "O SUSTO" },
    { capa: "assets/capas/verso.jpg", legenda: "SEU ANTÔNIO" },
    { capa: "assets/capas/hotel.jpg", legenda: "PARTE 1 · NO AR", principal: true },
    { capa: "assets/capas/homem.jpg", legenda: "QUEM É ELE?" },
    { capa: "assets/capas/banco.jpg", legenda: "BANCO DE TRÁS" },
  ],
  etiquetas: ["RISCO 85%", "R$ 40 MI NO BANCO"],

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
