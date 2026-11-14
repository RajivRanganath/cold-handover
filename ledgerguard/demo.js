// LedgerGuard live demo: runs the original Python package in the browser (Pyodide)
// and answers the dashboard's single data call, /api/state, from it. Adds an edit
// panel and voice/typed commands. Loaded in <head>, before the dashboard script.
(() => {
  const PYODIDE = "https://cdn.jsdelivr.net/pyodide/v0.27.7/full/";
  let EDITS = [], CASES = [], demo = null, lastFocus = null, LAST = null, FIX = false, py = null;

  const ready = (async () => {
    await new Promise((ok, fail) => {
      const s = document.createElement("script");
      s.src = PYODIDE + "pyodide.js"; s.onload = ok; s.onerror = () => fail(new Error("Could not load Pyodide from the CDN"));
      document.head.appendChild(s);
    });
    status("Starting Python in your browser...");
    py = await loadPyodide({ indexURL: PYODIDE });
    status("Loading pydantic...");
    await py.loadPackage(["pydantic"]);
    status("Loading the LedgerGuard source...");
    const bridge = await (await fetch("lg_demo.py")).text();
    for (const [dir, zip] of [["lg-orig", "ledgerguard.zip"], ["lg-fixed", "ledgerguard-fixed.zip"]]) {
      py.unpackArchive(await (await fetch(zip)).arrayBuffer(), "zip", { extractDir: "/home/pyodide/" + dir });
      py.FS.writeFile(`/home/pyodide/${dir}/lg_demo.py`, bridge);
    }
    load();
    CASES = JSON.parse(demo.case_ids());
    status("");
  })();

  // Import the bridge and package from the original or the fixed copy; edits live in JS, so they survive a switch.
  function load() {
    py.globals.set("lg_dir", "/home/pyodide/" + (FIX ? "lg-fixed" : "lg-orig"));
    py.runPython(`
import sys
sys.path[:] = [p for p in sys.path if not p.startswith("/home/pyodide/lg-")]
sys.path.insert(0, lg_dir)
for m in [m for m in sys.modules if m == "lg_demo" or m.split(".")[0] == "ledgerguard"]: del sys.modules[m]`);
    demo = py.pyimport("lg_demo");
  }

  const realFetch = window.fetch.bind(window);
  window.fetch = async (url, opts) => {
    if (String(url).endsWith("/api/state")) {
      await ready;
      status("LedgerGuard is reconciling 85 payments...");
      await new Promise(r => setTimeout(r, 30)); // let the status paint before Python blocks
      const t = performance.now();
      const body = demo.state(JSON.stringify(EDITS));
      const secs = (performance.now() - t) / 1000;
      status(`Ran in your browser in ${secs < 0.1 ? "under 0.1" : secs.toFixed(1)} s.` + (EDITS.length ? " Your edits are applied." : "") + (FIX ? " Running the agent's fixed code." : ""));
      return new Response(body, { headers: { "content-type": "application/json" } });
    }
    return realFetch(url, opts);
  };

  // The dashboard's download link points at a server route; serve it from memory instead.
  document.addEventListener("click", e => {
    const a = e.target.closest('a[href$="/api/evidence-download"]');
    if (!a || !window.STATE_JSON) return;
    e.preventDefault();
    const url = URL.createObjectURL(new Blob([window.STATE_JSON], { type: "application/json" }));
    Object.assign(document.createElement("a"), { href: url, download: "ledgerguard-evidence.json" }).click();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  });

  // ---------- edits ----------
  const LABEL = { drop_settlement: "Remove the settlement", drop_bank: "Remove the bank credit", extra_fee: "Add an extra fee", fail_settlement: "Mark the settlement as failed" };
  const lcNum = id => String(Number(id.replace(/\D/g, "")));
  const lcId = n => "LC" + String(n).padStart(4, "0");

  async function rerun(focusLc) {
    lastFocus = focusLc || null;
    renderEdits();
    await window.lgRender();
  }
  function addEdit(op, n, rupees) {
    const lc = lcId(n);
    if (!CASES.includes(lc)) return say(`Case ${n} is not in the test batch. Try one of: ${CASES.slice(0, 8).map(lcNum).join(", ")}.`);
    if (op === "extra_fee" && !(rupees > 0)) return say("Say how much, for example: add a 200 rupee fee to case 4.");
    EDITS.push({ op, lc, rupees: rupees || 0 });
    say(`${LABEL[op]} on case ${n}${op === "extra_fee" ? `, ₹${rupees}` : ""}. Rerunning LedgerGuard...`);
    return rerun(lc);
  }
  async function setFix(on) {
    if (on === FIX) return say(`Already running the ${on ? "agent's fix" : "original code"}.`);
    await ready;
    FIX = on; lastFocus = null;
    document.getElementById("lg-fix").checked = on;
    say(on ? "Switching to the agent's fix (attempt M-T2-03). Rerunning with your edits..." : "Switching back to the original code. Rerunning with your edits...");
    load();
    await rerun(EDITS.length ? EDITS[EDITS.length - 1].lc : null); // report the edited case's real state
    if (!EDITS.length) say(on ? "Now running the agent's fix. Try: mark the settlement for case 4 as failed." : "Now running the original code.");
  }
  function reset() { EDITS = []; say("All edits removed. Rerunning on the original data..."); return rerun(); }

  function showCase(n) {
    const c = LAST && LAST.cases.find(c => c.lifecycle_id === lcId(n));
    const item = c && document.querySelector(`.caseitem[data-id="${CSS.escape(c.case_id)}"]`);
    if (!item) return say(`Case ${n} is not in the test batch. Try one of: ${CASES.slice(0, 8).map(lcNum).join(", ")}.`);
    const search = document.getElementById("case-search");
    if (search) { search.value = ""; search.dispatchEvent(new Event("input")); }
    item.click();
    document.getElementById("cases")?.scrollIntoView({ behavior: matchMedia("(prefers-reduced-motion: reduce)").matches ? "auto" : "smooth" });
    say(`Case ${n} (${c.case_id}): ${STATE_WORDS[c.state] || c.state}${c.exception_type ? `, ${c.exception_type.replace("EXCEPTION_", "").replace(/_/g, " ").toLowerCase()}` : ""}.`);
  }
  const STATE_WORDS = { MATCHED: "matched and proved", AUTO_RESOLVED: "explained and closed after the Evidence Gate verified it",
    RECOMMEND_REVIEW: "explained, but a person must confirm", HUMAN_REVIEW_REQUIRED: "LedgerGuard refused to close it; a person must review" };

  // Called by the dashboard after every render (see the patched script).
  window.lgAfterRender = s => {
    LAST = s;
    document.getElementById("lg-notice")?.remove();
    if (EDITS.length) document.getElementById("benchmark")?.insertAdjacentHTML("afterbegin",
      `<p id="lg-notice" role="note" style="background:var(--warn-bg);color:var(--warn);border:1px solid var(--warn);border-radius:8px;padding:10px 14px;margin:0 0 14px;font-weight:600">You have edited the test data. This table still scores against the original answer key, so your edits appear as errors here.</p>`);
    window.STATE_JSON = JSON.stringify(s, null, 2);
    const byLc = Object.fromEntries(s.cases.map(c => [c.lifecycle_id, c.case_id]));
    document.getElementById("lg-case").innerHTML = CASES.map(id => `<option value="${lcNum(id)}">${lcNum(id)} (${byLc[id] || id})</option>`).join("");
    if (lastFocus) {
      showCase(lcNum(lastFocus));
      const last = EDITS[EDITS.length - 1], c = s.cases.find(c => c.lifecycle_id === lastFocus);
      if (!FIX && last && last.op === "fail_settlement" && c && ["MATCHED", "AUTO_RESOLVED"].includes(c.state))
        say(document.getElementById("lg-say").textContent + " That is the bug: the original code ignores settlement status. Try: use the agent's fix.");
    }
    else if (!EDITS.length) say("Original data: every case is as LedgerGuard first saw it.");
  };

  // ---------- commands (voice or typed) ----------
  const WORDS = { zero: 0, one: 1, two: 2, three: 3, four: 4, five: 5, six: 6, seven: 7, eight: 8, nine: 9, ten: 10,
    eleven: 11, twelve: 12, thirteen: 13, fourteen: 14, fifteen: 15, sixteen: 16, seventeen: 17, eighteen: 18, nineteen: 19,
    twenty: 20, thirty: 30, forty: 40, fifty: 50, hundred: 100, thousand: 1000, for: 4, to: 2, too: 2 };
  function normalise(t) {
    return t.toLowerCase().replace(/[₹,]/g, " ").replace(/\b(case|payment|lifecycle|number)\s+(for|to|too)\b/g, (m, a, b) => `${a} ${WORDS[b]}`)
      .replace(/\b(zero|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|thirty|forty|fifty|hundred|thousand)\b/g, w => WORDS[w]);
  }
  function run(text) {
    const t = normalise(text);
    const caseN = (t.match(/\b(?:case|payment|lifecycle|lc|number)\s*0*(\d+)/) || [])[1];
    const amount = (t.match(/(\d+(?:\.\d+)?)\s*(?:rupees?|rs|inr)/) || t.match(/(?:fee of|fee|by)\s*(\d+(?:\.\d+)?)/) || [])[1];
    if (/\b(original code|(turn|switch) off the fix|disable the fix|without the fix)\b/.test(t)) return setFix(false);
    if (/\b(agent'?s fix|(turn|switch) on the fix|enable the fix|use the fix|fixed code)\b/.test(t)) return setFix(true);
    if (/\b(reset|start over|undo all|clear|original)\b/.test(t)) return reset();
    if (/\b(run|rerun|again|refresh)\b/.test(t) && !caseN) { say("Rerunning LedgerGuard..."); return rerun(); }
    if (/\b(fail|failed)\b/.test(t) && /settle/.test(t) && caseN) return addEdit("fail_settlement", caseN);
    if (/\b(remove|delete|drop|lose|lost|missing|without)\b/.test(t) && /settle/.test(t) && caseN) return addEdit("drop_settlement", caseN);
    if (/\b(remove|delete|drop|lose|lost|missing|without)\b/.test(t) && /\b(bank|credit|deposit)/.test(t) && caseN) return addEdit("drop_bank", caseN);
    if (/\bfee/.test(t) && caseN) return addEdit("extra_fee", caseN, Number(amount));
    if (/\b(show|open|select|go to|explain|look at)\b/.test(t) && caseN) return showCase(caseN);
    const sections = { walkthrough: "walkthrough", benchmark: "benchmark", adversarial: "adversarial", exception: "exceptions", queue: "exceptions", explorer: "cases", overview: "overview", top: "overview" };
    for (const [k, id] of Object.entries(sections)) if (t.includes(k)) {
      document.getElementById(id)?.scrollIntoView(); return say(`Showing the ${k}.`);
    }
    if (caseN) return showCase(caseN);
    if (/\bnext\b/.test(t)) { document.getElementById("tour-next")?.click(); document.getElementById("walkthrough")?.scrollIntoView(); return say("Next walkthrough step."); }
    say(`I heard "${text}" but didn't match a command. Try one of the examples.`);
  }

  // ---------- panel ----------
  const css = `
  .lg-panel{position:sticky;top:0;z-index:20;background:var(--card);border-bottom:1px solid var(--line-2);box-shadow:0 4px 18px rgba(13,35,102,.06)}
  .lg-in{max-width:1180px;margin:0 auto;padding:10px 20px;display:grid;gap:8px}
  .lg-row{display:flex;flex-wrap:wrap;gap:8px;align-items:center}
  .lg-panel select,.lg-panel input{font:inherit;font-size:14px;padding:7px 9px;border:1px solid var(--line-2);border-radius:8px;background:var(--bg-2);color:var(--text)}
  .lg-panel input[type=number]{width:90px} .lg-cmd{flex:1;min-width:220px}
  .lg-panel button{font:inherit;font-size:14px;font-weight:600;padding:7px 13px;border-radius:8px;border:1px solid var(--accent);background:var(--card);color:var(--accent-dk);cursor:pointer}
  .lg-panel button.pri{background:var(--accent-dk);color:#fff}
  .lg-panel button:focus-visible,.lg-panel input:focus-visible,.lg-panel select:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
  .lg-mic[aria-pressed=true]{background:#C62828;border-color:#C62828;color:#fff}
  .lg-say{font-size:14px;color:var(--navy);font-weight:600} .lg-or{color:var(--muted);font-size:13px} .lg-status{font-size:13px;color:var(--muted)}
  .lg-edits{display:flex;flex-wrap:wrap;gap:6px;font-size:13px} .lg-edits span{background:var(--warn-bg);color:var(--warn);padding:3px 9px;border-radius:999px}
  .lg-help{font-size:13px;color:var(--muted)} .lg-help[open]{padding-bottom:4px} .lg-help summary{cursor:pointer;color:var(--accent-dk)} .lg-help li{margin:2px 0}
  .lg-title{font-weight:700;color:var(--navy);font-size:15px} .lg-back{font-size:13px}
  @media(max-width:540px){.lg-in{padding:10px 14px}.lg-panel{position:static}}`;
  const html = `<div class="lg-panel" role="region" aria-label="Live demo controls"><div class="lg-in">
    <div class="lg-row"><span class="lg-title">LedgerGuard, running live in your browser</span>
      <span class="lg-status" id="lg-status" aria-live="polite">Loading...</span><a class="lg-back" href="../">Back to the case study</a></div>
    <div class="lg-row">
      <button type="button" class="lg-mic" id="lg-mic" aria-pressed="false" hidden>Hold to talk</button>
      <input class="lg-cmd" id="lg-cmd" placeholder='Try "remove the settlement for case 4"' aria-label="Command (speak, type or dictate)">
      <button type="button" id="lg-go">Go</button>
      <span class="lg-or">or</span>
      <select id="lg-op" aria-label="Edit"><option value="drop_settlement">Remove the settlement</option><option value="drop_bank">Remove the bank credit</option><option value="extra_fee">Add an extra fee</option><option value="fail_settlement">Mark the settlement as failed</option></select>
      <span>on case</span><select id="lg-case" aria-label="Case"></select>
      <input type="number" id="lg-amt" min="1" value="250" aria-label="Fee in rupees" hidden>
      <button type="button" class="pri" id="lg-apply">Apply and rerun</button>
      <button type="button" id="lg-reset">Reset</button>
    </div>
    <div class="lg-row"><label><input type="checkbox" id="lg-fix"> Run with the agent's fix (attempt M-T2-03)</label></div>
    <div class="lg-row"><span class="lg-say" id="lg-say" aria-live="polite">Hold the button and speak, or type a command.</span><span class="lg-edits" id="lg-edits"></span></div>
    <details class="lg-help"><summary>What can I say?</summary><ul>
      <li>"Remove the settlement for case 4"</li><li>"Remove the bank credit for case 6"</li>
      <li>"Add a 300 rupee fee to case 7"</li><li>"Mark the settlement for case 4 as failed"</li>
      <li>"Use the agent's fix" or "use the original code"</li><li>"Show case 4" or "go to the benchmark"</li>
      <li>"Next" (walkthrough), "run it again", "reset"</li></ul>
      <p>Voice uses your browser's own speech recognition (Chrome, Edge, Safari). You can also type, or dictate with any dictation tool such as Wispr Flow.
      Your edits change the synthetic test data before LedgerGuard runs. The benchmark still scores against the original answer key, so an edit you make shows up there as an error. That is expected.</p></details>
  </div></div>`;

  function status(t) { const el = document.getElementById("lg-status"); if (el) el.textContent = t; }
  function say(t) { const el = document.getElementById("lg-say"); if (el) el.textContent = t; }
  function renderEdits() {
    document.getElementById("lg-edits").innerHTML = EDITS.map(e =>
      `<span>${LABEL[e.op]} on case ${lcNum(e.lc)}${e.op === "extra_fee" ? ` (₹${e.rupees})` : ""}</span>`).join("");
  }


  document.addEventListener("DOMContentLoaded", () => {
    document.head.insertAdjacentHTML("beforeend", `<style>${css}</style>`);
    document.body.insertAdjacentHTML("afterbegin", html);
    ready.catch(e => status("Could not start: " + e.message + ". Check your connection and reload."));
    const $ = id => document.getElementById(id);
    $("lg-op").onchange = () => { $("lg-amt").hidden = $("lg-op").value !== "extra_fee"; };
    $("lg-apply").onclick = () => addEdit($("lg-op").value, $("lg-case").value, Number($("lg-amt").value));
    $("lg-reset").onclick = reset;
    $("lg-fix").onchange = e => setFix(e.target.checked);
    const go = () => { const v = $("lg-cmd").value.trim(); if (v) { run(v); $("lg-cmd").value = ""; } };
    $("lg-go").onclick = go;
    $("lg-cmd").onkeydown = e => { if (e.key === "Enter") go(); };

    const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SR) return;
    const mic = $("lg-mic"); mic.hidden = false;
    const rec = new SR(); rec.lang = navigator.language || "en-US"; rec.interimResults = true; rec.continuous = true; // keep listening until the button is released
    let micReady = false, held = false, errored = false;
    let finalText = "";
    rec.onresult = e => { finalText = [...e.results].map(r => r[0].transcript).join(" "); $("lg-cmd").value = finalText; };
    rec.onend = () => { mic.setAttribute("aria-pressed", "false"); mic.textContent = "Hold to talk"; if (finalText) { run(finalText); $("lg-cmd").value = ""; finalText = ""; } else if (!errored) say("I didn't hear anything. Hold the button while you speak."); errored = false; };
    rec.onerror = e => (errored = true, say(e.error === "not-allowed" ? "Microphone access was blocked. You can type or dictate instead." : "Didn't catch that (" + e.error + "). Try again."));
    const start = async e => {
      e.preventDefault(); if (held) return; held = true; finalText = "";
      mic.setAttribute("aria-pressed", "true"); mic.textContent = "Listening... release to send";
      if (!micReady) { // open the mic once first: asks permission cleanly and avoids "audio-capture" errors
        try { (await navigator.mediaDevices.getUserMedia({ audio: true })).getTracks().forEach(t => t.stop()); micReady = true; await new Promise(r => setTimeout(r, 400)); } // let the device free up
        catch { held = false; mic.setAttribute("aria-pressed", "false"); mic.textContent = "Hold to talk"; return say("Microphone access was blocked. You can type or dictate instead."); }
      }
      if (held) try { rec.start(); } catch {}
    };
    const stop = () => { if (!held) return; held = false; try { rec.stop(); } catch {} };
    mic.addEventListener("pointerdown", start); mic.addEventListener("pointerup", stop); mic.addEventListener("pointerleave", stop);
    mic.addEventListener("keydown", e => { if ((e.key === " " || e.key === "Enter") && !e.repeat) start(e); });
    mic.addEventListener("keyup", e => { if (e.key === " " || e.key === "Enter") stop(); });
  });

  window.lgCommand = run; // exposed for testing
})();
