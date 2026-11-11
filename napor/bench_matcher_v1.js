// Runs the OLD (word-reader, version 1) matcher of "Your own option" on the benchmark queries, in a headless browser.
// usage: node bench_matcher_v1.js <site dir holding the old index.html + data> <queries.json> <out.json>
// Only the query text goes into the Description box, like a viewer who types "what if the US did X".
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
  const res = {};
  for (const tid of [...new Set(qs.map(q => q.theater))]) {
    const page = await browser.newPage();
    const errs = []; page.on("pageerror", e => errs.push(String(e)));
    await page.goto(base + "#" + tid);
    await page.waitForFunction(t => typeof D !== "undefined" && D && D.matcher && S.theater === t && typeof CAT !== "undefined" && CAT.size > 0, tid, { timeout: 20000 });
    for (const q of qs.filter(x => x.theater === tid)) {
      res[q.id] = await page.evaluate(text => {
        const rd = readSpec({ move: "", target: "", where: "", scale: "", who: "", open: "", desc: text });
        const m = matchCases(rd.sets);
        return { ids: m.cases.map(x => x.c.id), sets: rd.sets, dropped: m.dropped };
      }, q.text);
    }
    if (errs.length) console.error("page errors", errs);
    await page.close();
  }
  await browser.close(); srv.close();
  fs.writeFileSync(out, JSON.stringify(res));
})();
