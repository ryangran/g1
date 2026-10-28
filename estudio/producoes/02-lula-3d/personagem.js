/*
 * Personagem 3D caricato: presidente de cabelo e barba grisalhos, terno escuro,
 * gravata vermelha e faixa presidencial. Construído só com geometria procedural
 * (sem modelo externo) e um rig hierárquico simples: quadril → tronco → cabeça,
 * ombro → cotovelo → mão, quadril → joelho → pé.
 *
 * window.Caricatura.criar(THREE) → { root, rig, rosto, props, posar(pose) }
 */
(function () {
  function criar(THREE) {
    const E = window.Estudio3D;
    const rnd = E.aleatorio(1988);

    // ---------- materiais ----------
    const pele = new THREE.MeshPhysicalMaterial({ color: "#efb999", roughness: 0.55, sheen: 0.6, sheenColor: new THREE.Color("#ff9e88"), sheenRoughness: 0.5, clearcoat: 0.05 });
    const peleNariz = pele.clone(); peleNariz.color = new THREE.Color("#e99a88");
    const cabelo = (k) => new THREE.MeshStandardMaterial({ color: new THREE.Color().setHSL(0.08, 0.04, 0.72 + k * 0.12), roughness: 0.95 });
    const cabelos = [0, 0.4, 0.8, 1].map(cabelo);
    const terno = new THREE.MeshPhysicalMaterial({ color: "#2d313b", roughness: 0.72, sheen: 0.4, sheenColor: new THREE.Color("#5a6070") });
    const lapela = new THREE.MeshStandardMaterial({ color: "#23262e", roughness: 0.6 });
    const camisa = new THREE.MeshStandardMaterial({ color: "#f3f1ec", roughness: 0.7 });
    const gravata = new THREE.MeshPhysicalMaterial({ color: "#b3161b", roughness: 0.35, clearcoat: 0.3 });
    const verde = new THREE.MeshPhysicalMaterial({ color: "#159447", roughness: 0.45, sheen: 0.5 });
    const amarelo = new THREE.MeshPhysicalMaterial({ color: "#f5c518", roughness: 0.45, sheen: 0.5 });
    const sapato = new THREE.MeshPhysicalMaterial({ color: "#121316", roughness: 0.25, clearcoat: 0.8 });
    const escuro = new THREE.MeshStandardMaterial({ color: "#1a1112", roughness: 0.5 });
    const olhoBranco = new THREE.MeshPhysicalMaterial({ color: "#f4f1ec", roughness: 0.15, clearcoat: 1 });
    const iris = new THREE.MeshPhysicalMaterial({ color: "#3b2416", roughness: 0.1, clearcoat: 1 });
    const rubor = new THREE.MeshBasicMaterial({ color: "#ff8f8f", transparent: true, opacity: 0.22, depthWrite: false });

    const esfera = (r, mat, seg = 32) => new THREE.Mesh(new THREE.SphereGeometry(r, seg, Math.round(seg * 0.75)), mat);
    const capsula = (r, l, mat) => new THREE.Mesh(new THREE.CapsuleGeometry(r, l, 8, 24), mat);
    const grupo = (x = 0, y = 0, z = 0) => { const g = new THREE.Group(); g.position.set(x, y, z); return g; };

    const root = grupo();
    const rig = {};

    // ---------- pernas ----------
    rig.quadril = grupo(0, 1.95, 0); root.add(rig.quadril);
    const bacia = esfera(0.9, terno); bacia.scale.set(1.05, 0.55, 0.78); bacia.position.y = 0.05; rig.quadril.add(bacia);
    for (const s of [1, -1]) {
      const coxa = grupo(s * 0.45, 0, 0); rig.quadril.add(coxa);
      const mc = capsula(0.36, 0.7, terno); mc.position.y = -0.5; coxa.add(mc);
      const joelho = grupo(0, -1.0, 0); coxa.add(joelho);
      const ms = capsula(0.32, 0.55, terno); ms.position.y = -0.45; joelho.add(ms);
      const pe = grupo(0, -0.92, 0); joelho.add(pe);
      const sp = new THREE.Mesh(new THREE.RoundedBoxGeometry(0.5, 0.3, 0.8, 4, 0.14), sapato); sp.position.set(0, -0.04, 0.16); pe.add(sp);
      rig[s > 0 ? "coxaE" : "coxaD"] = coxa; rig[s > 0 ? "joelhoE" : "joelhoD"] = joelho; rig[s > 0 ? "peE" : "peD"] = pe;
    }

    // ---------- tronco ----------
    rig.tronco = grupo(0, 0.05, 0); rig.quadril.add(rig.tronco);
    const perfil = [[0, 0], [0.86, 0.05], [0.99, 0.4], [1.02, 0.9], [0.97, 1.4], [0.8, 1.72], [0.4, 1.93], [0, 1.96]].map(([r, y]) => new THREE.Vector2(r, y));
    const jaqueta = new THREE.Mesh(new THREE.LatheGeometry(perfil, 48), terno); jaqueta.scale.z = 0.78; rig.tronco.add(jaqueta);
    const frente = 0.79; // z da superfície frontal do peito (aprox.)
    // o peito recua para cima: plano inclinado que acompanha a jaqueta entre y 1,05 e 1,9
    const PEITO_ANG = -0.37, PEITO_Z = 1.21;
    // camisa em V, lapelas, gravata
    const v = new THREE.Shape(); v.moveTo(-0.42, 1.88); v.lineTo(0.42, 1.88); v.lineTo(0, 1.05); v.closePath();
    const mv = new THREE.Mesh(new THREE.ShapeGeometry(v), camisa); mv.position.z = PEITO_Z; mv.rotation.x = PEITO_ANG; rig.tronco.add(mv);
    for (const s of [1, -1]) {
      const l = new THREE.Shape(); l.moveTo(s * 0.42, 1.9); l.lineTo(s * 0.62, 1.7); l.lineTo(s * 0.2, 0.95); l.lineTo(0, 1.05); l.closePath();
      const ml = new THREE.Mesh(new THREE.ShapeGeometry(l), lapela); ml.position.z = PEITO_Z + 0.012; ml.rotation.x = PEITO_ANG; rig.tronco.add(ml);
    }
    const g = new THREE.Shape(); g.moveTo(-0.09, 1.82); g.lineTo(0.09, 1.82); g.lineTo(0.06, 1.72); g.lineTo(0.15, 1.2); g.lineTo(0, 1.06); g.lineTo(-0.15, 1.2); g.lineTo(-0.06, 1.72); g.closePath();
    const mg = new THREE.Mesh(new THREE.ExtrudeGeometry(g, { depth: 0.04, bevelEnabled: true, bevelSize: 0.015, bevelThickness: 0.015, bevelSegments: 2 }), gravata);
    mg.position.z = PEITO_Z + 0.004; mg.rotation.x = PEITO_ANG; rig.tronco.add(mg);
    // botões
    for (const y of [0.55, 0.85]) { const b = esfera(0.045, lapela, 12); b.position.set(0, y, frente + 0.02); rig.tronco.add(b); }

    // faixa presidencial: elipse inclinada do ombro direito ao quadril esquerdo
    function fita(largura, folga, mat) {
      const pos = [], idx = [];
      const n = 96;
      for (let i = 0; i <= n; i++) {
        const a = (i / n) * Math.PI * 2;
        const x = Math.cos(a) * (1.04 + folga), z = Math.sin(a) * (0.83 + folga);
        pos.push(x, -largura / 2, z, x, largura / 2, z);
        if (i < n) { const k = i * 2; idx.push(k, k + 1, k + 2, k + 1, k + 3, k + 2); }
      }
      const geo = new THREE.BufferGeometry();
      geo.setAttribute("position", new THREE.Float32BufferAttribute(pos, 3)); geo.setIndex(idx); geo.computeVertexNormals();
      const m = mat.clone(); m.side = THREE.DoubleSide;
      return new THREE.Mesh(geo, m);
    }
    const sash = grupo(0, 1.02, 0.0); sash.rotation.z = 0.62;
    sash.add(fita(0.42, 0.1, verde), fita(0.13, 0.115, amarelo)); rig.tronco.add(sash);

    // ---------- braços ----------
    for (const s of [1, -1]) {
      const ombro = grupo(s * 0.98, 1.62, 0); rig.tronco.add(ombro);
      const bo = esfera(0.36, terno); bo.scale.set(1, 0.9, 0.9); ombro.add(bo);
      const mb = capsula(0.3, 0.75, terno); mb.position.y = -0.55; ombro.add(mb);
      const cotovelo = grupo(0, -1.1, 0); ombro.add(cotovelo);
      const ma = capsula(0.27, 0.7, terno); ma.position.y = -0.5; cotovelo.add(ma);
      const punho = new THREE.Mesh(new THREE.TorusGeometry(0.22, 0.06, 10, 24), camisa); punho.rotation.x = Math.PI / 2; punho.position.y = -0.98; cotovelo.add(punho);
      const mao = grupo(0, -1.12, 0); cotovelo.add(mao);
      const palma = esfera(0.27, pele); palma.scale.set(0.95, 1.1, 0.7); palma.position.y = -0.12; mao.add(palma);
      const polegar = capsula(0.085, 0.16, pele); polegar.position.set(-s * 0.0, -0.05, 0.2); polegar.rotation.x = 0.9; mao.add(polegar);
      rig[s > 0 ? "ombroE" : "ombroD"] = ombro; rig[s > 0 ? "cotoveloE" : "cotoveloD"] = cotovelo; rig[s > 0 ? "maoE" : "maoD"] = mao;
    }

    // ---------- cabeça ----------
    rig.pescoco = grupo(0, 1.9, 0); rig.tronco.add(rig.pescoco);
    const colar = new THREE.Mesh(new THREE.CylinderGeometry(0.42, 0.48, 0.2, 24), camisa); colar.position.y = 0.0; rig.pescoco.add(colar);
    rig.cabeca = grupo(0, 0.95, 0.05); rig.pescoco.add(rig.cabeca);
    const H = rig.cabeca;
    const cranio = esfera(1, pele, 48); cranio.scale.set(0.96, 1.05, 0.94); H.add(cranio);
    for (const s of [1, -1]) {
      const o = esfera(0.3, pele); o.scale.set(0.45, 0.95, 0.6); o.position.set(s * 0.93, 0.02, -0.05); H.add(o);
      const r = esfera(0.2, rubor, 20); r.scale.set(1, 0.7, 0.3); r.position.set(s * 0.5, -0.12, 0.8); H.add(r);
    }
    const nariz = esfera(0.21, peleNariz); nariz.scale.set(1.05, 0.92, 0.95); nariz.position.set(0, -0.04, 0.97); H.add(nariz);
    for (const s of [1, -1]) { const n = esfera(0.11, peleNariz, 16); n.position.set(s * 0.15, -0.12, 0.9); H.add(n); }

    // olhos com pálpebras (0 aberto → 1 fechado) e pálpebra de baixo (sorriso)
    const rosto = { olhos: [], sobrancelhas: [], boca: {} };
    for (const s of [1, -1]) {
      const og = grupo(s * 0.34, 0.15, 0.8); H.add(og);
      const bola = esfera(0.13, olhoBranco, 24); bola.scale.z = 0.8; og.add(bola);
      const ir = esfera(0.082, iris, 20); ir.position.z = 0.075; ir.scale.z = 0.6; og.add(ir);
      const brilho = esfera(0.022, new THREE.MeshBasicMaterial({ color: "#ffffff" }), 8); brilho.position.set(0.03, 0.04, 0.125); og.add(brilho);
      const cima = new THREE.Mesh(new THREE.SphereGeometry(0.145, 24, 12, 0, Math.PI * 2, 0, Math.PI / 2), pele); og.add(cima);
      const baixo = new THREE.Mesh(new THREE.SphereGeometry(0.143, 24, 12, 0, Math.PI * 2, Math.PI / 2, Math.PI / 2), pele); og.add(baixo);
      const sob = capsula(0.05, 0.2, cabelos[3]); sob.rotation.z = Math.PI / 2; sob.position.set(s * 0.34, 0.37, 0.86); H.add(sob);
      rosto.olhos.push({ s, cima, baixo }); rosto.sobrancelhas.push({ s, m: sob });
    }

    // tufos de cabelo e barba: pontos de Fibonacci na casca da cabeça, com jitter de seed fixa
    function casca(n, aceita, raio, tam, mats) {
      const out = grupo();
      for (let i = 0; i < n; i++) {
        const y = 1 - (i / (n - 1)) * 2;
        const r = Math.sqrt(1 - y * y);
        const a = i * 2.399963 + rnd() * 0.4;
        const p = new THREE.Vector3(Math.cos(a) * r, y, Math.sin(a) * r);
        if (!aceita(p)) continue;
        const t = tam[0] + rnd() * (tam[1] - tam[0]);
        const m = esfera(t, mats[Math.floor(rnd() * mats.length)], 14);
        m.scale.set(1, 0.8 + rnd() * 0.3, 0.75);
        m.position.copy(p).multiply(new THREE.Vector3(0.96, 1.05, 0.94)).multiplyScalar(raio);
        m.lookAt(0, 0, 0);
        out.add(m);
      }
      return out;
    }
    const tufos = casca(1400, (p) => {
      const testa = p.z > 0.05 && p.y < 0.8; // testa e rosto livres
      const lado = p.y > -0.05 && p.z < 0.3 && Math.abs(p.x) > 0.72; // costeletas acima da orelha
      const nuca = p.z < -0.2 && p.y > -0.45;
      return (p.y > 0.3 && !testa) || lado || nuca;
    }, 1.0, [0.1, 0.17], cabelos);
    H.add(tufos);
    const barba = casca(2200, (p) => {
      const boca = Math.abs(p.x) < 0.27 && p.y > -0.56 && p.y < -0.3 && p.z > 0.6;
      const bochecha = p.z > 0.35 && p.y > -0.3 - (1 - Math.abs(p.x)) * 0.15;
      return p.y < -0.18 && p.z > -0.3 && !boca && !bochecha;
    }, 0.99, [0.075, 0.13], cabelos);
    H.add(barba);
    // bigode
    for (let i = 0; i < 14; i++) {
      const x = -0.36 + (i / 13) * 0.72;
      const m = esfera(0.075 + rnd() * 0.03, cabelos[1 + (i % 3)], 12);
      m.position.set(x, -0.24 - Math.abs(x) * 0.25, 0.92 - Math.abs(x) * 0.25);
      m.scale.set(1.2, 0.75, 0.8); H.add(m);
    }
    // boca: aberta (sorriso), fechada, preocupada, mastigando
    const bocaG = grupo(0, -0.42, 0.9); H.add(bocaG);
    const aberta = new THREE.Mesh(new THREE.CircleGeometry(0.2, 32, Math.PI, Math.PI), escuro); aberta.scale.set(1.1, 0.95, 1); bocaG.add(aberta);
    const dentes = new THREE.Mesh(new THREE.PlaneGeometry(0.34, 0.06), new THREE.MeshStandardMaterial({ color: "#fbfaf5" })); dentes.position.set(0, -0.03, 0.005); bocaG.add(dentes);
    const lingua = esfera(0.09, new THREE.MeshStandardMaterial({ color: "#d9635f" }), 16); lingua.scale.set(1.3, 0.5, 0.4); lingua.position.set(0, -0.15, -0.01); bocaG.add(lingua);
    const fechada = new THREE.Mesh(new THREE.TorusGeometry(0.15, 0.025, 8, 24, Math.PI), escuro); fechada.rotation.z = Math.PI; fechada.position.y = 0.04; bocaG.add(fechada);
    rosto.boca = { aberta, dentes, lingua, fechada };

    // ---------- expressões ----------
    rosto.aplicar = (ex) => {
      const fechar = ex.olhos ?? 0, sorriso = ex.sorriso ?? 0;
      for (const o of rosto.olhos) {
        o.cima.rotation.x = E.lerp(-0.75, 1.5, fechar);
        o.baixo.rotation.x = E.lerp(0.75, -0.25, sorriso);
      }
      const ang = ex.sobrancelha ?? 0; // + preocupado (interno sobe), - bravo
      for (const b of rosto.sobrancelhas) { b.m.rotation.z = Math.PI / 2 - b.s * ang; b.m.position.y = 0.37 + Math.abs(ang) * 0.04 + (ex.sobeSobrancelha || 0); }
      const tipo = ex.boca || "sorriso";
      rosto.boca.aberta.visible = tipo === "aberta" || tipo === "comendo";
      rosto.boca.dentes.visible = tipo === "aberta";
      rosto.boca.lingua.visible = tipo === "aberta";
      rosto.boca.fechada.visible = tipo === "sorriso" || tipo === "preocupado";
      rosto.boca.fechada.rotation.z = tipo === "preocupado" ? 0 : Math.PI;
      rosto.boca.fechada.position.y = tipo === "preocupado" ? -0.08 : 0.04;
      rosto.boca.aberta.scale.set(tipo === "comendo" ? 0.7 : 1.1, tipo === "comendo" ? 0.6 : 0.95, 1);
    };

    // ---------- poses ----------
    const juntas = ["quadril", "tronco", "pescoco", "cabeca", "coxaE", "coxaD", "joelhoE", "joelhoD", "peE", "peD", "ombroE", "ombroD", "cotoveloE", "cotoveloD", "maoE", "maoD"];
    const base = {};
    for (const j of juntas) base[j] = rig[j].position.clone();
    function posar(p) {
      for (const j of juntas) { rig[j].rotation.set(0, 0, 0); rig[j].position.copy(base[j]); }
      // braços caídos levemente afastados por padrão
      rig.ombroE.rotation.z = 0.12; rig.ombroD.rotation.z = -0.12;
      for (const [j, r] of Object.entries(p.juntas || {})) rig[j].rotation.set(r[0] || 0, r[1] || 0, r[2] || 0, r[3] || "XYZ");
      root.rotation.set(...(p.rotRoot || [0, 0, 0]));
      root.position.set(0, 0, 0);
      root.updateMatrixWorld(true);
      const caixa = new THREE.Box3().setFromObject(root);
      root.position.y = -caixa.min.y + (p.altura || 0);
      rosto.aplicar(p.rosto || {});
    }
    return { root, rig, rosto, posar };
  }
  window.Caricatura = { criar };
})();
