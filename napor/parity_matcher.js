// Runs the page's NEW matcher (word-meaning model) in a headless browser on a list of specs and prints each result,
// so tests/test_matcher_parity.py can compare it with napor/matcher_ref.py (same ranked ids, scores within 1e-3).
// usage: node parity_matcher.js <explorer dir> <specs.json [{id, theater, spec}]> <out.json>
const { chromium } = require("playwright");
const http = require("http"), fs = require("fs"), path = require("path");
const [dir, qfile, out] = process.argv.slice(2);
const types = { ".html": "text/html", ".json": "application/json", ".js": "text/javascript" };
const srv = http.createServer((req, res) => {
  const f = path.join(dir, decodeURIComponent(req.url.split("?")[0]).replace(/^\/$/, "/index.html"));
  fs.readFile(f, (e, b) => { if (e) { res.writeHead(404); res.end(); } else { res.writeHead(200, { "content-type": types[path.extname(f)] || "text/plain" }); res.end(b); } });
});
(async () => {
  await new Promise(r => srv.listen(0, "127.0.0.1", r));
  const base = "http://127.0.0.1:" + srv.address().port + "/index.html";
  const qs = JSON.parse(fs.readFileSync(qfile));
  const browser = await chromium.launch();
  const res = {}, errs = [];
  for (const tid of [...new Set(qs.map(q => q.theater))]) {
    const page = await browser.newPage();
    page.on("pageerror", e => errs.push(String(e)));
    await page.goto(base + "#" + tid);
    await page.waitForFunction(t => typeof D !== "undefined" && D && D.matcher && S.theater === t && typeof CAT !== "undefined" && CAT.size > 0, tid, { timeout: 20000 });
    await page.evaluate(() => loadVectors());
    for (const q of qs.filter(x => x.theater === tid)) {
      res[q.id] = await page.evaluate(spec => {
        const full = Object.assign({ move: "", target: "", where: "", scale: "", who: "", open: "", desc: "" }, spec);
        const rd = readSpec(full), m = matchCases(rd);
        return { v: rd.v, ids: m.cases.map(x => x.c.id), sims: m.cases.map(x => x.sim), strength: m.cases.map(x => x.strength), dropped: m.dropped, moves: m.moves, reason: m.reason };
      }, Object.assign({}, q.spec || { desc: q.text }));
    }
    await page.close();
  }
  await browser.close(); srv.close();
  fs.writeFileSync(out, JSON.stringify({ res, errs }));
  if (errs.length) { console.error("page errors", errs); process.exit(2); }
})();
