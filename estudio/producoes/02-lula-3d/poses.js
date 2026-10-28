/* As 8 variações da referência, como poses do rig + acessórios. ?pose=1..8 */
(function () {
  const THREE = window.THREE;
  const E = window.Estudio3D;
  const W = 1024, H = 1024;
  const params = new URLSearchParams(location.search);
  const N = Number(params.get("pose") || 1);
  const ANG = Number(params.get("ang") || 0); // giro extra da câmera (turntable)

  const renderer = new THREE.WebGLRenderer({ canvas: document.getElementById("c"), antialias: true, alpha: true, preserveDrawingBuffer: true });
  renderer.setPixelRatio(1); renderer.setSize(W, H, false);
  renderer.setClearColor(0x000000, 0);
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.toneMapping = THREE.ACESFilmicToneMapping; renderer.toneMappingExposure = 1.05;
  renderer.shadowMap.enabled = true; renderer.shadowMap.type = THREE.PCFSoftShadowMap;

  const cena = new THREE.Scene();
  const cam = new THREE.PerspectiveCamera(26, W / H, 0.1, 100);

  // luz de estúdio: chave quente, preenchimento frio, contra, ambiente
  cena.add(new THREE.HemisphereLight("#ffffff", "#b8b0a8", 1.1));
  const chave = new THREE.DirectionalLight("#fff1e2", 2.6); chave.position.set(4, 9, 7);
  chave.castShadow = true; chave.shadow.mapSize.set(2048, 2048); chave.shadow.radius = 8; chave.shadow.bias = -0.0005;
  Object.assign(chave.shadow.camera, { left: -6, right: 6, top: 8, bottom: -3, near: 1, far: 30 });
  cena.add(chave);
  const pre = new THREE.DirectionalLight("#dfe8ff", 0.9); pre.position.set(-6, 3, 5); cena.add(pre);
  const contra = new THREE.DirectionalLight("#ffffff", 1.6); contra.position.set(-2, 6, -7); cena.add(contra);
  const chao = new THREE.Mesh(new THREE.PlaneGeometry(30, 30), new THREE.ShadowMaterial({ opacity: 0.22 }));
  chao.rotation.x = -Math.PI / 2; chao.receiveShadow = true; cena.add(chao);

  const P = window.Caricatura.criar(THREE);
  P.root.traverse((o) => { if (o.isMesh) { o.castShadow = true; } });
  cena.add(P.root);

  // ---------- acessórios ----------
  const mat = (c, r = 0.5, extra = {}) => new THREE.MeshPhysicalMaterial({ color: c, roughness: r, ...extra });
  function texto(str, cor, tam = 200, fonte = "900 {s}px Arial Black, Arial, sans-serif") {
    const c = document.createElement("canvas"); c.width = 512; c.height = 256;
    const g = c.getContext("2d"); g.font = fonte.replace("{s}", tam); g.fillStyle = cor; g.textAlign = "center"; g.textBaseline = "middle";
    g.fillText(str, 256, 135);
    const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace;
    const sp = new THREE.Sprite(new THREE.SpriteMaterial({ map: t, depthWrite: false })); sp.scale.set(2, 1, 1); return sp;
  }
  function estrela(r = 1, cor = "#e3342b") {
    const s = new THREE.Shape();
    for (let i = 0; i < 10; i++) {
      const a = Math.PI / 2 + (i * Math.PI) / 5, rr = i % 2 ? r * 0.45 : r;
      i ? s.lineTo(Math.cos(a) * rr, Math.sin(a) * rr) : s.moveTo(Math.cos(a) * rr, Math.sin(a) * rr);
    }
    const geo = new THREE.ExtrudeGeometry(s, { depth: r * 0.35, bevelEnabled: true, bevelThickness: r * 0.18, bevelSize: r * 0.16, bevelSegments: 6 });
    geo.center();
    return new THREE.Mesh(geo, mat(cor, 0.45, { sheen: 0.6, sheenColor: new THREE.Color("#ff8a80") }));
  }
  function bone(corCopa, corAba, frente) {
    const g = new THREE.Group();
    const copa = new THREE.Mesh(new THREE.SphereGeometry(1.06, 40, 20, 0, Math.PI * 2, 0, Math.PI / 2), mat(corCopa, 0.7, { sheen: 0.4 }));
    copa.scale.set(1, 0.72, 1.02); g.add(copa);
    const aba = new THREE.Mesh(new THREE.CylinderGeometry(0.95, 0.95, 0.06, 40, 1, false, -Math.PI / 2.6, Math.PI / 1.3), mat(corAba, 0.6));
    aba.position.set(0, 0.02, 0.55); aba.scale.set(1, 1, 0.9); g.add(aba);
    const botao = new THREE.Mesh(new THREE.SphereGeometry(0.09, 16, 10), mat(corCopa, 0.6)); botao.position.y = 0.76; g.add(botao);
    if (frente) {
      const c = document.createElement("canvas"); c.width = 512; c.height = 256; frente(c.getContext("2d"));
      const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace;
      const painel = new THREE.Mesh(new THREE.SphereGeometry(1.075, 40, 16, Math.PI / 2 - 0.75, 1.5, 0.95, 0.55), new THREE.MeshStandardMaterial({ map: t, transparent: true, roughness: 0.7 }));
      painel.scale.set(1, 0.72, 1.02); painel.rotation.y = 0; g.add(painel);
    }
    return g;
  }
  const boneBrasil = () => bone("#1f9a45", "#16803a", (g) => {
    g.font = "900 120px Arial Black, Arial, sans-serif"; g.fillStyle = "#ffd21f"; g.textAlign = "center"; g.textBaseline = "middle"; g.fillText("BRASIL", 256, 136);
  });
  const boneAzul = () => bone("#2453c4", "#2fae55", (g) => {
    g.fillStyle = "#1e9c4a"; g.fillRect(146, 58, 220, 150);
    g.fillStyle = "#ffd21f"; g.beginPath(); g.moveTo(256, 68); g.lineTo(356, 133); g.lineTo(256, 198); g.lineTo(156, 133); g.fill();
    g.fillStyle = "#1d3f9e"; g.beginPath(); g.arc(256, 133, 42, 0, Math.PI * 2); g.fill();
    g.strokeStyle = "#fff"; g.lineWidth = 7; g.beginPath(); g.arc(256, 165, 52, -2.35, -0.8); g.stroke();
  });
  function pizza() {
    const g = new THREE.Group();
    const s = new THREE.Shape(); s.moveTo(0, 0); s.lineTo(-0.42, 1.0); s.quadraticCurveTo(0, 1.12, 0.42, 1.0); s.closePath();
    const massa = new THREE.Mesh(new THREE.ExtrudeGeometry(s, { depth: 0.06, bevelEnabled: true, bevelSize: 0.03, bevelThickness: 0.03 }), mat("#e9a74f", 0.8)); g.add(massa);
    const queijo = new THREE.Mesh(new THREE.ShapeGeometry(s), mat("#ffd25a", 0.5)); queijo.scale.set(0.9, 0.9, 1); queijo.position.set(0, 0.04, 0.1); g.add(queijo);
    const borda = new THREE.Mesh(new THREE.CapsuleGeometry(0.08, 0.75, 6, 12), mat("#cf8a3a", 0.8)); borda.rotation.z = Math.PI / 2; borda.position.set(0, 1.03, 0.05); g.add(borda);
    for (const [x, y] of [[0, 0.75], [-0.18, 0.5], [0.15, 0.45], [0.02, 0.25]]) {
      const p = new THREE.Mesh(new THREE.CylinderGeometry(0.09, 0.09, 0.03, 20), mat("#c5352c", 0.5)); p.rotation.x = Math.PI / 2; p.position.set(x, y, 0.12); g.add(p);
    }
    return g;
  }
  function garfo() {
    const g = new THREE.Group(); const m = mat("#d9dde3", 0.2, { metalness: 1 });
    const cabo = new THREE.Mesh(new THREE.BoxGeometry(0.06, 0.9, 0.035), m); g.add(cabo);
    for (const x of [-0.06, -0.02, 0.02, 0.06]) { const d = new THREE.Mesh(new THREE.BoxGeometry(0.018, 0.25, 0.02), m); d.position.set(x, 0.55, 0); g.add(d); }
    const base = new THREE.Mesh(new THREE.BoxGeometry(0.16, 0.06, 0.03), m); base.position.y = 0.43; g.add(base);
    return g;
  }
  function livro() {
    const c = document.createElement("canvas"); c.width = 512; c.height = 640;
    const g = c.getContext("2d");
    const gr = g.createLinearGradient(0, 0, 512, 640); gr.addColorStop(0, "#7fc3ee"); gr.addColorStop(1, "#3d8fd0");
    g.fillStyle = gr; g.fillRect(0, 0, 512, 640);
    g.fillStyle = "#174d86"; g.font = "italic 700 92px Georgia, serif"; g.textAlign = "center"; g.fillText("História", 256, 190);
    g.fillStyle = "#ffd21f"; g.beginPath();
    for (let i = 0; i < 10; i++) { const a = -Math.PI / 2 + (i * Math.PI) / 5, r = i % 2 ? 40 : 95; g.lineTo(256 + Math.cos(a) * r, 400 + Math.sin(a) * r); }
    g.fill();
    const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace;
    const capa = mat("#3d8fd0", 0.55);
    const frente = new THREE.MeshStandardMaterial({ map: t, roughness: 0.55 });
    const paginas = mat("#f4efe2", 0.9);
    const box = new THREE.Mesh(new THREE.BoxGeometry(1.0, 1.25, 0.2), [paginas, capa, paginas, paginas, frente, capa]);
    return box;
  }
  function confete(n = 70) {
    const g = new THREE.Group(); const r = E.aleatorio(7);
    const cores = ["#1f9a45", "#f5c518", "#e3342b", "#2453c4"];
    for (let i = 0; i < n; i++) {
      const m = new THREE.Mesh(new THREE.PlaneGeometry(0.12, 0.26), new THREE.MeshStandardMaterial({ color: cores[i % 4], side: THREE.DoubleSide, roughness: 0.6 }));
      const a = r() * Math.PI * 2, d = 1.5 + r() * 2.2;
      m.position.set(Math.cos(a) * d, 5.0 + r() * 3.2, Math.sin(a) * d * 0.5);
      m.rotation.set(r() * 6, r() * 6, r() * 6); g.add(m);
    }
    return g;
  }
  const naMao = (lado, obj, pos, rot) => { obj.position.set(...pos); obj.rotation.set(...(rot || [0, 0, 0])); P.rig[lado].add(obj); return obj; };
  const naCabeca = (obj, pos, rot) => { obj.position.set(...pos); obj.rotation.set(...(rot || [0, 0, 0])); P.rig.cabeca.add(obj); return obj; };

  // ---------- poses (ângulos em rad: [x, y, z]) ----------
  const SENTA = { coxaE: [-1.5, 0, -0.12], coxaD: [-1.5, 0, 0.12], joelhoE: [0.15, 0, 0], joelhoD: [0.15, 0, 0], peE: [-0.2, 0, 0], peD: [-0.2, 0, 0] };
  const POSES = {
    1: { // braços abertos, recebendo
      juntas: { ombroE: [-0.25, 0, 0.95], ombroD: [-0.25, 0, -0.95], cotoveloE: [-0.2, 0, 0.75], cotoveloD: [-0.2, 0, -0.75], maoE: [0, 0, 0.4], maoD: [0, 0, -0.4], cabeca: [-0.05, 0, 0.06] },
      rosto: { olhos: 0.25, sorriso: 1, boca: "aberta", sobeSobrancelha: 0.02 },
    },
    2: { // apontando para o alto, mão na cintura
      juntas: { ombroD: [-0.25, 0, -2.25], cotoveloD: [0, 0, -0.05], ombroE: [0.2, 0, 0.75], cotoveloE: [-0.4, 0, -1.9], tronco: [0, -0.15, 0], cabeca: [-0.1, -0.35, -0.08] },
      rotRoot: [0, 0.25, 0],
      rosto: { olhos: 0.1, sorriso: 0.3, boca: "sorriso", sobrancelha: -0.1 },
    },
    3: { // dormindo sentado, abraçado à estrela, cabeça apoiada nela
      juntas: { ...SENTA, coxaE: [-1.45, 0, -0.35], coxaD: [-1.45, 0, 0.3], joelhoE: [1.2, 0, 0], joelhoD: [1.0, 0, 0], tronco: [0.42, 0, 0.12],
        ombroE: [-1.15, 0, -0.55], ombroD: [-1.15, 0, 0.55], cotoveloE: [-0.5, 0, -0.9], cotoveloD: [-0.5, 0, 0.9], cabeca: [0.35, 0.2, 0.4] },
      rotRoot: [0, -0.4, 0], camAlt: 0.35,
      rosto: { olhos: 1, sorriso: 0.25, boca: "sorriso" },
      props: () => { const st = estrela(1.05); st.position.set(0.15, 1.05, 1.45); st.rotation.set(-0.35, 0.25, 0.25); P.rig.tronco.add(st); },
      extra: () => { const z = texto("z z Z", "#1b1b22", 150); z.scale.multiplyScalar(1.5); z.position.set(1.4, 4.4, 0.6); cena.add(z); },
    },
    4: { // sentado, coçando a cabeça, confuso
      juntas: { ...SENTA, ombroD: [-0.6, 0, -2.4], cotoveloD: [-1.3, 0, -1.0], ombroE: [-0.5, 0, 0.2], cotoveloE: [-0.9, 0, 0], cabeca: [0.12, 0, -0.15], tronco: [0.08, 0, 0] },
      rotRoot: [0, -0.3, 0], camAlt: 0.4,
      rosto: { olhos: 0.15, sorriso: 0, boca: "preocupado", sobrancelha: 0.35 },
      props: () => { naCabeca(boneBrasil(), [0, 0.42, -0.02], [-0.18, 0, 0]); },
      extra: () => { const q = texto("?", "#1b1b22", 230); q.scale.multiplyScalar(1.7); q.position.set(1.3, 4.7, 0.4); cena.add(q); },
    },
    5: { // sentado comendo pizza
      juntas: { ...SENTA, ombroD: [-1.3, 0, -0.35], cotoveloD: [-1.6, 0, 0.35], ombroE: [-0.9, 0, 0.3], cotoveloE: [-0.6, 0, 0], cabeca: [-0.06, 0, 0.08] },
      rosto: { olhos: 1, sorriso: 1, boca: "comendo" },
      props: () => { const pz = pizza(); pz.scale.setScalar(1.35); naMao("maoD", pz, [0.15, -0.25, 0.3], [0.9, 0.2, 2.9]); const gf = garfo(); gf.scale.setScalar(1.3); naMao("maoE", gf, [0, -0.25, 0.22], [1.2, 0, 0.3]); },
      rotRoot: [0, -0.3, 0], camAlt: 0.4,
    },
    6: { // pulando, comemorando
      juntas: { ombroE: [0, 0, 2.6], ombroD: [0, 0, -2.6], cotoveloE: [0, 0, 0.35], cotoveloD: [0, 0, -0.35], coxaE: [-0.5, 0, -0.1], coxaD: [-0.3, 0, 0.15], joelhoE: [1.1, 0, 0], joelhoD: [0.9, 0, 0], cabeca: [-0.15, 0, 0] },
      altura: 0.9,
      rosto: { olhos: 1, sorriso: 1, boca: "aberta", sobeSobrancelha: 0.04 },
      extra: () => cena.add(confete()),
    },
    7: { // sentado acenando, boné azul
      juntas: { ...SENTA, ombroD: [0.1, 0, -2.5], cotoveloD: [0, 0, 0.5], ombroE: [0.5, 0, 0.45], cotoveloE: [0, 0, 0], tronco: [-0.2, 0, 0.05], cabeca: [-0.05, 0, -0.1] },
      rotRoot: [0, -0.35, 0], camAlt: 0.4,
      rosto: { olhos: 0.3, sorriso: 1, boca: "aberta" },
      props: () => { naCabeca(boneAzul(), [0, 0.42, -0.02], [-0.18, 0, 0]); },
    },
    8: { // sentado lendo "História"
      juntas: { ...SENTA, ombroD: [-0.75, 0, -0.25], cotoveloD: [-1.0, 0, 0.55], ombroE: [-0.75, 0, 0.25], cotoveloE: [-1.0, 0, -0.55], cabeca: [0.3, 0, 0] },
      rosto: { olhos: 0.55, sorriso: 0.5, boca: "sorriso" },
      props: () => { const lv = livro(); lv.scale.setScalar(1.25); lv.position.set(0, 0.95, 1.55); lv.rotation.set(-0.25, 0, 0); P.rig.tronco.add(lv); },
      rotRoot: [0, -0.3, 0], camAlt: 0.4,
    },
  };

  const pose = POSES[N];
  if (pose.props) pose.props();
  P.root.traverse((o) => { if (o.isMesh) o.castShadow = true; });
  P.posar(pose);
  if (pose.extra) pose.extra();

  // enquadra o personagem: câmera 3/4 levemente de cima
  const caixa = new THREE.Box3().setFromObject(P.root);
  const centro = caixa.getCenter(new THREE.Vector3());
  const tam = caixa.getSize(new THREE.Vector3());
  const raio = Math.max(tam.y * 0.52, tam.x * 0.52, 2.7);
  const dist = raio / Math.tan((cam.fov * Math.PI) / 360) * 1.08;
  const a = 0.38 + ANG;
  cam.position.set(centro.x + Math.sin(a) * dist, centro.y + dist * (pose.camAlt ?? 0.18), centro.z + Math.cos(a) * dist);
  cam.lookAt(centro.x, centro.y + (pose.extra ? 0.35 : 0), centro.z);
  renderer.render(cena, cam);
  window.__pronto = true;
})();
