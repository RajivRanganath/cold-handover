#!/usr/bin/env python3
"""Render each evidence .md / .patch / .json file as a readable .html page beside it.

Usage: python3 render_evidence.py <evidence_dir>
Standard library only. Every piece of file content goes through html.escape.
"""
import html
import json
import os
import re
import sys
import urllib.parse

LIST_RE = re.compile(r'^(\s*)([-*]|\d+\.)\s+(.*)$')
TABLE_SEP_RE = re.compile(r'^\|?\s*:?-+:?\s*(\|\s*:?-+:?\s*)*\|?$')
TAG_T_RE = re.compile(r'^T\d+$')

CSS = """
*{box-sizing:border-box}
:root{--bg:#f6f7f6;--text:#16191c;--muted:#5b636b;--line:#d9dddb;--accent:#0f6b4f;
--code:rgba(15,23,28,.06);--add:rgba(46,160,67,.20);--del:rgba(218,54,51,.17);--hunk:rgba(15,107,79,.10)}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--bg:#111416;--text:#e8ebe9;
--muted:#9aa3a0;--line:#2b3134;--accent:#4fbf95;--code:rgba(255,255,255,.07);
--add:rgba(63,185,80,.22);--del:rgba(248,81,73,.22);--hunk:rgba(79,191,149,.12)}}
body{margin:0;background:var(--bg);color:var(--text);
font:16px/1.55 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
main{max-width:900px;margin:0 auto;padding:16px}
.top{font-size:14px;color:var(--muted);border-bottom:1px solid var(--line);padding-bottom:10px;
margin-bottom:20px;display:flex;flex-wrap:wrap;gap:6px 16px;align-items:baseline}
.top .path{color:var(--text);font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;overflow-wrap:anywhere}
a{color:var(--accent)}
h1,h2,h3,h4,h5,h6{line-height:1.25;margin:1.4em 0 .5em;overflow-wrap:anywhere}
p,ul,ol,blockquote{margin:.6em 0}
ul,ol{padding-left:1.4em}
li,p{overflow-wrap:anywhere}
blockquote{margin:.8em 0;padding:.1em 0 .1em 14px;border-left:3px solid var(--accent);color:var(--muted)}
code{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-size:.92em;
background:var(--code);padding:.1em .3em;border-radius:4px;overflow-wrap:anywhere}
pre{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-size:13px;line-height:1.45;
background:var(--code);border:1px solid var(--line);border-radius:6px;padding:12px;margin:.8em 0;
overflow-x:auto;white-space:pre;tab-size:2}
pre code{background:none;padding:0;border-radius:0;font-size:inherit;overflow-wrap:normal}
.tw{overflow-x:auto;margin:.8em 0}
table{border-collapse:collapse;font-size:14px}
th,td{border:1px solid var(--line);padding:6px 8px;text-align:left;vertical-align:top}
td{overflow-wrap:anywhere}
th{background:var(--code)}
hr{border:0;border-top:1px solid var(--line);margin:1.5em 0}
.patch span{display:block;width:max-content;min-width:100%}
.patch .file{font-weight:700}
.patch .meta{color:var(--muted)}
.patch .hunk{color:var(--accent);background:var(--hunk)}
.patch .add{background:var(--add)}
.patch .del{background:var(--del)}
"""


def esc(s):
    return html.escape(s, quote=True)


def inline(text):
    """Inline code and **bold**. Splitting happens on raw text, then each piece is escaped."""
    out = []
    for i, part in enumerate(re.split(r'`([^`]+)`', text)):
        if i % 2:
            out.append('<code>%s</code>' % esc(part))
        else:
            out.append(re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', esc(part)))
    return ''.join(out)


def split_row(line):
    s = line.strip()
    if s.startswith('|'):
        s = s[1:]
    if s.endswith('|') and not s.endswith('\\|'):
        s = s[:-1]
    return [c.strip() for c in re.split(r'(?<!\\)\|', s)]


def parse_list(lines, i):
    """Parse a bullet or numbered list starting at lines[i]; nested by indentation."""
    first = LIST_RE.match(lines[i])
    base = len(first.group(1))
    tag = 'ol' if first.group(2)[-1] == '.' else 'ul'
    out = ['<%s>' % tag]
    n = len(lines)
    while i < n:
        m = LIST_RE.match(lines[i])
        if not m or len(m.group(1)) != base:
            # A blank line may separate items of the same list.
            j = i
            while j < n and not lines[j].strip():
                j += 1
            m2 = LIST_RE.match(lines[j]) if j < n else None
            if not lines[i].strip() and m2 and len(m2.group(1)) == base:
                i = j
                continue
            break
        body = [inline(m.group(3))]
        i += 1
        while i < n:
            nxt = lines[i]
            m2 = LIST_RE.match(nxt)
            if m2 and len(m2.group(1)) > base:
                sub, i = parse_list(lines, i)
                body.append(sub)
            elif nxt.strip() and not m2 and nxt.startswith(' ' * (base + 1)):
                body.append(' ' + inline(nxt.strip()))
                i += 1
            else:
                break
        out.append('<li>%s</li>' % ''.join(body))
    out.append('</%s>' % tag)
    return ''.join(out), i


def is_block_start(line):
    s = line.strip()
    return (s.startswith(('```', '#', '>', '|')) or bool(LIST_RE.match(line))
            or bool(re.match(r'^(-{3,}|\*{3,}|_{3,})$', s)))


def md_to_html(text):
    lines = text.replace('\r\n', '\n').split('\n')
    n = len(lines)
    out = []
    i = 0
    while i < n:
        line = lines[i]
        s = line.strip()
        if not s:
            i += 1
            continue
        if s.startswith('```'):
            i += 1
            code = []
            while i < n and not lines[i].strip().startswith('```'):
                code.append(lines[i])
                i += 1
            i += 1  # skip closing fence (or end of file)
            out.append('<pre><code>%s</code></pre>' % esc('\n'.join(code)))
            continue
        m = re.match(r'^(#{1,6})\s+(.*)$', s)
        if m:
            level = len(m.group(1))
            out.append('<h%d>%s</h%d>' % (level, inline(m.group(2)), level))
            i += 1
            continue
        if re.match(r'^(-{3,}|\*{3,}|_{3,})$', s):
            out.append('<hr>')
            i += 1
            continue
        if s.startswith('|') and i + 1 < n and '|' in lines[i + 1] and TABLE_SEP_RE.match(lines[i + 1].strip()):
            head = split_row(s)
            i += 2
            rows = []
            while i < n and lines[i].strip().startswith('|'):
                rows.append(split_row(lines[i]))
                i += 1
            t = ['<div class="tw"><table><thead><tr>']
            t += ['<th>%s</th>' % inline(c) for c in head]
            t.append('</tr></thead><tbody>')
            for r in rows:
                t.append('<tr>' + ''.join('<td>%s</td>' % inline(c) for c in r) + '</tr>')
            t.append('</tbody></table></div>')
            out.append(''.join(t))
            continue
        if s.startswith('>'):
            quoted = []
            while i < n and lines[i].strip().startswith('>'):
                quoted.append(re.sub(r'^\s*>\s?', '', lines[i]))
                i += 1
            out.append('<blockquote>%s</blockquote>' % md_to_html('\n'.join(quoted)))
            continue
        if LIST_RE.match(line):
            block, i = parse_list(lines, i)
            out.append(block)
            continue
        para = [s]
        i += 1
        while i < n and lines[i].strip() and not is_block_start(lines[i]):
            para.append(lines[i].strip())
            i += 1
        out.append('<p>%s</p>' % inline(' '.join(para)))
    return '\n'.join(out)


def render_patch(text):
    rows = []
    for line in text.replace('\r\n', '\n').split('\n'):
        if line.startswith('diff --git'):
            cls = 'file'
        elif line.startswith(('+++', '---', 'index ', 'new file', 'deleted file', 'similarity', 'rename ')):
            cls = 'meta'
        elif line.startswith('+'):
            cls = 'add'
        elif line.startswith('-'):
            cls = 'del'
        elif line.startswith('@@'):
            cls = 'hunk'
        else:
            cls = ''
        # The newline sits inside each block span so pre does not add blank lines.
        rows.append('<span class="%s">%s\n</span>' % (cls, esc(line)) if cls else '<span>%s\n</span>' % esc(line))
    return '<pre class="patch">%s</pre>' % ''.join(rows)


def render_json(text):
    try:
        body = json.dumps(json.loads(text), indent=2, ensure_ascii=False)
    except (ValueError, RecursionError):
        body = text
    return '<pre>%s</pre>' % esc(body)


RENDERERS = {'.md': md_to_html, '.patch': render_patch, '.json': render_json}


def page(rel, raw_href, back_href, body):
    return (
        '<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        '<title>%s</title>\n<style>%s</style>\n</head>\n<body>\n<main>\n'
        '<div class="top"><span class="path">%s</span>'
        '<a href="%s">Raw file</a><a href="%s">Back to the case study</a></div>\n'
        '%s\n</main>\n</body>\n</html>\n'
    ) % (esc(rel), CSS, esc(rel), esc(raw_href, ), esc(back_href), body)


def back_link(rel):
    """Relative link from the file's folder to <site>/index.html, anchored to T* for files under a T* folder."""
    anchor = ''
    parts = rel.split('/')
    if len(parts) > 1 and TAG_T_RE.match(parts[0]):
        anchor = '#' + parts[0]
    return anchor


def main():
    if len(sys.argv) != 2:
        print('usage: python3 render_evidence.py <evidence_dir>', file=sys.stderr)
        return 2
    root = os.path.abspath(sys.argv[1])
    site_index = os.path.join(os.path.dirname(root), 'index.html')

    inputs = []
    for dp, dn, fn in os.walk(root):
        dn.sort()
        for f in sorted(fn):
            if f.endswith(('.md', '.patch', '.json')) and not f.endswith('.html'):
                inputs.append(os.path.join(dp, f))

    written = []
    counts = {}
    for src in inputs:
        rel = os.path.relpath(src, root).replace(os.sep, '/')
        ext = os.path.splitext(src)[1]
        with open(src, encoding='utf-8', errors='replace') as fh:
            text = fh.read()
        body = RENDERERS[ext](text)
        here = os.path.dirname(src)
        back = os.path.relpath(site_index, here).replace(os.sep, '/') + back_link(rel)
        doc = page(rel, os.path.basename(src), back, body)
        out_path = src + '.html'
        with open(out_path, 'w', encoding='utf-8') as fh:
            fh.write(doc)
        written.append((src, out_path))
        counts[ext] = counts.get(ext, 0) + 1

    print('rendered %d files: %s' % (len(written), ', '.join('%d %s' % (counts[e], e) for e in sorted(counts))))
    print('output dir: %s' % root)

    # Self-check 1: untrusted content renders escaped in every renderer.
    probe = '<script>alert(1)</script>'
    for name, rendered in (
        ('md', md_to_html(probe)),
        ('md-table', md_to_html('| a |\n|---|\n| %s |' % probe)),
        ('patch', render_patch(probe)),
        ('json-raw', render_json(probe)),
        ('json-valid', render_json(json.dumps(probe))),
    ):
        assert '<script' not in rendered, 'unescaped script from %s renderer' % name
        assert '&lt;script&gt;' in rendered, 'probe missing from %s renderer' % name

    # Self-check 2: every input has its .html, each output is a doctype page with no script tags.
    for src, out_path in written:
        assert os.path.isfile(out_path), 'missing output for %s' % src
        with open(out_path, encoding='utf-8') as fh:
            content = fh.read()
        assert content.startswith('<!doctype html>'), 'bad doctype in %s' % out_path
        assert '<script' not in content, 'script tag in %s' % out_path
    assert len(written) == len(inputs)
    print('self-check passed: %d inputs, %d outputs, escaping probes ok' % (len(inputs), len(written)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
