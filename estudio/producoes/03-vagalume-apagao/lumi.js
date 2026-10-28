/*
 * Lumi — vagalume de pijama (procedural). Unidade: cm (Lumi ≈ 1,5 cm em pé).
 * window.criarLumi(THREE) → { root, rig, rosto(ex), bunda, luz, asas(t,voando) }
 * Origem do root: chão, sob o tórax. Frente: +z.
 */
(function () {
  function texturaPijama() {
    const c = document.createElement("canvas"); c.width = c.height = 256;
    const g = c.getContext("2d");
    g.fillStyle = "#24386b"; g.fillRect(0, 0, 256, 256);
    g.fillStyle = "#ffd34d";
    const est = (x, y, r) => { g.beginPath(); for (let i = 0; i < 10; i++) { const a = -Math.PI / 2 + (i * Math.PI) / 5, rr = i % 2 ? r * 0.45 : r; g.lineTo(x + Math.cos(a) * rr, y + Math.sin(a) * rr); } g.fill(); };
    for (const [x, y] of [[40, 50], [150, 30], [220, 120], [90, 150], [180, 210], [30, 220], [120, 90]]) est(x, y, 13);
    return c;
  }

  function criarLumi(THREE) {
    const tex = new THREE.CanvasTexture(texturaPijama()); tex.colorSpace = THREE.SRGBColorSpace; tex.wrapS = tex.wrapT = THREE.RepeatWrapping; tex.repeat.set(2, 2);
    const quitina = new THREE.MeshPhysicalMaterial({ color: "#4a2f22", roughness: 0.35, clearcoat: 0.6, clearcoatRoughness: 0.3, sheen: 0.4, sheenColor: new THREE.Color("#8a5a40") });
    const pijama = new THREE.MeshPhysicalMaterial({ map: tex, roughness: 0.85, sheen: 0.6, sheenColor: new THREE.Color("#5d78c8") });
    const branco = new THREE.MeshPhysicalMaterial({ color: "#fbf8f1", roughness: 0.15, clearcoat: 1 });
    const ambar = new THREE.MeshPhysicalMaterial({ color: "#f2a93b", roughness: 0.1, clearcoat: 1 });
    const preto = new THREE.MeshPhysicalMaterial({ color: "#0b0706", roughness: 0.1, clearcoat: 1 });
    const brilho = new THREE.MeshBasicMaterial({ color: "#ffffff" });
    const boca = new THREE.MeshStandardMaterial({ color: "#1a0d0a", roughness: 0.6 });
    const amarelo = new THREE.MeshStandardMaterial({ color: "#ffd34d", roughness: 0.6 });
    const asaMat = new THREE.MeshPhysicalMaterial({ color: "#d9ecff", transparent: true, opacity: 0.38, roughness: 0.1, iridescence: 1, iridescenceIOR: 1.6, side: THREE.DoubleSide, depthWrite: false });
    const luzMat = new THREE.MeshPhysicalMaterial({ color: "#d8ff5a", emissive: new THREE.Color("#e9ff7a"), emissiveIntensity: 0.35, roughness: 0.25, transmission: 0.2, thickness: 0.3 });

    const G = (x = 0, y = 0, z = 0) => { const g = new THREE.Group(); g.position.set(x, y, z); return g; };
    const esf = (r, m, s = 32) => new THREE.Mesh(new THREE.SphereGeometry(r, s, Math.round(s * 0.75)), m);
    const cap = (r, l, m) => new THREE.Mesh(new THREE.CapsuleGeometry(r, l, 6, 12), m);

    const root = G(); const rig = {};
    rig.corpo = G(0, 0, 0); root.add(rig.corpo);
    // tórax de pijama
    const torax = esf(0.29, pijama); torax.scale.set(1, 1.05, 0.95); torax.position.y = 0.42; rig.corpo.add(torax);
    const barra = new THREE.Mesh(new THREE.TorusGeometry(0.24, 0.035, 8, 28), pijama); barra.rotation.x = Math.PI / 2; barra.position.y = 0.2; rig.corpo.add(barra);
    // abdômen que brilha (atrás e um pouco abaixo)
    rig.bunda = G(0, 0.34, -0.3); rig.corpo.add(rig.bunda);
    const abd = esf(0.27, luzMat, 40); abd.scale.set(0.95, 0.9, 1.35); abd.rotation.x = 0.35; rig.bunda.add(abd);
    for (let i = 0; i < 3; i++) { const anel = new THREE.Mesh(new THREE.TorusGeometry(0.235 - i * 0.03, 0.012, 6, 28), quitina); anel.position.z = 0.05 - i * 0.14; anel.scale.y = 0.95; rig.bunda.add(anel); }
    const luz = new THREE.PointLight("#e9ff7a", 0, 12, 1.6); luz.position.set(0, 0, -0.1); rig.bunda.add(luz);

    // pernas (4) e braços (2)
    rig.pernas = [];
    for (const [x, z] of [[0.16, 0.08], [-0.16, 0.08], [0.17, -0.12], [-0.17, -0.12]]) {
      const p = G(x, 0.26, z); rig.corpo.add(p);
      const c1 = cap(0.032, 0.16, quitina); c1.position.y = -0.1; c1.rotation.z = Math.sign(x) * 0.5; p.add(c1);
      const pe = esf(0.045, quitina, 12); pe.position.set(Math.sign(x) * 0.1, -0.22, 0); p.add(pe);
      rig.pernas.push(p);
    }
    for (const s of [1, -1]) {
      const om = G(s * 0.24, 0.5, 0.1); rig.corpo.add(om);
      const b1 = cap(0.035, 0.14, pijama); b1.position.y = -0.1; om.add(b1);
      const cot = G(0, -0.2, 0); om.add(cot);
      const b2 = cap(0.03, 0.12, quitina); b2.position.y = -0.09; cot.add(b2);
      const mao = esf(0.055, quitina, 14); mao.position.y = -0.19; cot.add(mao);
      rig[s > 0 ? "ombroE" : "ombroD"] = om; rig[s > 0 ? "cotoveloE" : "cotoveloD"] = cot;
    }
    // asas recolhidas nas costas
    rig.asas = [];
    for (const s of [1, -1]) {
      const sh = new THREE.Shape(); sh.absellipse(0, -0.3, 0.13, 0.34, 0, Math.PI * 2);
      const a = G(s * 0.07, 0.62, -0.15); const m = new THREE.Mesh(new THREE.ShapeGeometry(sh, 24), asaMat); a.add(m);
      a.rotation.set(-0.55, s * 0.25, s * 0.12); rig.corpo.add(a); rig.asas.push({ g: a, s });
    }

    // cabeça
    rig.cabeca = G(0, 0.78, 0.05); rig.corpo.add(rig.cabeca);
    const H = rig.cabeca;
    const cranio = esf(0.42, quitina, 48); cranio.scale.set(1.08, 0.98, 0.95); H.add(cranio);
    const olhos = [];
    for (const s of [1, -1]) {
      const og = G(s * 0.18, 0.04, 0.3); H.add(og);
      const sc = esf(0.165, branco, 32); sc.scale.set(1, 1.25, 0.62); og.add(sc);
      const ir = G(0, 0, 0.075); og.add(ir);
      const iris = esf(0.11, ambar, 24); iris.scale.set(1, 1.2, 0.45); ir.add(iris);
      const pup = esf(0.076, preto, 20); pup.scale.set(1, 1.2, 0.4); pup.position.z = 0.03; ir.add(pup);
      const b1 = esf(0.026, brilho, 10); b1.position.set(0.035, 0.05, 0.055); ir.add(b1);
      const b2 = esf(0.012, brilho, 8); b2.position.set(-0.03, -0.035, 0.055); ir.add(b2);
      const cima = new THREE.Mesh(new THREE.SphereGeometry(0.175, 28, 14, 0, Math.PI * 2, 0, Math.PI / 2), quitina); cima.scale.set(1, 1.25, 0.66); og.add(cima);
      const baixo = new THREE.Mesh(new THREE.SphereGeometry(0.173, 28, 14, 0, Math.PI * 2, Math.PI / 2, Math.PI / 2), quitina); baixo.scale.set(1, 1.25, 0.66); og.add(baixo);
      olhos.push({ s, og, ir, pup, cima, baixo });
    }
    // boca: sorriso (arco), aberta (O), riso (meia-lua), reta, amarela
    const bocaG = G(0, -0.2, 0.37); H.add(bocaG);
    const arco = new THREE.Mesh(new THREE.TorusGeometry(0.1, 0.018, 8, 24, Math.PI), boca); arco.rotation.z = Math.PI; bocaG.add(arco);
    const oBoca = esf(0.07, boca, 20); oBoca.scale.set(1, 1.2, 0.3); bocaG.add(oBoca);
    const riso = new THREE.Mesh(new THREE.CircleGeometry(0.13, 28, Math.PI, Math.PI), boca); riso.position.z = 0.012; bocaG.add(riso);
    const reta = new THREE.Mesh(new THREE.BoxGeometry(0.16, 0.022, 0.02), boca); bocaG.add(reta);
    // bochechas (infladas no esforço)
    const boch = [];
    for (const s of [1, -1]) { const b = esf(0.12, quitina, 16); b.position.set(s * 0.24, -0.16, 0.22); b.scale.setScalar(0.01); H.add(b); boch.push(b); }
    // antenas
    rig.antenas = [];
    for (const s of [1, -1]) {
      const ag = G(s * 0.12, 0.34, 0.05); H.add(ag);
      const curva = new THREE.QuadraticBezierCurve3(new THREE.Vector3(0, 0, 0), new THREE.Vector3(s * 0.05, 0.35, 0.05), new THREE.Vector3(s * 0.22, 0.55, 0.22));
      ag.add(new THREE.Mesh(new THREE.TubeGeometry(curva, 16, 0.016, 6), quitina));
      const ponta = esf(0.045, quitina, 12); ponta.position.set(s * 0.22, 0.55, 0.22); ag.add(ponta);
      rig.antenas.push({ g: ag, s });
    }
    // touca com pompom
    const touca = G(0.02, 0.24, -0.05); touca.rotation.set(-0.45, 0, 0.3); H.add(touca);
    const cone = new THREE.Mesh(new THREE.ConeGeometry(0.36, 0.62, 28, 1, true), pijama); cone.position.y = 0.3; touca.add(cone);
    const aba = new THREE.Mesh(new THREE.TorusGeometry(0.34, 0.045, 10, 30), pijama); aba.rotation.x = Math.PI / 2; aba.position.y = 0.0; touca.add(aba);
    const pom = esf(0.085, amarelo, 16); pom.position.y = 0.62; touca.add(pom);

    root.traverse((o) => { if (o.isMesh) { o.castShadow = true; o.receiveShadow = true; } });

    function rosto(ex = {}) {
      const fe = ex.olhoE ?? ex.olhos ?? 0, fd = ex.olhoD ?? ex.olhos ?? 0, lb = ex.baixo ?? 0;
      for (const o of olhos) {
        const f = o.s > 0 ? fe : fd;
        o.cima.rotation.x = -0.95 + f * 2.35; // 0 aberto → 1 fechado
        o.baixo.rotation.x = 0.95 - lb * 1.25;
        const p = ex.pupila ?? 1; o.pup.scale.set(p, p * 1.2, 0.4);
        o.ir.position.x = (ex.olharX || 0) * 0.05; o.ir.position.y = (ex.olharY || 0) * 0.05;
      }
      const b = ex.boca || "reta";
      arco.visible = b === "sorriso" || b === "triste" || b === "amarelo";
      arco.rotation.z = b === "triste" ? 0 : Math.PI;
      arco.position.y = b === "triste" ? -0.07 : 0;
      arco.scale.setScalar(b === "amarelo" ? 0.7 : 1);
      arco.position.x = b === "amarelo" ? 0.05 : 0;
      oBoca.visible = b === "O"; oBoca.scale.set(1 + (ex.grito || 0) * 0.6, 1.2 + (ex.grito || 0), 0.3);
      riso.visible = b === "riso";
      reta.visible = b === "reta" || b === "esforco";
      reta.scale.x = b === "esforco" ? 0.6 : 1;
      const bc = ex.bochecha || 0; for (const x of boch) x.scale.setScalar(0.01 + bc * 0.9);
      cranio.scale.x = 1.08 + bc * 0.08;
      const ant = ex.antenas ?? 0; // + eriçadas, - murchas
      for (const a of rig.antenas) a.g.rotation.set(-ant * 0.4, 0, -a.s * ant * 0.35 + (ex.tremor ? Math.sin(ex.tremor * 60) * 0.12 : 0));
    }
    function asas(t, voando) {
      for (const a of rig.asas) {
        if (voando) { const b = Math.sin(t * 2 * Math.PI * 22); a.g.rotation.set(-0.2, a.s * (0.9 + b * 0.7), a.s * (0.6 + b * 0.3)); }
        else a.g.rotation.set(-0.55, a.s * 0.25, a.s * 0.12);
      }
    }
    function neutro() {
      for (const k of ["ombroE", "ombroD", "cotoveloE", "cotoveloD", "cabeca", "corpo"]) rig[k].rotation.set(0, 0, 0);
      rig.ombroE.rotation.z = 0.25; rig.ombroD.rotation.z = -0.25;
      for (const p of rig.pernas) p.rotation.set(0, 0, 0);
      rig.corpo.position.set(0, 0, 0);
    }
    rosto({});
    return { root, rig, rosto, asas, neutro, luz, luzMat };
  }
  window.criarLumi = criarLumi;
})();
