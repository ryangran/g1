# Caricatura 3D — 8 variações

Personagem 3D caricato (cabelo e barba grisalhos, terno, gravata vermelha, faixa presidencial) feito só com geometria procedural em Three.js, a partir da folha de figurinhas de referência. É caricatura estilizada, não fotorrealismo.

- `personagem.js` — modelo + rig (quadril, tronco, cabeça, ombros, cotovelos, mãos, coxas, joelhos, pés) + expressões (pálpebras, sorriso, sobrancelhas, boca).
- `poses.js` — as 8 poses e os acessórios (estrela, bonés "BRASIL" e com bandeira, pizza, garfo, livro "História", confete, "?", "zzz").
- `render-poses.cjs` — gera `renders/pose-N.png` (1024×1024, fundo transparente, prontas para figurinha) e `renders/folha.png`.

```bash
node render-poses.cjs        # todas
node render-poses.cjs 3 5    # só algumas
```

Para animar: o mesmo `Caricatura.criar(THREE)` funciona dentro de uma composição HyperFrames com o Estudio3D (trocar `posar()` por chaves de rotação no tempo).
