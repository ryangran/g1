/*
 * Estudio3D — motor de animação 3D determinística para HyperFrames.
 *
 * Tudo o que aparece num quadro é função do tempo t (segundos): personagens,
 * expressões, câmera e luz são descritos como trilhas com chaves, e cada
 * quadro é recalculado do zero. Isso permite o render quadro a quadro, fora
 * de ordem, sempre idêntico.
 *
 * Requer window.THREE (assets/lib/three-bundle.js).
 */
(function () {
  const THREE = window.THREE;

  // ---------- easing e trilhas ----------
  const ease = {
    linear: (x) => x,
    in: (x) => x * x * x,
    out: (x) => 1 - Math.pow(1 - x, 3),
    inOut: (x) => (x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2),
    suave: (x) => x * x * (3 - 2 * x),
    back: (x) => {
      const c1 = 1.70158, c3 = c1 + 1;
      return 1 + c3 * Math.pow(x - 1, 3) + c1 * Math.pow(x - 1, 2);
    },
  };
  const clamp = (x, a, b) => Math.min(b, Math.max(a, x));
  const lerp = (a, b, k) => a + (b - a) * k;
  const mix = (a, b, k) =>
    Array.isArray(a) ? a.map((v, i) => lerp(v, b[i], k))
    : typeof a === "object" ? Object.fromEntries(Object.keys(a).map((key) => [key, lerp(a[key], b[key] ?? 0, k)]))
    : lerp(a, b, k);

  /** Trilha com chaves [[t, valor, ease?], ...]: ease da chave vale para o trecho que chega nela. */
  function trilha(chaves) {
    return (t) => {
      if (t <= chaves[0][0]) return chaves[0][1];
      for (let i = 1; i < chaves.length; i++) {
        const [t1, v1, e] = chaves[i];
        if (t < t1) {
          const [t0, v0] = chaves[i - 1];
          const k = (ease[e || "inOut"])((t - t0) / (t1 - t0));
          return mix(v0, v1, k);
        }
      }
      return chaves[chaves.length - 1][1];
    };
  }

  /** PRNG determinístico (mulberry32). */
  function aleatorio(seed) {
    let a = seed >>> 0;
    return () => {
      a |= 0; a = (a + 0x6d2b79f5) | 0;
      let t = Math.imul(a ^ (a >>> 15), 1 | a);
      t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }

  // ---------- carregamento ----------
  function carregarGLTF(url) {
    return new Promise((resolve, reject) => new THREE.GLTFLoader().load(url, resolve, undefined, reject));
  }

  function carregarFonte(nome, url) {
    const f = new FontFace(nome, `url(${url})`);
    return f.load().then((loaded) => { document.fonts.add(loaded); return loaded; });
  }

  // ---------- personagens ----------
  /**
   * Cria um personagem a partir de um glTF com esqueleto.
   * opcoes.cores: { NomeDoMaterial: "#hex" } recolore materiais (mantém o resto igual).
   * opcoes.escala: número.  opcoes.emissivo: { NomeDoMaterial: ["#hex", intensidade] }.
   */
  function criarPersonagem(gltf, opcoes = {}) {
    const root = THREE.SkeletonUtils.clone(gltf.scene);
    const escala = opcoes.escala ?? 1;
    root.scale.setScalar(escala);
    const ossos = {};
    let rosto = null;
    const materiais = {};
    root.traverse((o) => {
      if (o.isBone) ossos[o.name] = o;
      if (o.isMesh) {
        o.castShadow = true;
        o.receiveShadow = true;
        o.frustumCulled = false;
        const m = o.material.clone();
        const nome = o.material.name;
        if (opcoes.cores && opcoes.cores[nome]) m.color = new THREE.Color(opcoes.cores[nome]);
        if (opcoes.emissivo && opcoes.emissivo[nome]) {
          m.emissive = new THREE.Color(opcoes.emissivo[nome][0]);
          m.emissiveIntensity = opcoes.emissivo[nome][1];
        }
        m.roughness = opcoes.rugosidade ?? 0.55;
        m.metalness = opcoes.metal ?? 0.2;
        o.material = m;
        materiais[nome] = materiais[nome] || [];
        materiais[nome].push(m);
        if (o.morphTargetDictionary && Object.keys(o.morphTargetDictionary).length) rosto = o;
      }
    });
    // pose de repouso de cada osso, para somar ajustes sem acumular entre quadros
    const repouso = {};
    for (const [n, b] of Object.entries(ossos)) repouso[n] = b.quaternion.clone();

    const mixer = new THREE.AnimationMixer(root);
    const acoes = {};
    for (const clip of gltf.animations) {
      const a = mixer.clipAction(clip);
      a.play();
      a.setEffectiveWeight(0);
      acoes[clip.name] = a;
    }

    const p = {
      root, ossos, rosto, mixer, acoes, materiais, escala,
      segmentos: [{ t0: -1e9, clip: "Idle" }],
      posicao: () => [0, 0, 0],
      rotacaoY: () => 0,
      expressao: () => ({}),
      ajustes: null, // (t, p, eul) => void: ajustes finos de ossos depois da animação
    };

    /** Segmentos de atuação: [{t0, clip, vel=1, offset=0, loop=true, fade=0.25}] em ordem. */
    p.atuar = (segs) => { p.segmentos = segs; return p; };
    p.mover = (chavesPos, chavesRot) => {
      if (chavesPos) p.posicao = trilha(chavesPos);
      if (chavesRot) p.rotacaoY = trilha(chavesRot);
      return p;
    };
    p.rostoChaves = (chaves) => { p.expressao = trilha(chaves); return p; };

    function tempoDaAcao(seg, t) {
      const a = acoes[seg.clip];
      const dur = a.getClip().duration;
      let x = (seg.offset || 0) + (t - seg.t0) * (seg.vel ?? 1);
      if (seg.loop === false) x = clamp(x, 0, dur - 1e-4);
      else x = ((x % dur) + dur) % dur;
      return x;
    }

    const _e = new THREE.Euler();
    const _q = new THREE.Quaternion();
    /** Gira um osso por (x,y,z) radianos em cima da pose atual. */
    p.girar = (nome, x = 0, y = 0, z = 0) => {
      const b = ossos[nome];
      if (!b) return;
      _e.set(x, y, z, "XYZ");
      _q.setFromEuler(_e);
      b.quaternion.multiply(_q);
    };

    p.aplicar = (t) => {
      for (const [n, b] of Object.entries(ossos)) b.quaternion.copy(repouso[n]);
      for (const a of Object.values(acoes)) a.setEffectiveWeight(0);
      const segs = p.segmentos;
      let i = 0;
      while (i + 1 < segs.length && segs[i + 1].t0 <= t) i++;
      const atual = segs[i];
      const fade = atual.fade ?? 0.25;
      const ant = segs[i - 1];
      let w = 1;
      if (ant && ant.clip !== atual.clip && t < atual.t0 + fade) {
        w = ease.suave((t - atual.t0) / fade);
        const aa = acoes[ant.clip];
        aa.time = tempoDaAcao(ant, t);
        aa.setEffectiveWeight(1 - w);
      }
      const a = acoes[atual.clip];
      a.time = tempoDaAcao(atual, t);
      a.setEffectiveWeight(w);
      mixer.update(0);

      const pos = p.posicao(t);
      p.root.position.set(pos[0], pos[1], pos[2]);
      p.root.rotation.y = p.rotacaoY(t);
      if (rosto) {
        const ex = p.expressao(t);
        const dict = rosto.morphTargetDictionary;
        for (const k of Object.keys(dict)) rosto.morphTargetInfluences[dict[k]] = clamp(ex[k] || 0, 0, 1);
      }
      if (p.ajustes) p.ajustes(t, p);
    };
    return p;
  }

  // ---------- câmera por planos ----------
  /**
   * planos: [{t0, de:{pos:[x,y,z], alvo:[x,y,z], fov}, para:{...}, ease, tremor}] em ordem.
   * Cada plano vai de "de" até "para" durante sua duração (corte seco entre planos).
   */
  function diretorDeCamera(camera, planos, duracaoTotal) {
    const v = new THREE.Vector3();
    return (t) => {
      let i = 0;
      while (i + 1 < planos.length && planos[i + 1].t0 <= t) i++;
      const pl = planos[i];
      const t1 = i + 1 < planos.length ? planos[i + 1].t0 : duracaoTotal;
      const k = (ease[pl.ease || "inOut"])(clamp((t - pl.t0) / (t1 - pl.t0), 0, 1));
      const de = pl.de, para = pl.para || pl.de;
      const pos = mix(de.pos, para.pos, k);
      const alvo = mix(de.alvo, para.alvo, k);
      const tr = pl.tremor || 0;
      if (tr) {
        pos[0] += Math.sin(t * 17.3) * tr + Math.sin(t * 31.7) * tr * 0.5;
        pos[1] += Math.sin(t * 23.1 + 1.3) * tr;
      }
      camera.position.set(pos[0], pos[1], pos[2]);
      camera.fov = lerp(de.fov ?? 35, para.fov ?? de.fov ?? 35, k);
      camera.updateProjectionMatrix();
      camera.lookAt(v.set(alvo[0], alvo[1], alvo[2]));
      return { plano: i, k };
    };
  }

  // ---------- texto em textura (placas, letreiros) ----------
  function texturaTexto(linhas, opcoes = {}) {
    const w = opcoes.largura || 1024, h = opcoes.altura || 512;
    const c = document.createElement("canvas");
    c.width = w; c.height = h;
    const ctx = c.getContext("2d");
    const tex = new THREE.CanvasTexture(c);
    tex.colorSpace = THREE.SRGBColorSpace;
    tex.anisotropy = 4;
    tex.desenhar = (lin = linhas, op = opcoes) => {
      ctx.clearRect(0, 0, w, h);
      if (op.fundo) { ctx.fillStyle = op.fundo; ctx.fillRect(0, 0, w, h); }
      if (op.borda) { ctx.strokeStyle = op.borda; ctx.lineWidth = op.bordaLargura || 18; ctx.strokeRect(14, 14, w - 28, h - 28); }
      ctx.textAlign = "center"; ctx.textBaseline = "middle";
      const n = lin.length;
      lin.forEach((l, idx) => {
        const s = l.tamanho || op.tamanho || 150;
        ctx.font = `${l.peso || op.peso || 400} ${s}px "${l.fonte || op.fonte || "Bangers"}"`;
        ctx.fillStyle = l.cor || op.cor || "#fff";
        if (l.brilho) { ctx.shadowColor = l.cor; ctx.shadowBlur = l.brilho; } else ctx.shadowBlur = 0;
        ctx.fillText(l.texto, w / 2, h * ((idx + 1) / (n + 1)) + (l.dy || 0));
      });
      tex.needsUpdate = true;
    };
    tex.desenhar();
    return tex;
  }

  window.Estudio3D = { ease, trilha, aleatorio, clamp, lerp, carregarGLTF, carregarFonte, criarPersonagem, diretorDeCamera, texturaTexto };
})();
