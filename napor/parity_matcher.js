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
      res[q.id] = await page.evaluate(([spec, nomodel]) => {
        const keep = MV.m; if(nomodel) MV.m = null;
        try {
          const full = Object.assign({ move: "", target: "", where: "", scale: "", who: "", open: "", desc: "" }, spec);
          const rd = readSpec(full), m = matchCases(rd);
          const rel = m.cases.length ? relevanceCalc(rd, m.cases, m.dropped) : null;
          const f = {}; for (const k of Object.keys(rd.fields)) { const x = rd.fields[k]; f[k] = { vals: x.fromDesc ? [] : x.vals, ignored: x.ignored, neg: x.neg, excl: x.excl, negated: x.negated, used: x.used }; }
          return { ids: m.cases.map(x => x.c.id), sims: m.cases.map(x => x.sim), strength: m.cases.map(x => x.strength), missed: m.cases.map(x => x.missed), dropped: m.dropped, kept: m.kept, moves: m.moves, moves_from: m.movesFrom, reason: m.reason, hold: !!m.hold, ranked: !!m.ranked, ordered: !!m.ordered,
            neg: !!rd.neg, negs: rd.negs, refrain: !!rd.refrain, boxes_context: !!rd.boxesContext, conflict: !!rd.conflict, ptoks: rd.ptoks, fixes: rd.fixes, unread: rd.unread, sets: rd.sets, fields: f, rev: rd.rev.map(r => [r.text, r.moves]), lex: rd.lex, typed: !!rd.typed, any: !!rd.any,
            cue: { moves: rd.cue.moves, tier: rd.cue.tier, relief: !!rd.cue.relief }, covered_words: rd.coveredWords,
            case_moves: m.cases.map(x => x.c.tags ? x.c.tags.move : "week"),
            rel: rel && { n: rel.n, close: rel.close, pct: rel.pct, band: rel.band, kw_total: rel.kw_total, kw_found: rel.kw_found, kw_missing: rel.kw_missing, words: rel.words } };
        } finally { MV.m = keep; }
      }, [Object.assign({}, q.spec || { desc: q.text }), !!q.nomodel]);
    }
    await page.close();
  }
  await browser.close(); srv.close();
  fs.writeFileSync(out, JSON.stringify({ res, errs }));
  if (errs.length) { console.error("page errors", errs); process.exit(2); }
})();
