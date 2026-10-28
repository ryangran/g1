#!/usr/bin/env bash
# Cria um episódio novo (projeto HyperFrames vertical 1080x1920) com a biblioteca do estúdio.
# Uso: ./estudio/tools/novo-episodio.sh 02-nome-do-episodio
set -euo pipefail
NOME="${1:?uso: novo-episodio.sh <pasta>}"
E="$(cd "$(dirname "$0")/.." && pwd)"
D="$E/producoes/$NOME"
[ -e "$D" ] && { echo "já existe: $D"; exit 1; }
mkdir -p "$D"/{assets/lib,assets/modelos,assets/fontes,assets/audio,docs,renders}
cp "$E"/lib/{three-bundle.js,gsap.min.js,estudio3d.js} "$D/assets/lib/"
cp "$E"/biblioteca/modelos/*.glb "$D/assets/modelos/"
cp "$E"/biblioteca/fontes/*.woff2 "$D/assets/fontes/"
for f in "$E"/modelos-docs/*.md; do sed "s/<episódio>/$NOME/g" "$f" > "$D/docs/$(basename "$f")"; done
cat > "$D/hyperframes.json" <<'J'
{
  "$schema": "https://hyperframes.heygen.com/schema/hyperframes.json",
  "registry": "https://raw.githubusercontent.com/heygen-com/hyperframes/main/registry",
  "paths": { "blocks": "compositions", "components": "compositions/components", "assets": "assets" },
  "media": { "autoProxy": true }
}
J
printf '{\n  "id": "%s",\n  "name": "%s"\n}\n' "$NOME" "$NOME" > "$D/meta.json"
cat > "$D/package.json" <<'J'
{
  "private": true,
  "type": "module",
  "scripts": {
    "dev": "npx --yes hyperframes@0.8.193 preview",
    "check": "npx --yes hyperframes@0.8.193 check",
    "render": "npx --yes hyperframes@0.8.193 render -o renders/final.mp4"
  }
}
J
printf 'renders/\n.hyperframes/\nbuild/\n' > "$D/.gitignore"
echo "criado: $D"
