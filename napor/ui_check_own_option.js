// Drives the real page in a headless browser: builds "Your own option" through the popup (typing into the boxes, pressing Assess) and prints, for each
// query, what the viewer sees: the live preview, the Relevance box in the option window, the small line on the saved card, and the risk index.
// tests/test_own_option_ui.py compares those numbers with napor/matcher_ref.py. usage: node ui_check_own_option.js <explorer dir> <queries.json [{id, theater, spec}]> <out.json> [shots dir]
const { chromium } = require("playwright");
const http = require("http"), fs = require("fs"), path = require("path");
const [dir, qfile, out, shots] = process.argv.slice(2);
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
  for (const q of qs) {
    const ctx = await browser.newContext({ viewport: { width: 1280, height: 900 } });
    const page = await ctx.newPage();
    page.on("pageerror", e => errs.push(q.id + ": " + String(e)));
    await page.goto(base + "#" + q.theater);
    await page.waitForFunction(t => typeof D !== "undefined" && D && D.matcher && S.theater === t && typeof CAT !== "undefined" && CAT.size > 0, q.theater, { timeout: 20000 });
    await page.click('[data-my="new"]');
    await page.waitForFunction(() => mvReady(), null, { timeout: 20000 });
    for (const [k, v] of Object.entries(q.spec)) if (v) await page.fill("#mf-" + k, v);
    await page.waitForTimeout(450);
    const preview = await page.innerText("#mprev");
    const r = { preview };
    if (!(await page.isDisabled("#my-go"))) {
      await page.click("#my-go");
      await page.waitForSelector(".win");
      const win = page.locator(".win").first();
      r.relbox = await win.locator("#relbox").count() ? await win.locator("#relbox").innerText() : null;
      r.card = await page.locator(".mc .rel").count() ? await page.locator(".mc .rel").first().innerText() : null;
      r.cardText = await page.locator(".mc .mgo").first().innerText();
      r.title = await win.locator(".wbar").innerText();
      r.body = await win.locator(".wbody").innerText();
      r.risk = await page.evaluate(() => { const o = myOpts()[0], ix = riskIndex(o, activeCases(o)); return { n: activeCases(o).length, raw: ix ? ix.raw : null, hold: !!o.is_hold }; });
      r.rel = await page.evaluate(() => relOf(myOpts()[0]));
      if (shots && q.shot) { await page.screenshot({ path: path.join(shots, q.shot + ".png") }); }
    } else if (shots && q.shot) { await page.screenshot({ path: path.join(shots, q.shot + ".png") }); }
    res[q.id] = r;
    await ctx.close();
  }
  await browser.close(); srv.close();
  fs.writeFileSync(out, JSON.stringify({ res, errs }));
  if (errs.length) { console.error("page errors", errs); process.exit(2); }
})();
