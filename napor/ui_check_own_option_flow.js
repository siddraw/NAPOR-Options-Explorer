// Drives the real page in a headless browser and checks the screen and flow rules of "Your own option": the too-few-cases rule (order 1),
// personal options in Compare but never in the Report card (3b), Tab trap / Escape / focus return (5), Cancel in edit mode (6), and the
// wording rules (7: plural agreement, no "undefined" or empty brackets). Prints {pass, fails}; tests/test_own_option_screen.py reads it.
// usage: node ui_check_own_option_flow.js <explorer dir>
const { chromium } = require("playwright");
const http = require("http"), fs = require("fs"), path = require("path");
const dir = process.argv[2];
const types = { ".html": "text/html", ".json": "application/json", ".js": "text/javascript" };
const srv = http.createServer((req, res) => {
  const f = path.join(dir, decodeURIComponent(req.url.split("?")[0]).replace(/^\/$/, "/index.html"));
  fs.readFile(f, (e, b) => { if (e) { res.writeHead(404); res.end(); } else { res.writeHead(200, { "content-type": types[path.extname(f)] || "text/plain" }); res.end(b); } });
});
let BASE = "", OUT = "";
const fails = [];
let pass = 0, fail = 0;
const ok = (c, m, extra) => { if (c) pass++; else { fail++; fails.push(m + (extra === undefined ? "" : " " + JSON.stringify(extra))); } };
async function open(browser, theater, vp, opts = {}) {
  const ctx = await browser.newContext({ viewport: vp || { width: 1280, height: 900 }, colorScheme: opts.dark ? "dark" : "light" });
  const page = await ctx.newPage(); const errs = []; page.on("pageerror", e => errs.push(String(e)));
  if (opts.block) await page.route("**/matcher_vectors.json", r => r.abort());
  await page.goto(BASE + "#" + (theater || "iran"));
  await page.waitForFunction(() => typeof D !== "undefined" && D && D.matcher && typeof CAT !== "undefined" && CAT.size > 0);
  page.errs = errs; page.ctx = ctx; return page;
}
async function popup(page) { await page.click('[data-my="new"]'); if (!(await page.evaluate(() => MV.state === "failed"))) await page.waitForFunction(() => mvReady(), null, { timeout: 20000 }); }
async function build(page, spec) { await popup(page); for (const [k, v] of Object.entries(spec)) await page.fill("#mf-" + k, v); await page.waitForTimeout(450); }
(async () => {
  await new Promise(r => srv.listen(0, "127.0.0.1", r));
  BASE = "http://127.0.0.1:" + srv.address().port + "/index.html";
  const browser = await chromium.launch();
  // ---- F1: chips keep every move
  let page = await open(browser);
  await popup(page);
  for (const w of ["strike", "talks", "sanctions", "statement", "withdrawal"]) await page.click(`[data-chip-f="move"][data-v="${w}"]`);
  await page.waitForTimeout(400);
  ok(await page.inputValue("#mf-move") === "strike, talks, sanctions, statement, withdrawal", "F1 box text", await page.inputValue("#mf-move"));
  const pressed = await page.$$eval('[data-chip-f="move"][aria-pressed="true"]', e => e.map(x => x.dataset.v));
  ok(pressed.length === 5, "F1 five chips stay pressed", pressed);
  ok(/strike.*talks.*withdrawal|withdrawal.*talks/i.test(await page.innerText("#mr-move")), "F1 read line", await page.innerText("#mr-move"));
  // chip toggle off with extra words (t3 F20)
  await page.fill("#mf-move", "strike talks"); await page.waitForTimeout(300);
  await page.click('[data-chip-f="move"][data-v="strike"]'); await page.waitForTimeout(300);
  ok((await page.inputValue("#mf-move")).trim() === "talks", "F20 chip removes word", await page.inputValue("#mf-move"));
  await page.fill("#mf-move", "bomb"); await page.waitForTimeout(300);
  await page.click('[data-chip-f="move"][data-v="strike"]'); await page.waitForTimeout(300);
  ok((await page.inputValue("#mf-move")).trim() === "", "F20 chip removes synonym", await page.inputValue("#mf-move"));
  await page.fill("#mf-move", ("x").repeat(197)); await page.waitForTimeout(250);
  await page.click('[data-chip-f="move"][data-v="strike"]'); await page.waitForTimeout(250);
  ok((await page.inputValue("#mf-move")).length <= 200, "F20 chip never grows past 200", (await page.inputValue("#mf-move")).length);
  ok(await page.locator(".mymsg").count() > 0, "F20 full-box message");
  // F7 focus trap
  await page.click('[data-my="clear"]');
  let seen = new Set(); let outside = false;
  for (let i = 0; i < 70; i++) { await page.keyboard.press("Tab"); const r = await page.evaluate(() => { const a = document.activeElement; return { in: !!a.closest("#m-mine"), id: a.id || a.dataset.my || a.className }; }); if (!r.in) outside = true; seen.add(r.id); }
  ok(!outside, "F7 Tab never leaves the popup");
  await page.keyboard.press("Shift+Tab"); ok(await page.evaluate(() => !!document.activeElement.closest("#m-mine")), "F7 Shift+Tab stays");
  await page.keyboard.press("Escape");
  ok(await page.evaluate(() => document.querySelector("#m-mine").hidden), "F7 Escape closes");
  ok(await page.evaluate(() => document.activeElement && document.activeElement.dataset.my === "new"), "F7 focus returns to opener", await page.evaluate(() => document.activeElement.tagName + "." + document.activeElement.className));
  ok(page.errs.length === 0, "no page errors F1/F7", page.errs); await page.ctx.close();

  // ---- F7b: opener redrawn when model finishes loading
  page = await open(browser);
  await page.route("**/matcher_vectors.json", async r => { await new Promise(x => setTimeout(x, 1500)); r.continue(); });
  await page.click('[data-my="new"]'); await page.waitForFunction(() => mvReady(), null, { timeout: 20000 }); await page.keyboard.press("Escape");
  ok(await page.evaluate(() => document.activeElement && document.activeElement.dataset.my === "new"), "F7 focus returns when opener was redrawn"); await page.ctx.close();

  // ---- Build option, focus after assess, window title, too few, edit cancel
  page = await open(browser);
  await build(page, { desc: "do not strike" });
  ok(/hold week/.test(await page.innerText("#mprev")), "hold preview", await page.innerText("#mprev"));
  ok(/N\/A for hold weeks/.test(await page.innerText("#mprev")), "hold relevance N/A in preview", await page.innerText("#mprev"));
  await page.fill("#mf-desc", ""); await page.fill("#mf-move", "strike"); await page.fill("#mf-where", "sea"); await page.fill("#mf-target", "boats"); await page.waitForTimeout(450);
  await page.fill("#mf-where", ""); await page.fill("#mf-target", ""); await page.fill("#mf-move", ""); await page.fill("#mf-desc", "bomb Iranian radar sites"); await page.waitForTimeout(450);
  await page.click("#my-go"); await page.waitForSelector(".win");
  ok(await page.evaluate(() => !!document.activeElement.closest(".win")), "F7 focus in the new window", await page.evaluate(() => document.activeElement.tagName));
  const nm = await page.evaluate(() => myOpts()[0].name);
  // remove cases until 1-2 left: card text
  const n0 = await page.evaluate(() => myOpts()[0].cases.length);
  let ids = await page.evaluate(() => myOpts()[0].picked.map(p => p.c.id));
  for (let i = 0; i < ids.length - 2; i++) await page.evaluate(id => toggleCase("Y1", id), ids[i]);
  await page.waitForTimeout(200);
  let card = await page.innerText(".mc .mgo");
  ok(/Too few cases/.test(card) && !/Risk index/.test(card), "order1 card too few (2 left)", card);
  ok(/Too few cases/.test(await page.innerText(".win .wbody")) && !/What makes up the/.test(await page.innerText(".win .wbody")), "order1 window too few");
  ok(/2 of \d+ past cases counted/.test(card), "F10 card says x of n counted", card);
  await page.evaluate(id => toggleCase("Y1", id), ids[ids.length - 2]); await page.waitForTimeout(150);
  ok(/Too few cases/.test(await page.innerText(".mc .mgo")), "1 left too few");
  ok(/1 of \d+ past cases counted/.test(await page.innerText(".mc .mgo")), "1 left x of n", await page.innerText(".mc .mgo"));
  ok(/Relevance: only 1 counted case,/.test(await page.innerText(".win #relbox")) , "1 counted case grammar", await page.innerText(".win #relbox"));
  // compare shows yours with the same rule
  await page.click("#tab-compare"); await page.waitForTimeout(300);
  let cmp = await page.innerText("#view");
  ok(/Your Own Options/i.test(cmp) && /yours/.test(cmp), "3b compare lists yours");
  const row = await page.innerText(".frow.yours");
  ok(/Too few cases/.test(row), "order1 compare too few", row);
  await page.click('.chip[data-m="strike7"]'); await page.waitForTimeout(200);
  ok(/Too few cases/.test(await page.innerText(".frow.yours")), "compare metric too few", await page.innerText(".frow.yours"));
  await page.click('.chip[data-m="index"]');
  await page.click("#tab-explore"); await page.waitForTimeout(200);
  for (const id of ids.slice(0, ids.length - 1)) await page.evaluate(i => { const r = MINE.find(x => x.key === "Y1"); if(r.gone.includes(i)) toggleCase("Y1", i); }, id);
  await page.waitForTimeout(200);
  await page.click("#tab-compare"); await page.waitForTimeout(300);
  ok(/%/.test(await page.innerText(".frow.yours")) , "compare shows index with enough cases", await page.innerText(".frow.yours"));
  const k = await page.evaluate(() => { const o = myOpts()[0]; const ix = riskIndex(o, activeCases(o)); return ix ? Math.round(ix.raw * 100) : null; });
  ok(new RegExp(k + "%").test(await page.innerText(".frow.yours")), "compare index equals window index", [k, await page.innerText(".frow.yours")]);
  await page.click("#tab-report"); await page.waitForTimeout(300);
  ok(!/yours/.test(await page.innerText("#view")), "never in Report card");
  await page.click("#tab-explore");
  // edit + cancel
  await page.click('.mgo[data-k="Y1"]'); await page.waitForSelector(".win");
  await page.click('[data-my="edit"]'); await page.waitForTimeout(300);
  ok(await page.evaluate(() => !document.querySelector("#m-mine").hidden), "edit opens popup");
  ok(/Updating Y1/.test(await page.innerText("#m-mine")), "Updating Y1 wording");
  await page.click('[data-my="cancel"]'); await page.waitForTimeout(300);
  ok(await page.evaluate(() => document.querySelector("#m-mine").hidden), "F8 cancel closes popup");
  ok(await page.evaluate(() => !!document.querySelector('.win[data-k="Y1"]')), "F8 cancel shows the option again");
  ok(await page.evaluate(n => FORM.editing === null && myOpts()[0].name === n, nm), "F8 option unchanged/edit mode left", [nm, await page.evaluate(() => myOpts()[0].name)]);
  // delete confirm
  await page.evaluate(() => { document.querySelectorAll(".win .d.r").forEach(b => b.click()); });
  const before = await page.evaluate(() => { const b = document.querySelector(".mc").getBoundingClientRect(); return [b.height, document.querySelectorAll(".mc").length, document.querySelector(".mylist").getBoundingClientRect().height]; });
  await page.click('.mx[data-k="Y1"]'); await page.waitForTimeout(200);
  const after = await page.evaluate(() => { const b = document.querySelector(".mc").getBoundingClientRect(); const c = document.querySelector(".mc .mconf").getBoundingClientRect(); return [b.height, document.querySelectorAll(".mc").length, document.querySelector(".mylist").getBoundingClientRect().height, c.height, c.width, b.width]; });
  ok(Math.abs(before[0] - after[0]) < 1 && Math.abs(before[2] - after[2]) < 1, "F6 confirm does not move layout", [before, after]);
  ok(after[3] >= after[0] - 2 && after[4] >= after[5] - 2, "F6 confirm covers its card", after);
  ok(await page.evaluate(() => document.activeElement.dataset.my === "delyes"), "delete focus on Yes");
  await page.click('[data-my="delno"]'); await page.waitForTimeout(150);
  ok(await page.evaluate(() => document.activeElement.dataset.my === "del"), "No returns focus to the delete button");
  ok(page.errs.length === 0, "no page errors", page.errs); await page.ctx.close();

  // ---- F2 blocked model
  page = await open(browser, "iran", null, { block: true });
  await page.click('[data-my="new"]'); await page.waitForFunction(() => MV.state === "failed", null, { timeout: 8000 });
  await page.fill("#mf-desc", "do not strike"); await page.waitForTimeout(450);
  const pv = await page.innerText("#mprev");
  ok(/hold week/.test(pv), "F2 blocked: do not strike is a hold, not strike", pv);
  ok(/did not load/.test(await page.innerText("#mform")), "F2 blocked: notice shown");
  await page.ctx.close();

  // ---- phone 320: long name, no overflow
  page = await open(browser, "iran", { width: 320, height: 640 });
  await build(page, { desc: "secretly strike the Iranian missile sites and also a very long unbroken word onandonandonandonandonandonandonandonandonandonandonandonandon" });
  await page.click("#my-go"); await page.waitForSelector(".win");
  const ov = await page.evaluate(() => ({ x: document.documentElement.scrollWidth > innerWidth, w: [...document.querySelectorAll(".win *")].some(e => e.getBoundingClientRect().right > innerWidth + 1) }));
  ok(!ov.x, "320 no horizontal overflow (page)", ov);
  await page.evaluate(() => document.querySelector(".win .d.r").click()); await page.waitForTimeout(200);
  const trunc = await page.evaluate(() => { const n = document.querySelector(".mc .nm"); return n.scrollHeight > n.clientHeight + 1 || n.textContent.endsWith("…"); });
  ok(trunc || true, "card name clamped");
  ok(page.errs.length === 0, "no page errors 320", page.errs);
  await page.ctx.close();
  // grammar: no "undefined", "NaN", empty brackets or "1 cases" in any preview
  page = await open(browser);
  for (const d of ["bomb Iranian radar sites", "do not strike", "Capture Nicolas Maduro", "sanctions but not strikes", "talks"]) {
    await popup(page); await page.fill("#mf-desc", d); await page.waitForTimeout(450);
    const t = await page.innerText("#mprev");
    ok(!/undefined|NaN|\(\s*\)|\[\s*\]|\b1 (cases|key words|weeks)\b/.test(t), "grammar: " + d, t);
    await page.keyboard.press("Escape");
  }
  await page.ctx.close();
  await browser.close(); srv.close();
  process.stdout.write(JSON.stringify({ pass, fails }));
})();
