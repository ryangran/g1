#!/usr/bin/env bash
# Publica o site em https://obilhete.vercel.app (projeto "obilhete", time vetrexs-projects).
# Precisa da CLI logada: npx vercel login (abre um link de autorização no navegador).
# As variáveis IG_TOKEN, IG_USER_ID e VOTO_OPCOES já estão no projeto da Vercel.
set -euo pipefail
cd "$(dirname "$0")"
DESTINO=$(mktemp -d)
cp -r index.html serie.js api lib package.json assets "$DESTINO"/
cd "$DESTINO"
npx --yes vercel@65 link --yes --project obilhete --scope vetrexs-projects >/dev/null
npx --yes vercel@65 deploy --prod --yes
