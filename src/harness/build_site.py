"""Build portfolio/site/ (static case study plus the live demo) from portfolio/site-data.json and the evidence pack."""
import json, shutil, datetime, subprocess, zipfile
from html import escape
from pathlib import Path

P = Path("/path/to/tms-work/portfolio")
SITE = P / "site"
SITE_URL = "https://rajivranganath.github.io/cold-handover/"  # where the site is published; used for link previews
FAVICON = """<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='7' fill='%230f6b4f'/%3E%3Cpath d='M9 17l5 5 9-11' fill='none' stroke='white' stroke-width='3.5' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E">"""
d = json.loads((P / "site-data.json").read_text())


def e(s):  # escape + house style: no em/en dashes on the page
    return escape(str(s).replace("—", ", ").replace("–", "-"))


def para(s):
    return "".join(f"<p>{e(x)}</p>" for x in str(s).split("\n\n") if x.strip())


# Real excerpt from attempt M-T2-03's change to matcher.py (see evidence/T2/M-T2-03/agent_changes.patch).
EXCERPT = """# Only processed settlements take part.
# A pending or failed record must not make a
# processed one look duplicated or conflicting.
processed = [
    s for s in batch.settlements
    if s.status == SettlementStatus.PROCESSED
]

# ...
# 2. No processed settlement. Pending or failed
# settlements have paid out nothing, so they are
# reported as context but never close the payment."""

pj, tasks = d["project"], d["tasks"]
total_pass = sum(t["passed"] for t in tasks)
total = sum(t["attempts"] for t in tasks)

decisions = "".join(
    f'<li><p class="dec">{e(x["decision"])}</p>'
    + f'<p class="src">Source: {e(x["source"])}</p></li>'
    for i, x in enumerate(pj["documented_design_decisions"]))

exp_decisions = "".join(
    f'<li><p class="dec">{e(x["decision"])}</p>'
    + "</li>"
    for i, x in enumerate(d["experiment_decisions_on_record"]))


def trial(t, tr):
    checks = "".join(f'<li>{"✓" if ok else "✗"} {e(d["check_labels"][k])}</li>' for k, ok in tr["checks"].items())
    files = "".join(f"<li><code>{e(f)}</code></li>" for f in tr["files_changed"]) or "<li>No files changed (by design)</li>"
    ev = "".join(f'<a href="evidence/{e(tr["evidence_folder"])}{e(f)}.html">{e(f)}</a>' for f in tr["evidence_files"])
    t1 = (f'<p>Backed up committed results before running: <strong>{"yes" if tr["backed_up_before_running_benchmark"] else "no"}</strong></p>'
          if t["id"] == "T1" else "")
    if "handled_unscored_combined_case" in tr:
        t1 += f'<p>Also handled a harder case the report never mentioned (not scored): <strong>{"yes" if tr["handled_unscored_combined_case"] else "no"}</strong></p>'
    word = "Passed" if tr["outcome"] == "PASS" else "Failed"
    return f"""<details class="attempt"><summary><span class="mark">{"✓" if word == "Passed" else "✗"} {word}</span>
<span class="lbl">{e(tr["label"])}</span><span class="dur">{e(tr["duration"])}</span></summary>
<div class="body"><p class="sum">{e(tr["summary"])}</p>{t1}
<div class="cols"><div><h4>Checks</h4><ul class="checks">{checks}</ul></div>
<div><h4>Files changed</h4><ul class="files">{files}</ul></div></div>
<p class="ev">Evidence: {ev}</p></div></details>"""


task_html = "".join(f"""<article class="task" id="{t["id"]}">
<div class="task-head"><div><h3>{e(t["title"])}</h3><p>{e(t["plain"])}</p>
<p class="muted">Why it matters: {e(t["why_it_matters"])}</p>
{'<p class="note">Held out: never used before measurement.</p>' if t["id"] == "T3" else ""}{'<p class="note">Round 2: a harder task added after round 1, built on a real bug found in the original code.</p>' if t["id"] == "T4" else ""}</div>
<div class="score"><span class="big">{t["passed"]} of {t["attempts"]}</span><span>passed</span>
<span class="muted">median {e(t["median_duration"])}<br>range {e(t["duration_range"])}</span>
<a href="evidence/{e(t["prompt_file"])}.html">Task prompt</a></div></div>
{"".join(trial(t, tr) for tr in t["trials"])}</article>""" for t in tasks)


links = [f'<a href="{e(d["owner"]["github"])}">GitHub</a>', f'<a href="{e(pj["url"])}">LedgerGuard source</a>']

html = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Cold Handover</title>
<meta name="description" content="{e(d["framing"])}">
<meta property="og:title" content="Cold Handover">
<meta property="og:description" content="{e(d["framing"])}">
<meta property="og:type" content="website">
<meta property="og:url" content="{SITE_URL}">
<meta property="og:image" content="{SITE_URL}og.png">
<meta name="twitter:card" content="summary_large_image">
{FAVICON}
<style>
:root{{--bg:#f6f7f6;--fg:#16191c;--muted:#5b636b;--line:#d9dddb;--panel:#eceeed;--accent:#0f6b4f;--code:#1d2226;--codefg:#e4e8e6}}
@media (prefers-color-scheme:dark){{:root{{--bg:#111416;--fg:#e8ebe9;--muted:#9aa3a0;--line:#2b3134;--panel:#181c1e;--accent:#4fbf95;--code:#0b0d0e;--codefg:#d6dcd9}}}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--fg);font:17px/1.6 ui-sans-serif,-apple-system,"Segoe UI",Roboto,sans-serif}}
main{{max-width:1080px;margin:0 auto;padding:0 16px}}
a{{color:var(--accent);text-underline-offset:3px}}
a:focus-visible,summary:focus-visible{{outline:2px solid var(--accent);outline-offset:3px}}
h1{{font-size:clamp(2.4rem,5vw,3.5rem);line-height:1.05;letter-spacing:-.03em;margin:0 0 1rem}}
h2{{font-size:clamp(1.6rem,3.5vw,2.2rem);letter-spacing:-.02em;line-height:1.15;margin:0 0 1.25rem}}
h3{{font-size:1.25rem;margin:0 0 .5rem}} h4{{font-size:.9rem;margin:0 0 .4rem;color:var(--muted)}}
p{{max-width:65ch}} .muted{{color:var(--muted);font-size:.95rem}}
code,pre{{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:.85rem}}
section{{padding:72px 0;border-top:1px solid var(--line)}}
.hero{{display:grid;grid-template-columns:minmax(0,.9fr) minmax(0,1.1fr);gap:48px;align-items:center;padding:96px 0 72px}}
.hero>*,.task-head>*,.cols>*{{min-width:0}}
.who{{color:var(--muted);margin:0 0 .75rem}}
.lede{{font-size:1.2rem}}
.cta{{display:flex;gap:12px;flex-wrap:wrap;margin-top:1.5rem}}
.btn{{display:inline-block;padding:.65rem 1.1rem;border-radius:8px;border:1px solid var(--accent);text-decoration:none;font-weight:600;white-space:nowrap}}
.btn.primary{{background:var(--accent);color:var(--bg)}}
.btn:active{{transform:translateY(1px)}}
figure{{margin:0}} pre{{background:var(--code);color:var(--codefg);padding:20px;border-radius:8px;overflow-x:auto;line-height:1.55;margin:0}}
figcaption{{color:var(--muted);font-size:.85rem;margin-top:.6rem}}
.stats{{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));justify-content:start;gap:12px 40px;padding:28px 0;border-top:1px solid var(--line)}}
.stats div{{display:flex;flex-direction:column}} .stats strong{{font-size:1.6rem}} .stats span{{color:var(--muted);font-size:.9rem}}
blockquote{{margin:1.5rem 0 2rem;padding-left:20px;border-left:3px solid var(--accent);font-size:1.25rem;max-width:60ch}}
.decisions{{list-style:none;padding:0;display:grid;grid-template-columns:1fr 1fr;gap:32px 48px}}
.decisions .dec{{font-weight:600;margin:0 0 .4rem}} .src{{color:var(--muted);font-size:.85rem;margin:.3rem 0 0}}
.why p{{margin:.3rem 0}}
.steps{{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;padding:0;list-style:none;margin:1.5rem 0 2.5rem}}
.steps li{{background:var(--panel);border-radius:8px;padding:16px;font-weight:600}}
.plain{{padding-left:1.2rem}} .plain li{{margin:.4rem 0;max-width:65ch}}
.task{{padding:40px 0;border-top:1px solid var(--line)}} .task:first-of-type{{border-top:0;padding-top:0}}
.task-head{{display:grid;grid-template-columns:1fr 240px;gap:32px;margin-bottom:1.25rem}}
.score{{display:flex;flex-direction:column;gap:4px}} .big{{font-size:2.2rem;font-weight:700;line-height:1;color:var(--accent)}}
.note{{font-size:.9rem;font-weight:600}}
.attempt{{border-top:1px solid var(--line)}} .attempt:last-child{{border-bottom:1px solid var(--line)}}
.attempt summary{{display:grid;grid-template-columns:7rem 1fr auto;gap:16px;padding:12px 4px;cursor:pointer;list-style:none}}
.attempt summary::-webkit-details-marker{{display:none}}
.attempt summary:hover{{background:var(--panel)}}
.mark{{color:var(--accent);font-weight:700}} .lbl{{font-family:ui-monospace,Menlo,monospace}} .dur{{color:var(--muted)}}
.body{{padding:4px 4px 20px}} .sum{{font-weight:600}}
.cols{{display:grid;grid-template-columns:1fr 1fr;gap:24px}}
.checks,.files{{padding-left:0;list-style:none;margin:0;font-size:.92rem}} .checks li,.files li{{margin:.2rem 0}} .files code{{overflow-wrap:anywhere}}
.ev{{display:flex;flex-wrap:wrap;gap:6px 14px}} .ev a{{font-size:.92rem}}
footer{{border-top:1px solid var(--line);padding:40px 0 64px;display:flex;gap:24px;flex-wrap:wrap;color:var(--muted)}}
@media (max-width:767px){{.hero,.task-head,.decisions,.cols{{grid-template-columns:1fr}}.hero{{padding:56px 0 40px;gap:32px}}
.steps{{grid-template-columns:1fr 1fr}}.stats{{grid-template-columns:1fr 1fr}}.attempt summary{{grid-template-columns:5.5rem 1fr auto;gap:8px}}}}
@media (prefers-reduced-motion:no-preference){{.btn,.attempt summary{{transition:background .2s,transform .1s}}}}
</style></head><body><main>

<header class="hero"><div>
<p class="who">{e(d["owner"]["name"])}</p>
<h1>Cold Handover</h1>
<p class="lede">{e(d["framing"])}</p>
<div class="cta"><a class="btn primary" href="ledgerguard/">Try LedgerGuard live</a><a class="btn" href="#tasks">See every attempt</a></div>
</div>
<figure><pre><code>{e(EXCERPT)}</code></pre>
<figcaption>From attempt M-T2-03: the agent's own change to <code>matcher.py</code>, written with no one to ask (rewrapped to fit; lines between omitted). <a href="evidence/T2/M-T2-03/agent_changes.patch.html">Full diff</a></figcaption></figure>
</header>

<div class="stats" aria-label="Results">
<div><strong>{total_pass} of {total}</strong><span>attempts passed</span></div>
{"".join(f'<div><strong>{t["passed"]} of {t["attempts"]}</strong><span>{e(t["id"])}: {e(t["title"])}</span></div>' for t in tasks)}
</div>
<p class="muted">The agent results above are recorded. The <a href="ledgerguard/">LedgerGuard demo</a> runs live in your browser.</p>

<section id="ledgerguard"><h2>LedgerGuard, and the decisions behind it</h2>
<p>{e(pj["one_line"])} It checks that the money from every payment actually arrived, and refuses to close anything it cannot prove.</p>
<blockquote>{e(pj["core_claim_quote"])}</blockquote>
<ul class="decisions">{decisions}</ul>
</section>

<section id="method"><h2>Putting my own handover to the test</h2>
<p>{e(d["method"])}</p>
<ol class="steps"><li>Tasks fixed in advance</li><li>A fresh, sandboxed agent each time, with nobody to ask</li><li>Five attempts per task</li><li>Hidden checks it could not see</li></ol>
<p class="muted">{e(d["agent"]["setup"])} Agent: {e(d["agent"]["tool"])}, model {e(d["agent"]["model"])}.</p>
<h3>Decisions I made along the way</h3>
<ul class="decisions">{exp_decisions}</ul>
</section>

<section id="tasks"><h2>{len(tasks)} tasks, {total} attempts</h2>
<p class="muted">Open any attempt for what it changed, which checks it passed, and the full transcript.</p>
{task_html}</section>


<section id="limits"><h2>What this does and does not show</h2>
<p>{e(d["limitation"])}</p>
<p class="muted">{e(d["framing_note"])}</p>
<h3>It cannot claim</h3><ul class="plain">{"".join(f"<li>{e(x)}</li>" for x in d["cannot_claim"])}</ul>
<h3>Disclosures</h3><ul class="plain">{"".join(f"<li>{e(x)}</li>" for x in d["disclosures"])}</ul>
<p><a href="evidence/results.md.html">Full results table</a></p>
</section>

<footer>{"".join(links)}<span>Last updated {datetime.date.today():%-d %B %Y}</span></footer>
</main></body></html>
"""
assert "—" not in html and "–" not in html
SITE.mkdir(exist_ok=True)
ev = SITE / "evidence"  # generated copy: rebuild from scratch (source prompts are read-only)
if ev.exists():
    subprocess.run(["chmod", "-R", "u+w", ev], check=True); shutil.rmtree(ev)
shutil.copytree(P / "evidence-pack", ev, copy_function=shutil.copyfile)
(ev / "site-data.json").unlink(missing_ok=True)  # internal build input, not evidence
subprocess.run(["python3", str(Path(__file__).with_name("render_evidence.py")), str(ev)], check=True, stdout=subprocess.DEVNULL)
(SITE / "index.html").write_text(html)
for f in ("README.md", "og.png", ".gitattributes"):  # repo README and link-preview image
    if (P.parent / "demo-src" / f).exists():
        shutil.copyfile(P.parent / "demo-src" / f, SITE / f)

# Live LedgerGuard demo: the original dashboard + package, run in the browser by demo-src/demo.js.
W = P.parent
LG = SITE / "ledgerguard"; LG.mkdir(exist_ok=True)
dash = (W / "snapshot/ledgerguard/frontend/index.html").read_text()
for a, b in [("<title>LedgerGuard</title>", '<title>LedgerGuard live demo</title>\n' + FAVICON + '\n<script src="demo.js"></script>'),
             ("fetch('/api/state').then(r =>", "(window.lgRender = () => fetch('/api/state').then(r =>"),
             ("  renderDetail();\n}).catch(e => {", "  renderDetail();\n  window.lgAfterRender && window.lgAfterRender(s);\n}).catch(e => {"),
             ("});\n</script>\n</body>", "}))();\n</script>\n</body>")]:
    assert dash.count(a) == 1, a
    dash = dash.replace(a, b)
(LG / "index.html").write_text(dash)
for f in ("demo.js", "lg_demo.py"):
    shutil.copyfile(W / "demo-src" / f, LG / f)
# Reference copies of the experiment and build source, with local paths and username replaced.
SRC = SITE / "src"
if SRC.exists():
    shutil.rmtree(SRC)
SOURCES = {"harness": ["run_attempt.sh", "run_attempt_r2.sh", "run_schedule.sh", "sandbox.sb.tmpl", "shims/mktemp", "aggregate.py",
                       "build_public_evidence.py", "build_site_data.py", "render_evidence.py", "build_site.py"],
           "demo-src": ["demo.js", "lg_demo.py"], "protocol": ["protocol-lock.md", "schedule.txt"],
           "protocol-r2": ["protocol-lock.md", "schedule.txt"]}
for folder, files in SOURCES.items():
    for f in files:
        dst = SRC / {"demo-src": "demo", "protocol": "protocol/round1", "protocol-r2": "protocol/round2"}.get(folder, folder) / f
        dst.parent.mkdir(parents=True, exist_ok=True)
        text = (W / folder / f).read_text().replace("/path/to/tms-work", "/path/to/tms-work").replace("/path/to/home", "/path/to/home")
        dst.write_text(text.replace("rajiv", "USERNAME") if f == "build_public_evidence.py" else text)  # only that script names the local username
shutil.copyfile(W / "demo-src/SRC_README.md", SRC / "README.md")


def zip_pkg(root, out):
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted((root / "ledgerguard").rglob("*")):
            rel = f.relative_to(root)
            if f.is_file() and not {"tests", "frontend", "outputs", "__pycache__"} & set(rel.parts):
                z.write(f, rel)
zip_pkg(W / "snapshot", LG / "ledgerguard.zip")
# The agent's fix (attempt M-T2-03): a copy of the snapshot with its patch applied. A patch that fails to apply fails the build.
import tempfile
with tempfile.TemporaryDirectory() as tmp:
    shutil.copytree(W / "snapshot/ledgerguard", Path(tmp) / "ledgerguard", copy_function=shutil.copyfile)
    subprocess.run(["chmod", "-R", "u+w", tmp], check=True)
    subprocess.run(["git", "apply", "--verbose", W / "portfolio/evidence-pack/T2/M-T2-03/agent_changes.patch"], cwd=tmp, check=True)
    zip_pkg(Path(tmp), LG / "ledgerguard-fixed.zip")
print("wrote", SITE / "index.html")
