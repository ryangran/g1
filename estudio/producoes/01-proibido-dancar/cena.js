/*
 * PROIBIDO DANÇAR — episódio 01
 * Fábrica de robôs onde é proibido dançar. Bolt (laranja) não aguenta o ritmo.
 * Tudo é função do tempo t; a atuação e a câmera estão em ATUACAO e PLANOS.
 */
(function () {
  const THREE = window.THREE;
  const E = window.Estudio3D;
  const DUR = 38.5;
  const BEAT = 60 / 144; // a dança do modelo dura 8 batidas a 144 BPM
  const W = 1080, H = 1920;

  const tl = window.__timelines["main"]; // registrada no index.html

  // ---------- renderer, cena, câmera ----------
  const canvas = document.getElementById("palco");
  const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, preserveDrawingBuffer: true });
  renderer.setPixelRatio(1);
  renderer.setSize(W, H, false);
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.15;
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;

  const cena = new THREE.Scene();
  cena.background = new THREE.Color("#0c0f15");
  cena.fog = new THREE.Fog("#0c0f15", 7, 17);
  const camera = new THREE.PerspectiveCamera(40, W / H, 0.05, 60);
  const preenchimento = new THREE.PointLight("#ffd9b0", 2.2, 5, 1.5); // fill suave que acompanha a câmera
  preenchimento.position.set(0.3, 0.2, 0); camera.add(preenchimento); cena.add(camera);

  // ---------- cenário: galpão da fábrica ----------
  function texturaPiso() {
    const c = document.createElement("canvas"); c.width = c.height = 1024;
    const g = c.getContext("2d");
    g.fillStyle = "#2a2d33"; g.fillRect(0, 0, 1024, 1024);
    const r = E.aleatorio(7);
    for (let i = 0; i < 2500; i++) { // manchas de concreto
      g.fillStyle = `rgba(${r() > 0.5 ? 255 : 0},${r() > 0.5 ? 255 : 0},${r() > 0.5 ? 255 : 0},0.025)`;
      g.fillRect(r() * 1024, r() * 1024, 2 + r() * 14, 2 + r() * 14);
    }
    g.strokeStyle = "rgba(0,0,0,0.45)"; g.lineWidth = 4;
    for (let i = 0; i <= 1024; i += 128) { g.beginPath(); g.moveTo(i, 0); g.lineTo(i, 1024); g.stroke(); g.beginPath(); g.moveTo(0, i); g.lineTo(1024, i); g.stroke(); }
    const t = new THREE.CanvasTexture(c);
    t.wrapS = t.wrapT = THREE.RepeatWrapping; t.repeat.set(6, 6); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 8;
    return t;
  }
  function texturaParede() {
    const c = document.createElement("canvas"); c.width = 1024; c.height = 512;
    const g = c.getContext("2d");
    g.fillStyle = "#353a42"; g.fillRect(0, 0, 1024, 512);
    for (let x = 0; x < 1024; x += 64) { g.fillStyle = x % 128 ? "#31363d" : "#3a3f47"; g.fillRect(x, 0, 60, 512); }
    g.fillStyle = "rgba(0,0,0,0.35)";
    for (let x = 0; x < 1024; x += 64) g.fillRect(x + 60, 0, 4, 512);
    const t = new THREE.CanvasTexture(c);
    t.wrapS = THREE.RepeatWrapping; t.repeat.set(3, 1); t.colorSpace = THREE.SRGBColorSpace;
    return t;
  }

  const piso = new THREE.Mesh(new THREE.PlaneGeometry(30, 30), new THREE.MeshStandardMaterial({ map: texturaPiso(), roughness: 0.85 }));
  piso.rotation.x = -Math.PI / 2; piso.receiveShadow = true; cena.add(piso);

  // faixa de segurança amarela/preta à frente das fileiras
  (function faixa() {
    const c = document.createElement("canvas"); c.width = 512; c.height = 32;
    const g = c.getContext("2d");
    for (let i = -32; i < 512; i += 32) { g.fillStyle = (i / 32) % 2 ? "#e0b21c" : "#151515"; g.beginPath(); g.moveTo(i, 32); g.lineTo(i + 16, 0); g.lineTo(i + 32, 0); g.lineTo(i + 16, 32); g.fill(); }
    const tex = new THREE.CanvasTexture(c); tex.wrapS = THREE.RepeatWrapping; tex.repeat.set(4, 1); tex.colorSpace = THREE.SRGBColorSpace;
    const m = new THREE.Mesh(new THREE.PlaneGeometry(7, 0.16), new THREE.MeshStandardMaterial({ map: tex, roughness: 0.7 }));
    m.rotation.x = -Math.PI / 2; m.position.set(0, 0.003, 0.62); m.receiveShadow = true; cena.add(m);
  })();

  const matParede = new THREE.MeshStandardMaterial({ map: texturaParede(), roughness: 0.8 });
  const paredeFundo = new THREE.Mesh(new THREE.PlaneGeometry(14, 7), matParede);
  paredeFundo.position.set(0, 3.5, -4.6); paredeFundo.receiveShadow = true; cena.add(paredeFundo);
  for (const s of [-1, 1]) {
    const p = new THREE.Mesh(new THREE.PlaneGeometry(14, 7), matParede);
    p.position.set(5.2 * s, 3.5, 1.5); p.rotation.y = -s * Math.PI / 2; p.receiveShadow = true; cena.add(p);
  }
  // canos horizontais e colunas
  const matCano = new THREE.MeshStandardMaterial({ color: "#4f5660", roughness: 0.4, metalness: 0.6 });
  for (const [y, r] of [[4.85, 0.09], [5.1, 0.06], [0.55, 0.05]]) {
    const cano = new THREE.Mesh(new THREE.CylinderGeometry(r, r, 12, 16), matCano);
    cano.rotation.z = Math.PI / 2; cano.position.set(0, y, -4.45); cano.castShadow = true; cena.add(cano);
  }
  for (const x of [-3.6, 3.6]) {
    const col = new THREE.Mesh(new THREE.BoxGeometry(0.4, 7, 0.4), new THREE.MeshStandardMaterial({ color: "#3d434c", roughness: 0.6, metalness: 0.3 }));
    col.position.set(x, 3.5, -4.35); col.castShadow = true; cena.add(col);
  }

  // ---------- placas (texto no mundo) ----------
  const placaTex = E.texturaTexto([], { largura: 1024, altura: 640 });
  const placa = new THREE.Mesh(new THREE.PlaneGeometry(3.2, 2.0), new THREE.MeshStandardMaterial({ map: placaTex, roughness: 0.6 }));
  placa.position.set(0, 2.62, -4.52); cena.add(placa);
  // tábua que cobre a palavra escondida (o "plant" da reviravolta)
  const tabua = new THREE.Group();
  const tabuaMesh = new THREE.Mesh(new THREE.BoxGeometry(2.75, 0.6, 0.05), new THREE.MeshStandardMaterial({ color: "#6b5a43", roughness: 0.9 }));
  tabuaMesh.position.y = -0.3; tabuaMesh.castShadow = true;
  tabua.add(tabuaMesh);
  for (const x of [-1.2, 1.2]) { // parafusos
    const p = new THREE.Mesh(new THREE.CylinderGeometry(0.035, 0.035, 0.02, 12), new THREE.MeshStandardMaterial({ color: "#aaa", metalness: 0.8, roughness: 0.3 }));
    p.rotation.x = Math.PI / 2; p.position.set(x, -0.08, 0.035); tabua.add(p);
  }
  tabua.position.set(0, 2.38, -4.47); cena.add(tabua);

  // letreiro neon (desligado até o final)
  const neonTex = E.texturaTexto([], { largura: 1024, altura: 256 });
  const neonMat = new THREE.MeshBasicMaterial({ map: neonTex, transparent: true });
  const neon = new THREE.Mesh(new THREE.PlaneGeometry(2.9, 0.72), neonMat);
  neon.position.set(0, 4.22, -4.5); cena.add(neon);
  const neonLuz = new THREE.PointLight("#ff2a8a", 0, 4, 2); neonLuz.position.set(0, 4.2, -4.0); cena.add(neonLuz);

  function desenharPlacas() {
    placaTex.desenhar(
      [
        { texto: "PROIBIDO", tamanho: 150, cor: "#ffd23f", dy: -10 },
        { texto: "DANÇAR", tamanho: 220, cor: "#ffffff", dy: -48 },
        { texto: "MAL", tamanho: 170, cor: "#ffe14a", dy: 18 },
      ],
      { fundo: "#c21f1f", borda: "#ffffff", bordaLargura: 22, fonte: "Bangers" },
    );
  }
  function desenharNeon(aceso) {
    neonTex.desenhar(
      [{ texto: "PROIBIDO PARAR", tamanho: 150, cor: aceso ? "#ffd0ec" : "rgba(40,30,36,0.10)", brilho: aceso ? 40 : 0 }],
      { fundo: aceso ? "rgba(255,40,140,0.10)" : "rgba(0,0,0,0)", fonte: "Bangers" },
    );
  }

  // ---------- luzes ----------
  cena.add(new THREE.HemisphereLight("#8fa8d8", "#1a1410", 0.75));
  const chave = new THREE.SpotLight("#ffe2b8", 60, 14, 0.62, 0.55, 1.6);
  chave.position.set(1.6, 5.2, 3.2); chave.target.position.set(0.3, 0, -0.6);
  chave.castShadow = true; chave.shadow.mapSize.set(1024, 1024); chave.shadow.bias = -0.0004; chave.shadow.radius = 4;
  cena.add(chave, chave.target);
  const contra = new THREE.DirectionalLight("#6fa0ff", 1.4); contra.position.set(-3, 4, -6); cena.add(contra);
  const placaLuz = new THREE.SpotLight("#fff1d6", 25, 7, 0.5, 0.6, 1.5);
  placaLuz.position.set(0, 5.4, -2.2); placaLuz.target.position.set(0, 3.0, -4.6); cena.add(placaLuz, placaLuz.target);
  // giroflex vermelho (alarme) ao lado da placa
  const giroBase = new THREE.Mesh(new THREE.CylinderGeometry(0.1, 0.12, 0.16, 16), new THREE.MeshStandardMaterial({ color: "#ff2020", emissive: "#ff1010", emissiveIntensity: 0.4 }));
  giroBase.position.set(1.95, 3.75, -4.4); cena.add(giroBase);
  const giro = new THREE.SpotLight("#ff2a2a", 0, 12, 0.5, 0.5, 1.2);
  giro.position.copy(giroBase.position); cena.add(giro, giro.target);
  // luzes de festa (só no final)
  const focoBolt = new THREE.SpotLight("#ffb46b", 0, 6, 0.32, 0.5, 1.4);
  focoBolt.position.set(0.9, 3.6, 1.6); focoBolt.target.position.set(0.55, 0.3, 0); cena.add(focoBolt, focoBolt.target);
  const festa = [0, 1, 2].map((i) => {
    const l = new THREE.SpotLight("#ffffff", 0, 14, 0.45, 0.6, 1.2);
    l.position.set(-3 + i * 3, 4.6, 2.5); cena.add(l, l.target); return l;
  });

  // ---------- personagens ----------
  const COR_OPERARIO = { Main: "#5c6878", Grey: "#3b4048", Black: "#111317" };
  const COR_BOLT = { Main: "#ff7a1a", Grey: "#5a5e66", Black: "#0f0f12" };
  const COR_CHEFE = { Main: "#8e1b1b", Grey: "#26282d", Black: "#0a0a0c" };

  // fileiras: 3 x 4. Bolt na fileira da frente, segundo da direita
  const POS_BOLT = [0.55, 0, 0];
  const lugares = [];
  for (let fila = 0; fila < 3; fila++) for (let c = 0; c < 4; c++) lugares.push([-1.65 + c * 1.1, 0, -fila * 1.4]);

  let bolt, chefe; const operarios = [];
  let pronto = false;

  function tempoBatida(t) { return (t / BEAT) % 1; }

  function montarAtuacao() {
    // ----- BOLT -----
    bolt.atuar([
      { t0: -1, clip: "Idle", vel: 0.35 },
      { t0: 6.25, clip: "Dance", vel: 1, offset: 0, fade: 0.2 },
      { t0: 7.55, clip: "Idle", vel: 0.35, fade: 0.12 },
      { t0: 12.083, clip: "Dance", vel: 1, offset: 0.833, fade: 0.25 },
      { t0: 19.25, clip: "Idle", vel: 0.3, fade: 0.15 },
      { t0: 31.9, clip: "Dance", vel: 1.08, offset: 1.3, fade: 0.3 }, // fora do ritmo de propósito
      { t0: 35.0, clip: "Sitting", vel: 0.9, loop: false, fade: 0.4 },
    ]);
    bolt.mover([[0, POS_BOLT]], [[0, 0]]);
    bolt.rostoChaves([
      [0, { Angry: 0, Surprised: 0, Sad: 0 }],
      [2.9, { Surprised: 0 }], [3.15, { Surprised: 0.8 }, "out"], [4.6, { Surprised: 0.8 }], [5.0, { Surprised: 0 }],
      [7.45, { Surprised: 0 }], [7.6, { Surprised: 1 }, "out"], [8.6, { Surprised: 0 }],
      [19.1, { Surprised: 0 }], [19.3, { Surprised: 1 }, "out"], [23.9, { Surprised: 1, Sad: 0 }], [24.6, { Surprised: 0.2, Sad: 1 }],
      [28.8, { Surprised: 0.2, Sad: 1 }], [29.6, { Surprised: 1, Sad: 0 }, "out"], [31.6, { Surprised: 0, Sad: 0 }],
      [35.2, { Sad: 0 }], [35.9, { Sad: 0.9 }], [36.4, { Sad: 0.2, Surprised: 1 }, "out"], [37.4, { Sad: 1, Surprised: 0.3 }],
    ]);
    const balanco = E.trilha([[0, 1], [2.85, 1], [3.0, 0, "out"], [5.3, 0], [5.6, 0.6], [6.1, 0.6], [6.2, 0], [9.5, 0], [10.0, 0.5], [12.0, 0.5], [12.1, 0]]);
    const cabecaBaixa = E.trilha([[0, 0], [24.0, 0], [24.6, 0.35, "out"], [28.9, 0.35], [29.4, -0.25, "out"], [31.4, 0], [36.2, 0], [36.6, -0.45, "out"]]);
    const encolher = E.trilha([[0, 1], [23.9, 1], [24.3, 0.9, "out"], [29.3, 0.9], [29.6, 1, "back"]]);
    bolt.ajustes = (t, p) => {
      const b = balanco(t);
      if (b) {
        const s = Math.sin(tempoBatida(t) * Math.PI * 2);
        p.girar("Head", 0.12 * b * Math.max(0, s), 0, 0.06 * b * s);
        p.girar("Abdomen", 0, 0, 0.03 * b * s);
      }
      p.girar("Head", cabecaBaixa(t), 0, 0);
      p.root.scale.set(p.escala, p.escala * encolher(t), p.escala);
    };

    // ----- CHEFE -----
    const RY_DIR = Math.PI / 2, RY_ESQ = -Math.PI / 2, RY_FUNDO = Math.PI;
    chefe.atuar([
      { t0: -1, clip: "Walking", vel: 0.9 },
      { t0: 7.0, clip: "Idle", vel: 0.6, fade: 0.3 },
      { t0: 11.3, clip: "Walking", vel: 0.9, fade: 0.3 },
      { t0: 15.6, clip: "Idle", vel: 0.6 },
      { t0: 17.4, clip: "Walking", vel: 0.9, fade: 0.2 },
      { t0: 18.75, clip: "Idle", vel: 0.6, fade: 0.2 },
      { t0: 19.8, clip: "Walking", vel: 0.62, fade: 0.25 },
      { t0: 23.35, clip: "Idle", vel: 0.5, fade: 0.25 },
      { t0: 26.3, clip: "No", vel: 1, loop: false, fade: 0.2 },
      { t0: 27.75, clip: "Punch", vel: 1, offset: 0, loop: false, fade: 0.15 },
      { t0: 28.05, clip: "Punch", vel: 0, offset: 0.33, loop: false, fade: 0.1 }, // braço esticado apontando
      { t0: 29.0, clip: "Idle", vel: 0.6, fade: 0.4 },
      { t0: 31.25, clip: "Dance", vel: 1, offset: 0, fade: 0.25 },
    ]);
    chefe.mover(
      [
        [0, [-3.4, 0, 1.35]], [7.0, [3.3, 0, 1.35], "linear"],
        [11.4, [3.3, 0, 1.35]], [15.6, [7.5, 0, 1.35], "linear"],
        [17.4, [5.0, 0, 1.35]], [18.75, [3.1, 0, 1.35], "out"],
        [19.9, [3.1, 0, 1.35]], [23.35, [0.62, 0, 0.95], "out"],
        [30.9, [0.62, 0, 0.95]], [30.95, [-0.45, 0, 1.6]], // reposiciona durante o close da placa
      ],
      [
        // olhar para as fileiras = virar para -z (π); andar até o Bolt = atan2(dx, dz) do trajeto
        [0, RY_DIR], [7.2, RY_DIR], [7.7, RY_FUNDO - 0.35, "out"], [10.0, RY_FUNDO - 0.35], [10.4, RY_FUNDO + 0.3], [11.0, RY_FUNDO + 0.3], [11.4, RY_DIR],
        [17.3, RY_DIR], [17.4, RY_ESQ], [19.5, RY_ESQ], [20.1, -1.78], [22.9, -1.78], [23.5, -3.07], [30.9, -3.07], [30.95, 0],
      ],
    );
    chefe.rostoChaves([
      [0, { Angry: 0.55 }], [7.6, { Angry: 0.55 }], [8.0, { Angry: 0.9 }], [11.0, { Angry: 0.6 }],
      [18.7, { Angry: 0.6, Surprised: 0 }], [18.85, { Angry: 0, Surprised: 1 }, "out"], [19.7, { Angry: 0, Surprised: 1 }], [20.1, { Angry: 1, Surprised: 0 }],
      [29.3, { Angry: 1 }], [29.9, { Angry: 0, Surprised: 0 }], [31.0, { Angry: 0 }],
    ]);
    const varredura = E.trilha([[0, 0], [8.0, 0], [8.8, 0.45], [9.8, -0.45], [10.6, 0.15], [11.2, 0]]);
    const inclinar = E.trilha([[0, 0], [23.0, 0], [23.6, 0.28, "out"], [26.2, 0.28], [26.5, 0]]);
    chefe.ajustes = (t, p) => {
      p.girar("Head", 0, varredura(t), 0);
      p.girar("Torso", inclinar(t), 0, 0);
    };

    // ----- OPERÁRIOS -----
    const viraPara = [ // vizinhos olham para o Bolt
      { idx: 1, ang: -0.7, t: 12.7 }, { idx: 3, ang: 0.7, t: 13.0 }, { idx: 6, ang: -0.35, t: 13.4 },
    ];
    operarios.forEach((op, i) => {
      const r = E.aleatorio(100 + i);
      const fila = Math.floor(op.lugar / 4);
      op.p.atuar([
        { t0: -1, clip: "Idle", vel: 0.18, offset: r() * 3 },
        { t0: 31.25 + fila * BEAT, clip: "Dance", vel: 1, offset: 0, fade: 0.25 }, // uma fileira por batida
      ]);
      op.p.mover([[0, lugares[op.lugar]]], [[0, (r() - 0.5) * 0.08]]);
      const v = viraPara.find((x) => x.idx === op.lugar);
      const olhar = v ? E.trilha([[0, 0], [v.t, 0], [v.t + 0.35, v.ang, "out"], [18.6, v.ang], [18.9, 0, "out"]]) : () => 0;
      op.p.rostoChaves([[0, { Surprised: 0 }], [31.5, { Surprised: 0 }], [32.0, { Surprised: 0.0 }]]);
      op.p.ajustes = (t, p) => p.girar("Head", 0, olhar(t), 0);
    });
  }

  // ---------- câmera ----------
  const PLANOS = [
    // 1 gancho: close no Bolt balançando a cabeça; placa ao fundo
    { t0: 0.0, de: { pos: [0.95, 0.6, 2.1], alvo: [0.5, 1.15, -1.8], fov: 46 }, para: { pos: [0.85, 0.62, 1.8], alvo: [0.5, 1.15, -1.8], fov: 44 }, ease: "linear" },
    // 2 geral alta: chefe patrulha na frente das fileiras
    { t0: 2.4, de: { pos: [3.6, 3.3, 5.0], alvo: [0, 0.6, -1.0], fov: 46 }, para: { pos: [3.0, 3.0, 4.6], alvo: [0.3, 0.6, -1.0], fov: 46 }, ease: "linear" },
    // 3 chefe de costas, Bolt dança escondido ao fundo
    { t0: 5.6, de: { pos: [4.4, 1.25, 3.4], alvo: [1.2, 0.75, 0.0], fov: 40 }, para: { pos: [4.2, 1.2, 3.1], alvo: [1.0, 0.7, 0.0], fov: 40 } },
    // 4 close no chefe desconfiado
    { t0: 9.0, de: { pos: [2.55, 1.05, -1.1], alvo: [3.3, 1.15, 1.35], fov: 40 }, para: { pos: [2.65, 1.05, -0.85], alvo: [3.3, 1.15, 1.35], fov: 38 } },
    // 5 Bolt dança de novo; vizinhos percebem
    { t0: 11.6, de: { pos: [0.55, 0.95, 2.6], alvo: [0.45, 0.65, -0.6], fov: 46 }, para: { pos: [0.55, 0.9, 2.2], alvo: [0.45, 0.62, -0.6], fov: 44 } },
    // 6 arco em volta do Bolt dançando solto
    { t0: 15.0, de: { pos: [2.0, 0.75, 1.7], alvo: [0.55, 0.55, 0], fov: 42 }, para: { pos: [-0.9, 0.85, 1.75], alvo: [0.55, 0.55, 0], fov: 42 }, ease: "inOut" },
    // 7 o chefe volta e vê
    { t0: 18.2, de: { pos: [1.0, 1.0, 4.2], alvo: [3.2, 1.0, 1.35], fov: 40 }, para: { pos: [1.4, 1.05, 3.7], alvo: [3.1, 1.1, 1.35], fov: 36 }, ease: "out" },
    // 8 contra-plongée: o chefe vem na direção do Bolt
    { t0: 19.6, de: { pos: [-0.4, 0.28, 1.35], alvo: [2.6, 1.15, 1.3], fov: 52 }, para: { pos: [-0.32, 0.3, 1.3], alvo: [0.62, 1.15, 0.95], fov: 52 }, tremor: 0.004 },
    // 9 perfil: nariz com nariz
    { t0: 23.6, de: { pos: [1.85, 1.15, 1.75], alvo: [0.5, 0.7, 0], fov: 40 }, para: { pos: [1.75, 1.1, 1.6], alvo: [0.5, 0.66, 0], fov: 38 }, ease: "linear" },
    // 10 o chefe nega com a cabeça e aponta a placa
    { t0: 26.2, de: { pos: [1.75, 0.62, 2.75], alvo: [0.25, 1.85, -3.2], fov: 56 }, para: { pos: [1.65, 0.62, 2.6], alvo: [0.2, 1.95, -3.2], fov: 56 } },
    // 11 inserto: a tábua cai e revela "MAL"
    { t0: 28.8, de: { pos: [0.05, 2.5, 1.6], alvo: [0, 2.55, -4.5], fov: 40 }, para: { pos: [0.03, 2.5, 1.2], alvo: [0, 2.5, -4.5], fov: 40 }, ease: "linear" },
    // 12 geral frontal: todo mundo dança, Bolt fora do ritmo
    { t0: 31.0, de: { pos: [0.3, 2.3, 6.2], alvo: [0.1, 0.9, -1.0], fov: 46 }, para: { pos: [0.4, 1.6, 4.9], alvo: [0.2, 0.85, -1.0], fov: 46 }, ease: "out" },
    // 13 Bolt exausto senta; o neon "PROIBIDO PARAR" acende
    { t0: 35.0, de: { pos: [1.05, 0.3, 2.65], alvo: [0.45, 1.6, -4.0], fov: 50 }, para: { pos: [1.0, 0.3, 2.4], alvo: [0.42, 1.75, -4.0], fov: 50 }, ease: "linear" },
  ];
  const cam = E.diretorDeCamera(camera, PLANOS, DUR);

  // ---------- luz e objetos por tempo ----------
  const tabuaQueda = E.trilha([[0, 0], [29.4, 0], [29.9, 1, "in"]]);
  const giroOn = E.trilha([[0, 0], [19.4, 0], [19.6, 1], [30.8, 1], [31.0, 0]]);
  const festaOn = E.trilha([[0, 0], [31.0, 0], [31.4, 1], [38.5, 1]]);
  const chaveInt = E.trilha([[0, 60], [19.4, 60], [19.8, 34], [30.9, 34], [31.2, 55]]);
  let neonAceso = null;

  function renderAt(t) {
    if (!pronto) return;
    t = E.clamp(t, 0, DUR - 1e-3);
    bolt.aplicar(t); chefe.aplicar(t);
    for (const op of operarios) op.p.aplicar(t);

    // tábua cai girando para frente
    const q = tabuaQueda(t);
    tabua.rotation.x = q * 1.9;
    tabua.position.y = 2.38 - q * q * 2.3;
    tabua.position.z = -4.47 + q * 0.5;
    tabua.visible = q < 0.999;

    const g = giroOn(t);
    giro.intensity = g * 70;
    const a = t * 5.2;
    giro.target.position.set(giroBase.position.x + Math.cos(a) * 4, 0.5, giroBase.position.z + 3 + Math.sin(a) * 3);
    giroBase.material.emissiveIntensity = 0.4 + g * 2.2 * (0.5 + 0.5 * Math.cos(a));
    chave.intensity = chaveInt(t);
    focoBolt.intensity = E.trilha([[0, 0], [35.0, 0], [35.6, 38]])(t);

    const f = festaOn(t);
    const cores = ["#ff3d8b", "#3dd6ff", "#ffd23f"];
    festa.forEach((l, i) => {
      const fase = Math.floor(t / (BEAT * 2) + i) % 3;
      l.color.set(cores[fase]);
      l.intensity = f * 45 * (0.65 + 0.35 * Math.cos((t / BEAT) * Math.PI * 2 + i));
      l.target.position.set(-2 + i * 2 + Math.sin(t * 1.7 + i) * 1.2, 0, -1 + Math.cos(t * 1.3 + i));
    });

    // neon pisca e acende
    const pisca = t >= 36.2 && (t < 36.35 || (t >= 36.5 && t < 36.6) || t >= 36.75);
    if (pisca !== neonAceso) { desenharNeon(pisca); neonAceso = pisca; }
    neonLuz.intensity = pisca ? 6 : 0;

    cam(t);
    renderer.render(cena, camera);
  }

  window.addEventListener("hf-seek", (e) => renderAt(e.detail.time));

  window.__hf = window.__hf || {};
  window.__hf.buildReady = window.__hf.buildReady || {};
  window.__hf.buildReady["proibido-dancar"] = Promise.all([
    E.carregarGLTF("assets/modelos/RobotExpressive.glb"),
    E.carregarFonte("Bangers", "assets/fontes/Bangers.woff2"),
  ]).then(([gltf]) => {
    // normaliza: operário com 1 unidade de altura
    const caixa = new THREE.Box3().setFromObject(gltf.scene);
    const base = 1 / (caixa.max.y - caixa.min.y);
    bolt = E.criarPersonagem(gltf, { cores: COR_BOLT, escala: base });
    chefe = E.criarPersonagem(gltf, { cores: COR_CHEFE, escala: base * 1.45, emissivo: { Black: ["#ff2a1a", 0.0] } });
    cena.add(bolt.root, chefe.root);
    lugares.forEach((pos, i) => {
      if (pos[0] === POS_BOLT[0] && pos[2] === POS_BOLT[2]) return;
      const p = E.criarPersonagem(gltf, { cores: COR_OPERARIO, escala: base });
      cena.add(p.root); operarios.push({ p, lugar: i });
    });
    montarAtuacao();
    desenharPlacas(); desenharNeon(false); neonAceso = false;
    pronto = true;
    renderer.compile(cena, camera);
    for (const x of [0, 20, 32, 0]) renderAt(x);
    renderAt(tl.time());
    renderer.getContext().finish();
  });
})();
