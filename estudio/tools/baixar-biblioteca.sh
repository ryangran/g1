#!/usr/bin/env bash
# Baixa/gera a biblioteca compartilhada do estúdio (modelos CC0, fontes, Three.js empacotado).
# Uso: ./estudio/tools/baixar-biblioteca.sh   (a partir da raiz do repositório)
set -euo pipefail
B=estudio/biblioteca; L=estudio/lib
mkdir -p "$B/modelos" "$B/fontes" "$L"
RAW=https://raw.githubusercontent.com/mrdoob/three.js/r170/examples/models/gltf
for f in RobotExpressive/RobotExpressive.glb RobotExpressive/README.md Parrot.glb Flamingo.glb Stork.glb; do
  out="$B/modelos/$(basename "$f")"; [ "$f" = RobotExpressive/README.md ] && out="$B/modelos/RobotExpressive.LICENSE.md"
  curl -fsSL --retry 3 "$RAW/$f" -o "$out"
done
# Fontes Google (OFL/Apache): baixa o woff2 latino de cada família
for fam in "Bangers" "Luckiest Guy" "Creepster" "Bebas Neue" "Caveat:wght@700"; do
  name="${fam%%:*}"; q="${fam// /+}"
  url=$(curl -fsSL -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36" "https://fonts.googleapis.com/css2?family=$q&display=swap" | grep -A7 '/\* latin \*/' | grep -o 'https://[^)]*woff2' | head -1)
  curl -fsSL "$url" -o "$B/fontes/${name// /}.woff2"
done
# Three.js + GLTFLoader + SkeletonUtils num único script clássico (window.THREE)
TMP=$(mktemp -d); (cd "$TMP" && npm init -y >/dev/null && npm i -s three@0.170.0 esbuild@0.24.0 gsap@3.14.2 >/dev/null)
cat > "$TMP/entry.js" <<'JS'
import * as THREE_NS from "three";
import { GLTFLoader } from "three/examples/jsm/loaders/GLTFLoader.js";
import * as SkeletonUtils from "three/examples/jsm/utils/SkeletonUtils.js";
import { RoundedBoxGeometry } from "three/examples/jsm/geometries/RoundedBoxGeometry.js";
window.THREE = Object.assign({}, THREE_NS, { GLTFLoader, SkeletonUtils, RoundedBoxGeometry });
JS
"$TMP/node_modules/.bin/esbuild" "$TMP/entry.js" --bundle --minify --format=iife --outfile="$L/three-bundle.js" --log-level=warning
cp "$TMP/node_modules/three/LICENSE" "$L/three.LICENSE"
cp "$TMP/node_modules/gsap/dist/gsap.min.js" "$L/gsap.min.js"
rm -rf "$TMP"
ls -la "$B/modelos" "$B/fontes" "$L"
