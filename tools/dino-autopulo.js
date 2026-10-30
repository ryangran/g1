// Cheat do jogo do dinossauro do Chrome (chrome://dino ou a página "sem internet").
// Como usar: abra o jogo, aperte F12 (Inspecionar) > aba Console, cole este código e dê Enter.
// Para desligar: digite  dinoBot.stop()  no Console.
(() => {
  const runner = Runner.instance_ || Runner.getInstance?.();
  if (!runner) return console.warn('Jogo do dinossauro não encontrado nesta página.');
  if (window.dinoBot) window.dinoBot.stop();

  let frame;
  const tick = () => {
    frame = requestAnimationFrame(tick);
    const t = runner.tRex;
    if (!runner.playing || runner.crashed) return;

    // Primeiro obstáculo que ainda não passou pelo dinossauro.
    const obs = runner.horizon.obstacles.find(o => o.xPos + o.width > t.xPos);
    if (!obs) return t.ducking && t.setDuck(false);

    const speed = runner.currentSpeed;
    const dist = obs.xPos - (t.xPos + t.config.WIDTH);
    const bottom = obs.yPos + obs.typeConfig.height;
    const isBird = obs.typeConfig.type === 'PTERODACTYL';

    if (bottom <= t.groundYPos + 5) {
      // Pássaro alto: passa por baixo correndo.
      if (t.ducking) t.setDuck(false);
    } else if (isBird && obs.yPos < 90) {
      // Pássaro do meio: abaixa.
      if (dist < speed * 12 && !t.jumping && !t.ducking) t.setDuck(true);
    } else if (dist < speed * 9 + obs.width / 2 && !t.jumping) {
      // Cacto ou pássaro baixo: pula.
      if (t.ducking) t.setDuck(false);
      t.startJump(speed);
    } else if (t.ducking && dist > speed * 12) {
      t.setDuck(false);
    }

    // Depois de passar por cima do obstáculo, desce rápido para estar pronto pro próximo.
    const near = runner.horizon.obstacles.some(o =>
      o.xPos < t.xPos + t.config.WIDTH + speed * 4 && o.xPos + o.width > t.xPos - 5);
    if (t.jumping && !t.speedDrop && !near) t.setSpeedDrop();
  };
  tick();

  window.dinoBot = { stop() { cancelAnimationFrame(frame); runner.tRex.setDuck(false); delete window.dinoBot; } };
  console.log('🦖 Auto-pulo ligado! Para desligar: dinoBot.stop()');
})();
