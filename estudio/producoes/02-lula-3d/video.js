/*
 * "Um dia na vida" — o personagem passa pelas 8 poses ao longo do dia.
 * Cada quadro é função do tempo: mistura as articulações, a expressão e os
 * acessórios entre a pose atual e a próxima, e pinta o céu da hora do dia.
 */
(function () {
  window.__modoVideo = true;
  const W = 1080, H = 1920;
  const C = window.LulaCena(document.getElementById("palco"), W, H);
  const { THREE, E, renderer, cena, cam, P, POSES, acessorios } = C;

  // roteiro: ordem das poses (um compasso de música por pose)
  const ORDEM = [3, 4, 8, 5, 2, 1, 7, 6];
  const SEGURA = 2.0, TRANS = 0.65, PERIODO = SEGURA + TRANS;
  const DUR = PERIODO * (ORDEM.length - 1) + 3.05;
  const inicio = (i) => i * PERIODO;
  // céu: [topo, base] por pose (06h → 20h)
  const CEU = [
    ["#2b2f5e", "#f2a07b"], ["#4a5f9e", "#ffc89a"], ["#7fb6ec", "#e9f4ff"], ["#5aa8f0", "#dff1ff"],
    ["#6aa6e8", "#fff4d8"], ["#e9773f", "#ffd27a"], ["#4b3a78", "#f08a6b"], ["#120f2e", "#4b2a72"],
  ];

  const JUNTAS = ["quadril", "tronco", "pescoco", "cabeca", "coxaE", "coxaD", "joelhoE", "joelhoD", "peE", "peD", "ombroE", "ombroD", "cotoveloE", "cotoveloD", "maoE", "maoD"];
  const PADRAO = { ombroE: [0, 0, 0.12], ombroD: [0, 0, -0.12] };
  const ang = (pose, j) => (pose.juntas && pose.juntas[j]) || PADRAO[j] || [0, 0, 0];
  const NUM = ["olhos", "sorriso", "sobrancelha", "sobeSobrancelha"];

  C.criarAcessorios(ORDEM);
  // confete cai durante o final
  const confete = acessorios.find((a) => a.pose === 6 && a.obj.isGroup && a.obj.children.length > 20);
  if (confete) confete.obj.children.forEach((c) => (c.userData.y0 = c.position.y));

  // pré-calcula, por pose: altura do chão, rotação do corpo e enquadramento
  const info = {};
  for (const n of ORDEM) {
    for (const a of acessorios) a.obj.visible = a.pose === n;
    P.posar(POSES[n]);
    info[n] = { y: P.root.position.y, rot: P.root.rotation.toArray().slice(0, 3), quadro: C.enquadrar(POSES[n], W / H) };
  }

  const cor = new THREE.Color(), cor2 = new THREE.Color();
  const ceuEl = document.getElementById("ceu");
  function mixCor(a, b, k) { return cor.set(a).lerp(cor2.set(b), k).getStyle(); }

  function renderAt(t) {
    t = E.clamp(t, 0, DUR - 1e-3);
    let i = Math.min(ORDEM.length - 1, Math.floor(t / PERIODO));
    const local = t - inicio(i);
    let k = 0;
    if (i < ORDEM.length - 1 && local > SEGURA) k = E.ease.inOut((local - SEGURA) / TRANS);
    const a = ORDEM[i], b = ORDEM[Math.min(i + 1, ORDEM.length - 1)];
    const pa = POSES[a], pb = POSES[b];

    // articulações misturadas
    for (const j of JUNTAS) {
      const ra = ang(pa, j), rb = ang(pb, j);
      P.rig[j].rotation.set(E.lerp(ra[0] || 0, rb[0] || 0, k), E.lerp(ra[1] || 0, rb[1] || 0, k), E.lerp(ra[2] || 0, rb[2] || 0, k));
    }
    // vida: respiração, cabeça, aceno, mastigar, pulo
    const resp = Math.sin((t / 3.1) * Math.PI * 2);
    P.rig.tronco.rotation.x += 0.025 * resp * (a === 3 ? 2 : 1);
    P.rig.cabeca.rotation.z += 0.04 * Math.sin(t * 1.3);
    const wA = 1 - k, wB = k;
    const peso = (n) => (a === n ? wA : 0) + (b === n ? wB : 0);
    P.rig.cotoveloD.rotation.z += 0.45 * Math.sin(t * 2 * Math.PI * 1.8) * peso(7);
    P.rig.maoD.rotation.z += 0.3 * Math.sin(t * 2 * Math.PI * 1.8 + 0.6) * peso(7);
    P.rig.ombroD.rotation.x += 0.08 * Math.sin(t * 2 * Math.PI * 1.6) * peso(5);
    P.rig.ombroE.rotation.z += 0.12 * Math.sin(t * 2 * Math.PI * 0.9) * peso(1);
    P.rig.ombroD.rotation.z -= 0.12 * Math.sin(t * 2 * Math.PI * 0.9) * peso(1);
    P.rig.cotoveloD.rotation.x += 0.25 * Math.sin(t * 2 * Math.PI * 2.4) * peso(4); // coça a cabeça

    // corpo: chão e giro
    const ra = info[a].rot, rb = info[b].rot;
    P.root.rotation.set(E.lerp(ra[0], rb[0], k), E.lerp(ra[1], rb[1], k), E.lerp(ra[2], rb[2], k));
    let y = E.lerp(info[a].y, info[b].y, k);
    if (a === 6) y += -0.9 + 1.0 * Math.abs(Math.sin(((t - inicio(i)) / 0.62) * Math.PI)); // pulos no ritmo
    P.root.position.set(0, y, 0);

    // expressão misturada + piscadas
    const ex = {};
    for (const n of NUM) ex[n] = E.lerp((pa.rosto || {})[n] || 0, (pb.rosto || {})[n] || 0, k);
    ex.boca = k < 0.5 ? (pa.rosto || {}).boca : (pb.rosto || {}).boca;
    const fase = (t + 0.7) % 3.3;
    if (ex.olhos < 0.6 && fase < 0.13) ex.olhos = 1;
    P.rosto.aplicar(ex);
    if (ex.boca === "comendo") P.rosto.boca.aberta.scale.y = 0.35 + 0.35 * Math.abs(Math.sin(t * 9));

    // acessórios entram e saem com escala elástica
    for (const ac of acessorios) {
      const w = peso(ac.pose);
      ac.obj.visible = w > 0.02;
      const s = w >= 1 ? 1 : E.ease.back(w);
      ac.obj.scale.copy(ac.escala).multiplyScalar(Math.max(0.001, s));
    }
    // "zzz" sobe, "?" balança, confete cai
    for (const ac of acessorios) {
      if (ac.obj.isSprite && ac.pose === 3) { ac.obj.position.y = 4.4 + ((t % 1.6) / 1.6) * 0.5; ac.obj.material.opacity = 0.6 + 0.4 * Math.cos((t % 1.6) * 2); }
      if (ac.obj.isSprite && ac.pose === 4) ac.obj.material.rotation = 0.15 * Math.sin(t * 4);
    }
    if (confete) {
      const t6 = Math.max(0, t - (inicio(ORDEM.length - 1) - 0.3));
      confete.obj.children.forEach((c, n) => {
        c.position.y = c.userData.y0 + 1.2 - ((t6 * (1.1 + (n % 5) * 0.12)) % 6.5);
        c.rotation.x = n + t * (2 + (n % 3)); c.rotation.y = n * 0.7 + t * 1.5;
      });
    }

    // céu da hora
    const ca = CEU[i], cb = CEU[Math.min(i + 1, CEU.length - 1)];
    ceuEl.style.background = `linear-gradient(180deg, ${mixCor(ca[0], cb[0], k)} 0%, ${mixCor(ca[1], cb[1], k)} 78%)`;

    // câmera: enquadramento da pose (misturado), leve órbita, personagem na faixa segura (168–1330 px)
    const qa = info[a].quadro, qb = info[b].quadro;
    const centro = qa.centro.clone().lerp(qb.centro, k);
    // escala constante: o quadro tem sempre ~14,5 unidades de altura (personagem em pé ≈ 6,2)
    const alturaQuadro = 14.5;
    const dist = alturaQuadro / (2 * Math.tan((cam.fov * Math.PI) / 360));
    const alt = E.lerp(qa.alt, qb.alt, k) * 0.6;
    const orbita = 0.38 + 0.22 * Math.sin(t * 0.35);
    cam.position.set(centro.x + Math.sin(orbita) * dist, centro.y + dist * alt, centro.z + Math.cos(orbita) * dist);
    // centro do personagem ~170 px acima do meio da tela (entre o horário e a frase)
    cam.lookAt(centro.x, centro.y - alturaQuadro * (170 / 1920), centro.z);
    renderer.render(cena, cam);
  }

  window.addEventListener("hf-seek", (e) => renderAt(e.detail.time));
  window.__hf = window.__hf || {};
  window.__hf.buildReady = window.__hf.buildReady || {};
  window.__hf.buildReady["um-dia"] = new Promise((resolve) => {
    renderer.compile(cena, cam);
    for (const x of [0.5, 10, 20]) renderAt(x);
    renderAt(window.__timelines["main"].time());
    renderer.getContext().finish();
    resolve();
  });
  window.__umDiaDur = DUR;
})();
