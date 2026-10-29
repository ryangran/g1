// Tudo que muda de série para série fica aqui. O index.html só lê este objeto.
// Ao lançar a série definitiva: troque os textos, as capas (assets/capas/) e os links.
window.SERIE = {
  marca: "3º JEITO",
  instagram: "https://www.instagram.com/",      // link do perfil
  reelAtual: "https://www.instagram.com/",      // link do Reel com a votação aberta
  tiktok: "", youtube: "",
  linkPagamento: "",  // link de pagamento (ex.: Mercado Pago "Link de pagamento" de R$ 9,90). Vazio = botão mostra "em breve".
  precoPasse: "R$ 9,90",
  vagasPorParte: 10,
  horaParte: 19,      // hora de Brasília em que sai cada parte
  horaFechaVoto: 15,  // hora de Brasília em que fecha a votação

  heroKicker: "Série interativa no Instagram",
  heroTitulo: "Você é um macaco.",
  heroDestaque: "Você decide.",
  heroTexto: "A maior banana da selva está do outro lado do rio. E o rio tem crocodilo. Todo dia sai uma parte, e os comentários escrevem a próxima.",

  // painel de jogo (o mesmo do vídeo)
  painel: [
    { rotulo: "Bananas", valor: "0" },
    { rotulo: "Energia", valor: "72%" },
    { rotulo: "Perigo", valor: "90%", barra: 90, alerta: true },
  ],

  // votação aberta (a parte atual)
  votacao: {
    parte: 1,
    titulo: "Cipó ou pedra?",
    chamada: "Daqui pra frente, você decide.",
    opcoes: ["CIPÓ", "PEDRA"],
    dica: "Tem um 3º jeito escondido na imagem. Só vale se você disser qual é.",
  },

  // arquivo do caso: uma entrada por parte, a mais nova por último
  partes: [
    { n: 1, titulo: "O rio", capa: "assets/capas/macaco-1.jpg", decisao: null, link: "" },
  ],
  // capas extras do mural (cenas da parte atual)
  mural: [
    { capa: "assets/capas/macaco-9.8.jpg", legenda: "O SUSTO" },
    { capa: "assets/capas/macaco-12.9.jpg", legenda: "RACHANDO" },
    { capa: "assets/capas/macaco-22.5.jpg", legenda: "PARTE 1 · NO AR", principal: true },
    { capa: "assets/capas/macaco-17.6.jpg", legenda: "UMA PISCOU" },
    { capa: "assets/capas/macaco-1.jpg", legenda: "VOCÊ" },
  ],
  etiquetas: ["PERIGO 90%", "BANANAS: 0"],

  // agentes reais (preencha conforme os pagamentos confirmados). Vazio = mostra vagas livres.
  agentes: [],   // ex.: { arroba: "@fulano", numero: 1, partes: 3, titulo: "O ESPERTO" }
  // números reais do perfil. Vazio = a seção some (nunca invente números).
  numeros: [],   // ex.: { valor: "120 mil", rotulo: "Visualizações" }
};
