/*
 * APAGÃO — Lumi só quer apagar a luz. 26 s, 1080x1920.
 * Cenários: quarto (cm), apartamento (cm), prédio (m), cidade (m), céu, escuro (= quarto sem luz).
 * Cada quadro é função de t: escolhe o plano, posiciona câmera, personagem e luzes.
 */
(function () {
  const THREE = window.THREE, E = window.Estudio3D;
  const W = 1080, H = 1920, DUR = 26.0;
  const tr = E.trilha, cl = E.clamp, ease = E.ease;
  const sm = (a, b, t) => { const x = cl((t - a) / (b - a), 0, 1); return x * x * (3 - 2 * x); };
  const R = new THREE.WebGLRenderer({ canvas: document.getElementById("palco"), antialias: true, preserveDrawingBuffer: true });
  R.setPixelRatio(1); R.setSize(W, H, false);
  R.outputColorSpace = THREE.SRGBColorSpace; R.toneMapping = THREE.ACESFilmicToneMapping; R.toneMappingExposure = 1.1;
  R.shadowMap.enabled = true; R.shadowMap.type = THREE.PCFSoftShadowMap;
  const cam = new THREE.PerspectiveCamera(40, W / H, 0.05, 20000);
  const fill = new THREE.PointLight("#ffd8b0", 0, 12, 1.6); fill.position.set(0.4, 0.3, 0); cam.add(fill);
  const V = (x, y, z) => new THREE.Vector3(x, y, z);
  const rnd = E.aleatorio(26);

  function canvasTex(w, h, desenho, rep) {
    const c = document.createElement("canvas"); c.width = w; c.height = h; desenho(c.getContext("2d"), w, h);
    const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 8;
    if (rep) { t.wrapS = t.wrapT = THREE.RepeatWrapping; t.repeat.set(rep[0], rep[1]); }
    return t;
  }
  const std = (c, r = 0.6, ex = {}) => new THREE.MeshStandardMaterial({ color: c, roughness: r, ...ex });
  const caixa = (w, h, d, m) => new THREE.Mesh(new THREE.BoxGeometry(w, h, d), m);
  function faisca(cor = "#9fe7ff", tam = 1) {
    const t = canvasTex(128, 128, (g) => { const gr = g.createRadialGradient(64, 64, 0, 64, 64, 64); gr.addColorStop(0, "#fff"); gr.addColorStop(0.25, cor); gr.addColorStop(1, "rgba(0,0,0,0)"); g.fillStyle = gr; g.fillRect(0, 0, 128, 128); });
    const s = new THREE.Sprite(new THREE.SpriteMaterial({ map: t, blending: THREE.AdditiveBlending, depthWrite: false, transparent: true }));
    s.scale.setScalar(tam); return s;
  }

  // ======================= QUARTO (cm) =======================
  const Q = new THREE.Scene(); Q.background = new THREE.Color("#0b1022"); Q.fog = new THREE.Fog("#0b1022", 40, 140);
  const madeira = canvasTex(512, 512, (g, w, h) => {
    g.fillStyle = "#3a2418"; g.fillRect(0, 0, w, h);
    for (let i = 0; i < 70; i++) { g.strokeStyle = `rgba(${20 + rnd() * 40},${10 + rnd() * 20},5,${0.25 + rnd() * 0.3})`; g.lineWidth = 1 + rnd() * 4; g.beginPath(); const y = rnd() * h; g.moveTo(0, y); g.bezierCurveTo(w * 0.3, y + rnd() * 20 - 10, w * 0.6, y + rnd() * 20 - 10, w, y + rnd() * 10 - 5); g.stroke(); }
  }, [3, 2]);
  const mesa = caixa(90, 3, 50, new THREE.MeshPhysicalMaterial({ map: madeira, roughness: 0.35, clearcoat: 0.7 })); mesa.position.set(0, -1.5, -8); mesa.receiveShadow = true; Q.add(mesa);
  const parede = new THREE.Mesh(new THREE.PlaneGeometry(200, 120), std("#2a2f44", 0.9)); parede.position.set(0, 40, -34); Q.add(parede);
  const janela = new THREE.Mesh(new THREE.PlaneGeometry(30, 40), new THREE.MeshBasicMaterial({ color: "#3d5aa8" })); janela.position.set(40, 45, -33.8); Q.add(janela);
  // luzes do quarto
  const qAmb = new THREE.HemisphereLight("#7d8fd0", "#20140c", 0.35); Q.add(qAmb);
  const lua = new THREE.DirectionalLight("#8aa4ff", 0.9); lua.position.set(40, 40, 10); Q.add(lua);

  // caixa de fósforos (cama) — comprimento em x
  const cama = new THREE.Group(); Q.add(cama);
  const rotulo = canvasTex(256, 64, (g) => { g.fillStyle = "#c62a24"; g.fillRect(0, 0, 256, 64); g.fillStyle = "#ffd34d"; g.font = "bold 34px sans-serif"; g.textAlign = "center"; g.fillText("FÓSFOROS", 128, 44); });
  const papelao = std("#d9c7a0", 0.9);
  const fundo = caixa(5, 0.1, 3.2, papelao); fundo.position.y = 0.05; cama.add(fundo);
  for (const [w, d, x, z] of [[5, 0.1, 0, 1.55], [5, 0.1, 0, -1.55], [0.1, 3.2, 2.45, 0], [0.1, 3.2, -2.45, 0]]) {
    const m = caixa(w, 1.3, d, d < 0.2 ? new THREE.MeshStandardMaterial({ map: rotulo, roughness: 0.8 }) : papelao); m.position.set(x, 0.65, z); m.castShadow = m.receiveShadow = true; cama.add(m);
  }
  const listras = canvasTex(256, 256, (g) => { for (let i = 0; i < 8; i++) { g.fillStyle = i % 2 ? "#f4efe6" : "#d93a3a"; g.fillRect(0, i * 32, 256, 32); } });
  const meia = new THREE.Mesh(new THREE.RoundedBoxGeometry(3.4, 0.45, 2.7, 3, 0.2), new THREE.MeshStandardMaterial({ map: listras, roughness: 0.95, emissive: new THREE.Color("#e9ff7a"), emissiveIntensity: 0 }));
  meia.castShadow = meia.receiveShadow = true; Q.add(meia);
  const tampinha = new THREE.Mesh(new THREE.CylinderGeometry(0.85, 0.85, 0.35, 24), std("#b8b8c0", 0.25, { metalness: 0.9 })); tampinha.position.set(-1.7, 0.3, 0); Q.add(tampinha);

  // abajur: pivô na borda de trás da base (cai para longe da cama)
  const centroAbajur = V(-12, 0, -8);
  const dir = V(12, 0, 8).normalize(); // do abajur para a cama
  const pivo = new THREE.Group(); pivo.position.copy(centroAbajur).addScaledVector(dir, -6); pivo.rotation.y = Math.atan2(-dir.x, -dir.z); Q.add(pivo);
  const abajur = new THREE.Group(); abajur.position.set(0, 0, -6); pivo.add(abajur);
  const metal = std("#c9b27a", 0.3, { metalness: 0.85 });
  const base = new THREE.Mesh(new THREE.CylinderGeometry(6, 6.4, 2.4, 48), metal); base.position.y = 1.2; base.castShadow = base.receiveShadow = true; abajur.add(base);
  const haste = new THREE.Mesh(new THREE.CylinderGeometry(0.45, 0.45, 28, 16), metal); haste.position.y = 15; abajur.add(haste);
  const cupulaMat = new THREE.MeshStandardMaterial({ color: "#f1e3c4", roughness: 0.9, side: THREE.DoubleSide, emissive: new THREE.Color("#ffcf8a"), emissiveIntensity: 1.0 });
  const cupula = new THREE.Mesh(new THREE.CylinderGeometry(7, 11, 13, 48, 1, true), cupulaMat); cupula.position.y = 31; abajur.add(cupula);
  const lampada = new THREE.Mesh(new THREE.SphereGeometry(2, 20, 16), new THREE.MeshBasicMaterial({ color: "#fff3d6" })); lampada.position.y = 28; abajur.add(lampada);
  const luzAbajur = new THREE.PointLight("#ffd9a0", 2600, 140, 1.5); luzAbajur.position.y = 27;  abajur.add(luzAbajur);
  // botão na lateral da base, virado para a cama (no referencial do abajur a cama fica em -z)
  const botao = new THREE.Mesh(new THREE.CylinderGeometry(0.7, 0.7, 0.7, 24), std("#d8262a", 0.35)); botao.rotation.x = Math.PI / 2; botao.position.set(0, 1.1, -6.0 - 0.25); abajur.add(botao);
  // o abajur foi construído com a cama em +z local (pivô olha para -dir; filho em z=-6 → +z local aponta para a cama)
  // posição do botão no mundo (para o Lumi)
  Q.updateMatrixWorld(true);
  const botaoMundo = botao.getWorldPosition(V());

  // régua de tomadas + fio
  const regua = new THREE.Group(); regua.position.set(16, 0, -14); Q.add(regua);
  const corpoRegua = new THREE.Mesh(new THREE.RoundedBoxGeometry(15, 2, 4, 3, 0.4), std("#eeeeea", 0.4)); corpoRegua.position.y = 1; corpoRegua.castShadow = corpoRegua.receiveShadow = true; regua.add(corpoRegua);
  const led = new THREE.Mesh(new THREE.SphereGeometry(0.25, 12, 8), new THREE.MeshBasicMaterial({ color: "#ff3030" })); led.position.set(6.6, 2, 1.2); regua.add(led);
  const tomadas = [], faiscasRegua = [];
  for (let i = 0; i < 4; i++) {
    const x = -5 + i * 3.2;
    const fur = new THREE.Mesh(new THREE.CylinderGeometry(1.0, 1.0, 0.1, 20), std("#d5d5d0", 0.5)); fur.position.set(x, 2.02, 0); regua.add(fur);
    const plug = new THREE.Group(); plug.position.set(x, 2.0, 0); regua.add(plug);
    const pc = new THREE.Mesh(new THREE.RoundedBoxGeometry(1.6, 1.8, 1.6, 2, 0.3), std(i === 0 ? "#2b2b2b" : "#f2f2ee", 0.5)); pc.position.y = 0.9; pc.castShadow = true; plug.add(pc);
    tomadas.push(plug);
    const fz = faisca("#9fe7ff", 0.01); fz.position.set(x, 2.4, 0); regua.add(fz); faiscasRegua.push(fz);
    // fios saindo para trás
    if (i > 0) { const c = new THREE.CatmullRomCurve3([V(x, 3.5, 0), V(x, 4, -3), V(x + 2, 0.4, -9), V(x + 6, 0.4, -18)]); regua.add(new THREE.Mesh(new THREE.TubeGeometry(c, 30, 0.28, 8), std("#e8e8e4", 0.5))); }
  }
  const fioCurva = new THREE.CatmullRomCurve3([pivo.position.clone().add(V(0, 0.4, 0)), V(-2, 0.4, -16), V(8, 0.4, -18), V(11, 0.4, -12), V(11, 3.5, -14)]);
  Q.add(new THREE.Mesh(new THREE.TubeGeometry(fioCurva, 80, 0.3, 8), std("#2b2b2b", 0.5)));
  const faiscaFio = faisca("#9fe7ff", 0.01); Q.add(faiscaFio);
  const luzFaisca = new THREE.PointLight("#9fe7ff", 0, 25, 2); Q.add(luzFaisca);

  const lumi = window.criarLumi(THREE); Q.add(lumi.root); Q.add(cam);
  const sombraTex = canvasTex(128, 128, (g) => { const gr = g.createRadialGradient(64, 64, 0, 64, 64, 64); gr.addColorStop(0, "rgba(0,0,0,0.55)"); gr.addColorStop(1, "rgba(0,0,0,0)"); g.fillStyle = gr; g.fillRect(0, 0, 128, 128); });
  const sombra = new THREE.Mesh(new THREE.PlaneGeometry(1.4, 1.4), new THREE.MeshBasicMaterial({ map: sombraTex, transparent: true, depthWrite: false })); sombra.rotation.x = -Math.PI / 2; Q.add(sombra);
  const rebote = new THREE.PointLight("#eaff9a", 0, 5, 1.4); Q.add(rebote);
  const LR = lumi.rig;

  // ======================= APARTAMENTO (cm) =======================
  const A = new THREE.Scene(); A.background = new THREE.Color("#0c0f18");
  const piso = new THREE.Mesh(new THREE.PlaneGeometry(800, 800), new THREE.MeshStandardMaterial({ map: canvasTex(256, 256, (g) => { g.fillStyle = "#6b4a32"; g.fillRect(0, 0, 256, 256); g.fillStyle = "#5a3d29"; for (let i = 0; i < 8; i++) g.fillRect(0, i * 32, 256, 2); }, [16, 16]), roughness: 0.5 }));
  piso.rotation.x = -Math.PI / 2; piso.receiveShadow = true; A.add(piso);
  const pAp = std("#8f877c", 0.9);
  const pf = new THREE.Mesh(new THREE.PlaneGeometry(800, 300), pAp); pf.position.set(0, 150, -300); A.add(pf);
  const pe1 = new THREE.Mesh(new THREE.PlaneGeometry(800, 300), pAp); pe1.position.set(-220, 150, 0); pe1.rotation.y = Math.PI / 2; A.add(pe1);
  const pd1 = new THREE.Mesh(new THREE.PlaneGeometry(800, 300), pAp); pd1.position.set(240, 150, 0); pd1.rotation.y = -Math.PI / 2; A.add(pd1);
  const forro = new THREE.Mesh(new THREE.PlaneGeometry(800, 800), std("#6f685f", 0.9)); forro.rotation.x = Math.PI / 2; forro.position.y = 290; A.add(forro);
  const aAmb = new THREE.HemisphereLight("#fff3e0", "#3a2a20", 0.35); A.add(aAmb);
  const teto = new THREE.PointLight("#ffe4c0", 14000, 900, 1.6); teto.position.set(0, 270, -120); teto.castShadow = true; A.add(teto);
  const tetoLamp = new THREE.Mesh(new THREE.SphereGeometry(14, 20, 14), new THREE.MeshBasicMaterial({ color: "#fff1d6" })); tetoLamp.position.copy(teto.position); tetoLamp.position.y = 276; A.add(tetoLamp);
  // rack + TV
  const rack = caixa(180, 45, 45, std("#2a2a30", 0.5)); rack.position.set(-60, 22, -270); A.add(rack);
  const telaTex = canvasTex(512, 288, (g) => { const gr = g.createLinearGradient(0, 0, 512, 288); gr.addColorStop(0, "#ff5aa8"); gr.addColorStop(0.5, "#5ad1ff"); gr.addColorStop(1, "#ffd35a"); g.fillStyle = gr; g.fillRect(0, 0, 512, 288); g.fillStyle = "#fff"; g.font = "bold 60px sans-serif"; g.fillText("♪ ♫", 200, 170); });
  const telaMat = new THREE.MeshBasicMaterial({ map: telaTex });
  const tv = caixa(130, 76, 6, std("#111", 0.3)); tv.position.set(-60, 95, -280); A.add(tv);
  const tela = new THREE.Mesh(new THREE.PlaneGeometry(124, 70), telaMat); tela.position.set(-60, 95, -276.9); A.add(tela);
  const luzTv = new THREE.PointLight("#9ad8ff", 9000, 400, 1.8); luzTv.position.set(-60, 95, -240); A.add(luzTv);
  // aquário
  const movel = caixa(100, 70, 40, std("#3b2b22", 0.6)); movel.position.set(110, 35, -270); A.add(movel);
  const agua = new THREE.MeshBasicMaterial({ color: "#2a8cff", transparent: true, opacity: 0.85 });
  const aquario = caixa(80, 45, 32, agua); aquario.position.set(110, 93, -270); A.add(aquario);
  const peixes = [];
  for (let i = 0; i < 5; i++) { const p = new THREE.Mesh(new THREE.SphereGeometry(3, 10, 8), new THREE.MeshBasicMaterial({ color: "#ff8a2a" })); p.scale.set(1.6, 1, 0.6); A.add(p); peixes.push(p); }
  const luzAq = new THREE.PointLight("#3aa0ff", 7000, 300, 1.8); luzAq.position.set(110, 100, -230); A.add(luzAq);
  // geladeira
  const gel = caixa(70, 180, 65, std("#e8e8e8", 0.25, { metalness: 0.3 })); gel.position.set(200, 90, -120); A.add(gel);
  const display = new THREE.Mesh(new THREE.PlaneGeometry(14, 6), new THREE.MeshBasicMaterial({ color: "#6af0ff" })); display.position.set(164.8, 120, -120); display.rotation.y = -Math.PI / 2; A.add(display);
  const luzGel = new THREE.PointLight("#bff6ff", 2500, 160, 1.8); luzGel.position.set(150, 120, -120); A.add(luzGel);
  // quadro de disjuntores
  const qd = caixa(4, 40, 30, std("#9a9a9a", 0.5, { metalness: 0.4 })); qd.position.set(-218, 150, -60); A.add(qd);
  const ledsQd = [];
  for (let i = 0; i < 4; i++) { const l = new THREE.Mesh(new THREE.SphereGeometry(1.4, 10, 8), new THREE.MeshBasicMaterial({ color: "#39ff6a" })); l.position.set(-215.8, 160 - i * 6, -60); A.add(l); ledsQd.push(l); }
  const faiscaQd = faisca("#9fe7ff", 0.01); faiscaQd.position.set(-214, 150, -60); A.add(faiscaQd);
  // régua no chão em primeiro plano (pista de continuidade)
  const reguaAp = new THREE.Mesh(new THREE.RoundedBoxGeometry(40, 6, 11, 3, 1.5), std("#eeeeea", 0.4)); reguaAp.position.set(-20, 3, 90); A.add(reguaAp);

  // ======================= PRÉDIO (m) =======================
  const P = new THREE.Scene(); P.background = new THREE.Color("#0b1230");
  P.add(new THREE.HemisphereLight("#5468b0", "#101018", 0.7));
  const ruaP = new THREE.Mesh(new THREE.PlaneGeometry(400, 400), std("#1b1d24", 0.9)); ruaP.rotation.x = -Math.PI / 2; P.add(ruaP);
  const ANDARES = 14, COLS = 7;
  const fachada = caixa(24, ANDARES * 3.2 + 1, 16, std("#a39a8c", 0.85)); fachada.position.set(0, (ANDARES * 3.2 + 1) / 2, 0); P.add(fachada);
  const janGeo = new THREE.PlaneGeometry(2.0, 1.8);
  const janelas = new THREE.InstancedMesh(janGeo, new THREE.MeshBasicMaterial({ color: "#ffffff" }), ANDARES * COLS);
  const corLit = [new THREE.Color("#ffb85c"), new THREE.Color("#fff1c9"), new THREE.Color("#ffd28a")], corOff = new THREE.Color("#0d111e");
  const m4 = new THREE.Matrix4();
  for (let a = 0; a < ANDARES; a++) for (let c = 0; c < COLS; c++) { m4.makeTranslation(-9 + c * 3, 2.4 + a * 3.2, 8.02); janelas.setMatrixAt(a * COLS + c, m4); janelas.setColorAt(a * COLS + c, corLit[(a * 7 + c * 3) % 3]); }
  P.add(janelas);
  const letreiroTex = canvasTex(512, 128, (g) => { g.fillStyle = "#000"; g.fillRect(0, 0, 512, 128); g.fillStyle = "#ff4f8b"; g.font = "bold 84px sans-serif"; g.textAlign = "center"; g.fillText("ED. LUAR", 256, 98); });
  const letreiroMat = new THREE.MeshBasicMaterial({ map: letreiroTex, transparent: true, blending: THREE.AdditiveBlending });
  const letreiro = new THREE.Mesh(new THREE.PlaneGeometry(14, 3.5), letreiroMat); letreiro.position.set(0, ANDARES * 3.2 + 3.5, 8.2); P.add(letreiro);
  const postes = [];
  for (const x of [-16, 0, 16]) {
    const haste2 = caixa(0.25, 6, 0.25, std("#333", 0.5)); haste2.position.set(x, 3, 16); P.add(haste2);
    const cab = new THREE.Mesh(new THREE.SphereGeometry(0.5, 12, 8), new THREE.MeshBasicMaterial({ color: "#ffd9a0" })); cab.position.set(x, 6.2, 16); P.add(cab);
    const l = new THREE.PointLight("#ffcf8a", 220, 25, 1.5); l.position.set(x, 6, 16.5); P.add(l); postes.push({ cab, l });
  }
  // vizinhos (continuam acesos aqui; apagam na cidade)
  for (const [x, h, z] of [[-34, 30, -10], [32, 38, -14], [-60, 22, -30], [60, 26, -40]]) {
    const v = caixa(18, h, 14, std("#5a5650", 0.9)); v.position.set(x, h / 2, z); P.add(v);
    const jv = new THREE.InstancedMesh(janGeo, new THREE.MeshBasicMaterial({ color: "#fff" }), 5 * Math.floor(h / 3.2));
    let n = 0; for (let a = 0; a < Math.floor(h / 3.2); a++) for (let c = 0; c < 5; c++) { m4.makeTranslation(x - 6 + c * 3, 2 + a * 3.2, z + 7.02); jv.setMatrixAt(n, m4); jv.setColorAt(n++, corLit[(a + c) % 3]); }
    P.add(jv);
  }
  const estrelasP = new THREE.Points(new THREE.BufferGeometry().setAttribute("position", new THREE.Float32BufferAttribute(Array.from({ length: 900 }, (_, i) => (i % 3 === 1 ? 60 + rnd() * 260 : (rnd() - 0.5) * 700)).map((v, i) => (i % 3 === 2 ? -250 - Math.abs(v) * 0.3 : v)), 3)), new THREE.PointsMaterial({ color: "#ffffff", size: 1.2, sizeAttenuation: false }));
  P.add(estrelasP);

  // ======================= CIDADE (m) =======================
  const C = new THREE.Scene(); C.background = new THREE.Color("#070b1c");
  const N = 46, PASSO = 26;
  const janTex = canvasTex(64, 128, (g) => { g.fillStyle = "#08090f"; g.fillRect(0, 0, 64, 128); for (let y = 6; y < 128; y += 12) for (let x = 6; x < 64; x += 14) { g.fillStyle = Math.random() < 0.75 ? "#ffcc7a" : "#20202a"; g.fillRect(x, y, 8, 6); } }, null);
  const predios = new THREE.InstancedMesh(new THREE.BoxGeometry(1, 1, 1), new THREE.MeshBasicMaterial({ map: janTex }), N * N);
  const dist = [], torres = [];
  let k = 0;
  for (let i = 0; i < N; i++) for (let j = 0; j < N; j++) {
    const x = (i - N / 2) * PASSO + (rnd() - 0.5) * 6, z = (j - N / 2) * PASSO + (rnd() - 0.5) * 6;
    const d = Math.hypot(x, z); const alto = 10 + rnd() * 30 + Math.max(0, 60 - d * 0.08) * rnd();
    const w = 10 + rnd() * 10;
    m4.compose(V(x, alto / 2, z), new THREE.Quaternion(), V(w, alto, w)); predios.setMatrixAt(k, m4);
    predios.setColorAt(k, new THREE.Color(1, 1, 1)); dist.push(d);
    if (alto > 55 && torres.length < 40) torres.push({ p: V(x, alto + 1.5, z), d });
    k++;
  }
  C.add(predios);
  // ruas: shader com grade iluminada que apaga atrás do raio uR
  const ruaMat = new THREE.ShaderMaterial({
    uniforms: { uR: { value: 0 }, uPasso: { value: PASSO } },
    vertexShader: "varying vec2 vP; void main(){ vec4 w = modelMatrix*vec4(position,1.); vP = w.xz; gl_Position = projectionMatrix*viewMatrix*w; }",
    fragmentShader: "uniform float uR; uniform float uPasso; varying vec2 vP; void main(){ vec2 g = abs(fract(vP/uPasso + 0.5) - 0.5)*uPasso; float l = 1. - smoothstep(0.6, 2.2, min(g.x, g.y)); float d = length(vP); float on = smoothstep(uR - 6., uR + 6., d); vec3 c = mix(vec3(0.015,0.018,0.035), vec3(1.0,0.72,0.35), l*on); gl_FragColor = vec4(c,1.); }",
  });
  const ruas = new THREE.Mesh(new THREE.PlaneGeometry(N * PASSO * 1.6, N * PASSO * 1.6), ruaMat); ruas.rotation.x = -Math.PI / 2; C.add(ruas);
  const vermelhas = torres.map((t) => { const s = faisca("#ff3030", 9); s.position.copy(t.p); C.add(s); return s; });
  const outTex = canvasTex(512, 160, (g) => { g.fillStyle = "#111"; g.fillRect(0, 0, 512, 160); g.fillStyle = "#3dff9a"; g.font = "bold 92px sans-serif"; g.textAlign = "center"; g.fillText("BOA NOITE", 256, 112); });
  const outdoor = new THREE.Mesh(new THREE.PlaneGeometry(70, 22), new THREE.MeshBasicMaterial({ map: outTex })); outdoor.position.set(130, 60, 120); outdoor.rotation.y = -0.6; C.add(outdoor);
  const distOutdoor = Math.hypot(130, 120);
  for (let i = 0; i < 9; i++) { const m = new THREE.Mesh(new THREE.SphereGeometry(220 + rnd() * 160, 24, 12), new THREE.MeshBasicMaterial({ color: "#05060d" })); const a = (i / 9) * Math.PI * 2; m.position.set(Math.cos(a) * 1300, -120, Math.sin(a) * 1300); m.scale.y = 0.5; C.add(m); }
  // céu (estrelas individuais + lua) — usado pela cidade e pelo plano do céu
  const NE = 420;
  const estrelas = new THREE.InstancedMesh(new THREE.SphereGeometry(1, 6, 4), new THREE.MeshBasicMaterial({ color: "#ffffff" }), NE);
  const estrelaInfo = [];
  for (let i = 0; i < NE; i++) {
    const az = rnd() * Math.PI * 2, el = 0.12 + rnd() * 1.35;
    const p = V(Math.cos(az) * Math.cos(el), Math.sin(el), Math.sin(az) * Math.cos(el)).multiplyScalar(5000);
    estrelaInfo.push({ p, s: 6 + rnd() * 14, off: 16.85 + Math.pow(rnd(), 0.6) * 1.6 });
  }
  C.add(estrelas);
  const luaMesh = new THREE.Mesh(new THREE.SphereGeometry(260, 32, 24), new THREE.MeshBasicMaterial({ color: "#f4f0e0" })); luaMesh.position.set(900, 3200, -3600); C.add(luaMesh);
  const halo = faisca("#d8e4ff", 1600); halo.material.opacity = 0.5; halo.position.copy(luaMesh.position); C.add(halo);

  // ======================= ATUAÇÃO DO LUMI =======================
  const CAMA_LUMI = V(-0.6, 0.35, 0);
  const PE_BOTAO = botaoMundo.clone().addScaledVector(dir, 0.85).setY(0); // em pé, de frente para o botão
  const RY_BOTAO = Math.atan2(dir.x, dir.z); // de costas para o botão, de frente para a cama
  function atuarQuarto(t) {
    lumi.neutro();
    const R2 = LR;
    let pos = CAMA_LUMI.clone(), ry = Math.PI / 2, rx = 0, voando = false;
    let ex = { olhos: 1, boca: "reta" };
    if (t < 2.2) { // na cama, recostado olhando para +x; abre um olho, cobre a cabeça, encara o abajur
      rx = -0.95; pos = V(-0.9, 0.35, 0);
      ex = { olhoE: t < 0.45 ? 1 : 0.45, olhoD: 1, boca: "reta", antenas: -0.2, tremor: t > 1.6 ? t : 0 };
      if (t > 1.5) { ex.olhoD = 0.45; R2.cabeca.rotation.y = -ease.out(sm(1.5, 1.9, t)) * 1.1; R2.cabeca.rotation.x = -0.25 * sm(1.5, 1.9, t); ex.olharX = -1; }
    } else if (t < 3.0) { // voa da cama até o botão
      const k = ease.inOut((t - 2.2) / 0.8);
      pos = CAMA_LUMI.clone().lerp(PE_BOTAO, k); pos.y += Math.sin(k * Math.PI) * 3.5 + 0.3 * (1 - k);
      ry = E.lerp(Math.PI / 2, RY_BOTAO + Math.PI * 2 * (RY_BOTAO < 0 ? 1 : 0), k); ry = RY_BOTAO * k + (Math.PI / 2) * (1 - k);
      voando = true; ex = { olhos: 0.35, boca: "reta", antenas: 0.3 };
      R2.ombroE.rotation.z = 1.2; R2.ombroD.rotation.z = -1.2;
    } else if (t < 4.6) { // empurra o botão com tudo
      pos = PE_BOTAO.clone(); ry = RY_BOTAO;
      const f = sm(3.0, 3.2, t) * (1 - sm(4.2, 4.35, t));
      pos.addScaledVector(dir, 0.12 * f + Math.sin(t * 40) * 0.015 * f); rx = -0.35 * f; // inclina para trás, empurrando com o bumbum
      R2.ombroE.rotation.set(-0.6 * f, 0, 0.9 * f + 0.2); R2.ombroD.rotation.set(-0.6 * f, 0, -0.9 * f - 0.2);
      R2.pernas.forEach((p, i) => (p.rotation.x = Math.sin(t * 28 + i * 1.6) * 0.6 * f));
      ex = f > 0.3 ? { olhos: 1, boca: "esforco", bochecha: 1, antenas: 0.8, tremor: t } : { olhos: 0.45, boca: "triste", antenas: -0.4 };
      if (t > 4.3) ex = { olhos: 0.5, boca: "O", grito: 0, antenas: -0.3 }; // ofegante
    } else if (t < 7.4) { // recua, chuta, comemora, vê a faísca
      ry = RY_BOTAO;
      const recuo = sm(4.6, 5.0, t) * (1 - sm(5.25, 5.4, t));
      pos = PE_BOTAO.clone().addScaledVector(dir, 0.9 * recuo);
      // antecipação: perna gira; chute em 5,35
      const anti = sm(4.8, 5.25, t) * (1 - sm(5.3, 5.36, t));
      for (const n of [2, 3]) R2.pernas[n].rotation.x = -0.6 * anti * Math.sin(t * 30) + 1.9 * sm(5.3, 5.36, t) * (1 - sm(5.6, 5.9, t)); // coice para trás
      rx = 0.25 * anti + 0.35 * sm(5.3, 5.36, t) * (1 - sm(5.6, 5.9, t));
      ex = { olhos: 0.3, boca: "esforco", antenas: 0.5, olharX: 0 };
      if (t > 5.4) { ex = { olhos: 0, pupila: 0.7, boca: "O", grito: 0.3, antenas: 0.6, olharY: 1 }; R2.cabeca.rotation.x = -0.5; }
      if (t > 6.45) { // comemora no escuro
        const pulo = Math.abs(Math.sin((t - 6.45) * 12)) * 0.6 * (1 - sm(6.85, 6.95, t));
        pos.y += pulo; R2.cabeca.rotation.x = -0.15;
        R2.ombroE.rotation.z = 2.7; R2.ombroD.rotation.z = -2.7;
        ex = { olhos: 0.1, baixo: 0.6, boca: "riso", antenas: 0.6 };
      }
      if (t > 6.92) { // estalo: congela e olha a faísca (à direita)
        R2.ombroE.rotation.z = 2.4; R2.ombroD.rotation.z = -2.4;
        R2.cabeca.rotation.y = 1.2 * sm(6.92, 7.05, t);
        ex = { olhos: 0, pupila: 0.35, boca: "O", grito: 0.6, antenas: 1, olharX: 1 };
      }
    }
    lumi.root.position.copy(pos);
    lumi.root.rotation.set(rx, ry, 0, "YXZ");
    lumi.asas(t, voando);
    lumi.rosto(ex);
  }
  const LUMI_ESCURO = V(0.4, 0.15, 0.2);
  const RY_ESC = -0.35; // corpo de lado (olha para a esquerda da câmera), bumbum à direita
  function atuarEscuro(t) { // cenas 8 e 9: sentado recostado na caixa, de 3/4 para a câmera; o bumbum brilha atrás
    lumi.neutro();
    lumi.root.position.copy(LUMI_ESCURO);
    lumi.root.rotation.set(-0.35, RY_ESC, 0, "YXZ");
    LR.ombroE.rotation.set(-0.4, 0, 0.6); LR.ombroD.rotation.set(-0.4, 0, -0.6);
    LR.cabeca.rotation.y = 1.0; // rosto para a câmera
    let ex = { olhos: 1, baixo: 0.3, boca: "sorriso", antenas: -0.3 };
    if (t > 20.3) ex = { olhoE: 0.45, olhoD: 1, boca: "reta", antenas: -0.2 };
    if (t > 20.8) { // olha por cima do ombro, para o próprio bumbum
      const k = sm(20.8, 21.3, t) * (1 - sm(21.9, 22.3, t));
      LR.cabeca.rotation.y = 1.0 + 1.3 * k; LR.cabeca.rotation.x = 0.3 * k;
      ex = { olhos: 0.45, boca: "reta", antenas: 0.4 * k, olharX: 1 };
    }
    if (t > 22.3) ex = { olhos: 0.5, boca: "reta", antenas: 0 };
    if (t > 22.5) ex = { olhos: 0.3, baixo: 0.4, boca: "amarelo", antenas: -0.7 };
    if (t > 23.0) LR.ombroE.rotation.set(-0.4 + 1.4 * sm(23.0, 23.5, t), 0, 0.6 + 1.2 * sm(23.0, 23.5, t)); // puxa a meia para trás
    if (t > 23.9) ex = { olhos: 1, baixo: 0.3, boca: "sorriso", antenas: -0.5 };
    lumi.asas(t, false); lumi.rosto(ex);
    rebote.position.copy(LUMI_ESCURO).add(V(0.9, 1.1, 1.0));
  }

  // ======================= PLANOS =======================
  // cada plano: [t0, t1, cena, câmera pos(t), alvo(t), fov]
  const PERP = V(-dir.z, 0, dir.x); // perpendicular ao eixo abajur→cama, do lado da câmera
  const arr = (v) => [v.x, v.y, v.z];
  const alvoLumi = () => lumi.root.position.clone().add(V(0, 0.75, 0));
  const fixo = (v) => () => v;
  const CENTRO_AB = centroAbajur.clone();
  const PL = [
    // 1 gancho: baixo e aberto, Lumi no terço de baixo, abajur aceso no alto
    { t0: 0, t1: 2.2, cena: Q, pos: tr([[0, [3.3, 2.5, 2.5]], [2.2, [2.7, 2.2, 2.0]]]), alvo: tr([[0, [-2.8, 2.6, -1.8]], [2.2, [-2.6, 2.4, -1.7]]]), fov: 58 },
    // 2 voo + empurrão: segue o Lumi; perfil quando ele empurra
    { t0: 2.2, t1: 4.6, cena: Q, f: (t) => { const a = alvoLumi(); const k = sm(2.2, 3.0, t); const p = a.clone().add(V(2.2, 0.8, 2.4).lerp(PERP.clone().multiplyScalar(0.9).addScaledVector(dir, 2.7).add(V(0, 0.55, 0)), k)); return [arr(p), arr(a)]; }, fov: 42 },
    // 3a antecipação do chute (perfil, um pouco mais aberto)
    { t0: 4.6, t1: 5.4, cena: Q, f: () => { const a = alvoLumi(); return [arr(a.clone().addScaledVector(PERP, 1.4).addScaledVector(dir, 3.2).add(V(0, 0.6, 0))), arr(a)]; }, fov: 46 },
    // 3b o abajur cai (geral de lado)
    { t0: 5.4, t1: 6.35, cena: Q, pos: fixo(arr(CENTRO_AB.clone().addScaledVector(PERP, 42).addScaledVector(dir, 10).add(V(0, 16, 0)))), alvo: fixo(arr(CENTRO_AB.clone().addScaledVector(dir, -6).add(V(0, 9, 0)))), fov: 52 },
    // 3c comemora no escuro e ouve o estalo
    { t0: 6.35, t1: 7.1, cena: Q, f: () => { const a = alvoLumi(); return [arr(a.clone().addScaledVector(dir, 2.6).addScaledVector(PERP, 0.9).add(V(0, 0.6, 0))), arr(a)]; }, fov: 46 },
    // 3d whip-pan até a régua
    { t0: 7.1, t1: 7.4, cena: Q, f: (t) => { const a = alvoLumi(); const k = ease.in(sm(7.1, 7.4, t)); const p0 = a.clone().addScaledVector(dir, 2.6).addScaledVector(PERP, 0.9).add(V(0, 0.6, 0)); const alvo = a.clone().lerp(V(15.5, 2, -14), k); return [arr(p0.lerp(V(12.5, 5.5, -4), k)), arr(alvo)]; }, fov: 44 },
    { t0: 7.4, t1: 8.9, cena: Q, pos: tr([[7.4, [12.5, 5.5, -4]], [8.9, [13.5, 4.6, -6.5]]]), alvo: tr([[7.4, [15.5, 2, -14]], [8.9, [15.5, 2, -14]]]), fov: 44 },
    { t0: 8.9, t1: 10.2, cena: A, pos: tr([[8.9, [0, 22, 360]], [10.2, [0, 26, 320]]]), alvo: tr([[8.9, [0, 105, -260]], [10.2, [0, 110, -260]]]), fov: 66 },
    { t0: 10.2, t1: 13.2, cena: P, pos: tr([[10.2, [6, 2.5, 40]], [13.2, [5, 4, 44]]]), alvo: tr([[10.2, [0, 20, 0]], [13.2, [0, 46, 0]]]), fov: 72 },
    { t0: 13.2, t1: 16.6, cena: C, pos: tr([[13.2, [60, 220, 160]], [16.6, [180, 900, 640], "out"]]), alvo: tr([[13.2, [0, 0, 0]], [16.6, [0, 0, 0]]]), fov: 50 },
    { t0: 16.6, t1: 19.0, cena: C, pos: tr([[16.6, [180, 900, 640]], [17.2, [180, 900, 640]]]), alvo: tr([[16.6, [0, 0, 0]], [17.2, [300, 2400, -2600], "inOut"]]), fov: 50 },
    // 8–9 escuro: push-in do pontinho até o rosto e o bumbum
    { t0: 19.0, t1: 26.0, cena: Q, f: (t) => { const a = LUMI_ESCURO.clone().add(V(0.12, 0.6, -0.3)); const k = ease.inOut(sm(19.4, 22.0, t)); const longe = a.clone().add(V(70, 45, 110)); const perto = a.clone().add(V(2.6, 1.5, 2.0)); return [arr(longe.lerp(perto, k)), arr(a)]; }, fov: 36 },
  ];

  const corQ = new THREE.Color();
  function renderAt(t) {
    t = cl(t, 0, DUR - 1e-3);
    const pl = PL.find((p) => t >= p.t0 && t < p.t1) || PL[PL.length - 1];
    const cena = pl.cena;

    // ---------- quarto ----------
    if (cena === Q) {
      const escuro = t >= 19.0;
      // abajur: cai de 5,4 a 6,3; apaga no impacto
      const queda = ease.in(sm(5.4, 6.3, t));
      pivo.rotation.x = queda * 1.38 + (t > 6.3 && t < 6.6 ? Math.sin((t - 6.3) * 40) * 0.02 * (1 - (t - 6.3) / 0.3) : 0);
      const aceso = t < 6.3 && !escuro;
      luzAbajur.intensity = aceso ? 2600 : 0; cupulaMat.emissiveIntensity = aceso ? 1 : 0; lampada.visible = aceso;
      qAmb.intensity = escuro ? 0 : aceso ? 0.35 : 0.2; lua.intensity = escuro ? 0 : aceso ? 0.9 : 0.7;
      fill.intensity = escuro ? 0 : aceso ? 1.6 : 0.9;
      Q.background.set(escuro ? "#000000" : "#0b1022"); pivo.visible = !escuro; regua.visible = !escuro; tampinha.visible = !escuro;
      Q.fog.color.set(escuro ? "#000000" : "#0b1022"); if (!escuro) rebote.intensity = 0; janela.visible = !escuro; parede.visible = !escuro;
      // plugue do abajur escapa da régua
      const sai = sm(6.32, 6.5, t);
      tomadas[0].position.y = 2 + sai * 1.6; tomadas[0].rotation.z = sai * 0.7;
      // faíscas: na régua (6,9) e pulando de tomada em tomada (7,4 / 7,95 / 8,5)
      const fpos = fioCurva.getPointAt(1);
      faiscaFio.position.copy(fpos).add(V(0, 0.8, 0));
      const fz = t > 6.88 && t < 7.4 ? 4.5 + Math.sin(t * 90) * 1.5 : 0; faiscaFio.scale.setScalar(Math.max(0.01, fz));
      let flash = fz > 0 ? 40 : 0;
      [7.4, 7.95, 8.5].forEach((tp, i) => { const a = t >= tp && t < tp + 0.3 ? (1 - (t - tp) / 0.3) * 9 + 2 * Math.sin(t * 80) : 0; faiscasRegua[i + 1].scale.setScalar(Math.max(0.01, a)); if (a > 0) flash = 60; if (t >= tp) tomadas[i + 1].children[0].material.color.set("#3a3a3a"); else tomadas[i + 1].children[0].material.color.set("#f2f2ee"); });
      luzFaisca.position.copy(t < 7.4 ? faiscaFio.position : regua.position.clone().add(V(0, 4, 2)));
      luzFaisca.intensity = flash;
      led.material.color.set(t < 8.5 ? (t > 6.9 && Math.sin(t * 50) > 0 ? "#ffffff" : "#ff3030") : "#200000");
      // Lumi
      if (escuro) atuarEscuro(t); else atuarQuarto(t);
      const lp = lumi.root.position; sombra.position.set(lp.x, (t < 2.2 || escuro ? 0.12 : 0.01), lp.z); sombra.visible = !escuro && t >= 2.2; const alt = Math.max(0, lp.y - 0.0); sombra.scale.setScalar(1 + alt * 0.3); sombra.material.opacity = cl(1 - alt * 0.3, 0.2, 1);
      // cama e meia
      if (!escuro) {
        meia.scale.set(1, 1, 1);
        if (t < 2.2) { // meia por cima, sobe até a cabeça (0,8–1,4)
          const cobre = sm(0.8, 1.0, t) * (1 - sm(1.3, 1.5, t));
          meia.position.set(0.4 - cobre * 0.9, 0.85 + cobre * 0.35, 0); meia.rotation.set(0, 0, 0.25 + cobre * 0.3);
        } else { meia.position.set(0.6, 0.55, 0); meia.rotation.set(0, 0, 0.05); }
        lumi.luz.intensity = 0.6; lumi.luzMat.emissiveIntensity = 0.35; meia.material.emissiveIntensity = t < 2.2 ? 0.18 : 0;
      } else {
        // a meia cobre as pernas; em 23,2–23,7 ela sobe por cima do bumbum
        const cobre = sm(23.15, 23.7, t);
        lumi.root.updateMatrixWorld(true); const bw = LR.bunda.getWorldPosition(V());
        const lado = V(1.4, 0.25, -0.8), sobre = bw.clone().add(V(0, 0.22, 0));
        meia.position.copy(lado.lerp(sobre, cobre)); meia.rotation.set(0.3 * cobre, RY_ESC, 0.2 * cobre); meia.scale.set(0.42, 1.1, 0.5);
        const brilho = 1 - cobre;
        const pisca = (t >= 24.8 && t < 25.15 ? Math.sin(((t - 24.8) / 0.35) * Math.PI) : 0) + (t >= 25.4 && t < 25.75 ? Math.sin(((t - 25.4) / 0.35) * Math.PI) : 0);
        const vis = t < 19.4 ? 0 : 1;
        lumi.luz.intensity = vis * (1.4 * brilho + 0.35 * pisca);
        lumi.luzMat.emissiveIntensity = vis * (1.1 * brilho + 0.4 * pisca);
        meia.material.emissiveIntensity = 0.25 * pisca;
        lumi.root.visible = vis > 0;
        rebote.intensity = lumi.luz.intensity * 1.1;
      }
    }

    // ---------- apartamento ----------
    if (cena === A) {
      const tvOn = t < 9.05, aqOn = t < 9.25, gelOn = t < 9.45, tudo = t < 9.7;
      telaMat.color.set(tvOn ? "#ffffff" : "#050505"); luzTv.intensity = tvOn ? 9000 * (0.8 + 0.2 * Math.sin(t * 13)) : 0;
      agua.color.set(aqOn ? "#2a8cff" : "#0a1220"); luzAq.intensity = aqOn ? 7000 : 0;
      peixes.forEach((p, i) => p.position.set(110 + Math.sin(t * 1.5 + i) * 30, 85 + i * 3, -270 + Math.cos(t + i * 2) * 8));
      display.material.color.set(gelOn ? "#6af0ff" : "#050505"); luzGel.intensity = gelOn ? 2500 : 0;
      gel.position.x = 200 + (t > 9.4 && t < 9.6 ? Math.sin(t * 120) * 1.5 : 0);
      ledsQd.forEach((l) => l.material.color.set(tudo ? "#39ff6a" : t < 9.85 ? "#ff3030" : "#200000"));
      faiscaQd.scale.setScalar(t >= 9.68 && t < 9.95 ? 30 + Math.sin(t * 90) * 10 : 0.01);
      teto.intensity = tudo ? 14000 : 0; tetoLamp.material.color.set(tudo ? "#fff1d6" : "#111"); aAmb.intensity = tudo ? 0.35 : 0.03;
    }

    // ---------- prédio ----------
    if (cena === P) {
      const onda = (t - 10.4) / 0.16; // andares a partir do 7º
      for (let a = 0; a < ANDARES; a++) for (let c = 0; c < COLS; c++) {
        const off = a === 6 || Math.abs(a - 6) <= onda;
        janelas.setColorAt(a * COLS + c, off ? corOff : corLit[(a * 7 + c * 3) % 3]);
      }
      janelas.instanceColor.needsUpdate = true;
      const let_ = t < 12.3 ? 1 : t < 12.6 ? (Math.sin(t * 70) > 0 ? 1 : 0.1) : 0;
      letreiroMat.opacity = let_;
      postes.forEach((p, i) => { const on = t < 12.75 + i * 0.08; p.l.intensity = on ? 220 : 0; p.cab.material.color.set(on ? "#ffd9a0" : "#222"); });
    }

    // ---------- cidade e céu ----------
    if (cena === C) {
      const uR = t < 13.4 ? 0 : ease.in(sm(13.4, 16.3, t)) * 900;
      ruaMat.uniforms.uR.value = uR;
      const cor = new THREE.Color();
      for (let i = 0; i < dist.length; i++) predios.setColorAt(i, dist[i] < uR || dist[i] < 14 ? cor.setRGB(0.02, 0.02, 0.035) : cor.setRGB(1, 1, 1));
      predios.instanceColor.needsUpdate = true;
      vermelhas.forEach((s, i) => { const on = torres[i].d > uR && Math.sin(t * 6 + i) > -0.3; s.visible = on; });
      outdoor.material.color.set(distOutdoor > uR + 40 ? "#ffffff" : distOutdoor > uR ? (Math.sin(t * 60) > 0 ? "#ffffff" : "#222") : "#050505");
      for (let i = 0; i < NE; i++) {
        const s = t < estrelaInfo[i].off ? estrelaInfo[i].s * (0.8 + 0.2 * Math.sin(t * 3 + i)) : 0.0001;
        m4.compose(estrelaInfo[i].p, new THREE.Quaternion(), V(s, s, s)); estrelas.setMatrixAt(i, m4);
      }
      estrelas.instanceMatrix.needsUpdate = true;
      const luaOn = t < 18.6; luaMesh.visible = luaOn; halo.visible = luaOn;
      C.background.set(t < 18.6 ? "#070b1c" : "#000000");
      if (t >= 18.6) { predios.visible = false; ruas.visible = false; } else { predios.visible = true; ruas.visible = true; }
    }

    const [p, a] = pl.f ? pl.f(t) : [pl.pos(t), pl.alvo(t)];
    cam.fov = pl.fov; cam.near = cena === Q ? 0.05 : 0.5; cam.far = cena === C ? 20000 : 3000; cam.updateProjectionMatrix();
    cam.position.set(p[0], p[1], p[2]); cam.lookAt(a[0], a[1], a[2]);
    R.render(cena, cam);
  }

  window.addEventListener("hf-seek", (e) => renderAt(e.detail.time));
  window.__hf = window.__hf || {}; window.__hf.buildReady = window.__hf.buildReady || {};
  window.__hf.buildReady["apagao"] = new Promise((res) => { for (const x of [0.5, 3.5, 6, 8, 9.5, 11, 14, 18, 21, 24]) renderAt(x); renderAt(window.__timelines["main"].time()); R.getContext().finish(); res(); });
})();
