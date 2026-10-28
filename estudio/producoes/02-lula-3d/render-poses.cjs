// Renderiza as 8 poses em PNG transparente (1024x1024) e monta a folha 4x2.
// Uso: node render-poses.cjs [pose...]
const { chromium } = require("playwright");
const { execFileSync } = require("node:child_process");
const { pathToFileURL } = require("node:url");
const path = require("node:path");

(async () => {
const dir = __dirname;
const poses = process.argv.slice(2).map(Number).filter(Boolean);
const lista = poses.length ? poses : [1, 2, 3, 4, 5, 6, 7, 8];
const browser = await chromium.launch({ args: ["--use-angle=swiftshader", "--enable-unsafe-swiftshader", "--allow-file-access-from-files"] });
const page = await browser.newPage({ viewport: { width: 1024, height: 1024 } });
page.on("pageerror", (e) => console.error("erro na página:", e.message));
for (const n of lista) {
  await page.goto(pathToFileURL(path.join(dir, "poses.html")).href + `?pose=${n}`);
  await page.waitForFunction(() => window.__pronto === true, null, { timeout: 120000 });
  await page.locator("#c").screenshot({ path: path.join(dir, `renders/pose-${n}.png`), omitBackground: true });
  console.log("pose", n, "ok");
}
await browser.close();
if (!poses.length) {
  const ins = lista.flatMap((n) => ["-i", path.join(dir, `renders/pose-${n}.png`)]);
  const f = lista.map((_, i) => `[${i}:v]`).join("") + `xstack=inputs=8:layout=0_0|w0_0|w0+w1_0|w0+w1+w2_0|0_h0|w0_h0|w0+w1_h0|w0+w1+w2_h0[g];color=white:s=4096x2048[bg];[bg][g]overlay=format=auto,scale=2048:-1`;
  execFileSync("ffmpeg", ["-v", "error", "-y", ...ins, "-filter_complex", f, "-frames:v", "1", path.join(dir, "renders/folha.png")]);
  console.log("folha ok");
}
})();
