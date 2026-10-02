#!/usr/bin/env python3
"""Generate the DayKeep legal/support site (GitHub Pages) from the Markdown source.

Reads the filled Markdown legal documents and writes styled, self-contained,
theme-aware HTML pages served from this repo's GitHub Pages at
https://daykeep-legal.vilae.uk/. Also writes the landing and support pages.

Pure Python standard library — no third-party dependencies. Re-run after editing
any of the source Markdown docs:

    python3 tools/build_legal_pages.py
"""
import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
YEAR = "2026"
OWNER = "Vladislav Lapets"
CONTACT = "daykeep@vilae.uk"

# (source markdown file, output directory, short nav/title label)
DOC_PAGES = [
    ("DayKeep-Privacy-Policy.md", "privacy", "Privacy Policy"),
    ("DayKeep-Terms-of-Use.md", "terms", "Terms of Use"),
]

NAV = [("/privacy/", "Privacy"), ("/terms/", "Terms"), ("/support/", "Support")]

CSS = """
*{box-sizing:border-box}
:root{
  --bg:#ffffff;--fg:#1c1c1e;--muted:#6b6b70;--accent:#0B6E4F;
  --rule:#e6e6eb;--header:#f7f7f8;
}
@media (prefers-color-scheme:dark){
  :root{
    --bg:#000000;--fg:#f2f2f7;--muted:#9b9ba1;--accent:#35c491;
    --rule:#2a2a2e;--header:#121214;
  }
}
html{-webkit-text-size-adjust:100%}
body{
  margin:0;background:var(--bg);color:var(--fg);
  font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
  line-height:1.65;font-size:17px;
}
a{color:var(--accent);text-decoration:underline;text-underline-offset:2px}
.site-header{
  background:var(--header);border-bottom:1px solid var(--rule);
  padding:14px 20px;
}
.brand{
  font-weight:700;font-size:1.15rem;color:var(--accent);text-decoration:none;
  letter-spacing:-0.01em;
}
main{max-width:44rem;margin:0 auto;padding:28px 20px 8px}
h1{font-size:1.9rem;line-height:1.2;letter-spacing:-0.02em;margin:0.2em 0 0.6em}
h2{font-size:1.2rem;margin:1.9em 0 0.5em;letter-spacing:-0.01em}
p{margin:0.85em 0}
ul{margin:0.85em 0;padding-left:1.3em}
li{margin:0.4em 0}
strong{font-weight:600}
hr{border:0;border-top:1px solid var(--rule);margin:2em 0}
.site-footer{
  max-width:44rem;margin:0 auto;padding:24px 20px 40px;
  border-top:1px solid var(--rule);margin-top:28px;
  color:var(--muted);font-size:0.95rem;
}
.site-footer nav a{margin-right:1em}
.site-footer nav a[aria-current="page"]{color:var(--muted);text-decoration:none;font-weight:600}
.copyright{margin:0.8em 0 0}
.link-list{list-style:none;padding:0}
.link-list li{margin:0.6em 0;font-size:1.05rem}
"""


def render_inline(text):
    text = html.escape(text, quote=False)
    text = re.sub(r"\[([^\]]+)\]\((https?://[^)]+)\)", r'<a href="\2">\1</a>', text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\*(.+?)\*", r"<em>\1</em>", text)
    return text


def markdown_to_body(md):
    """Convert the limited Markdown used in these docs to an HTML body.

    Supports: #/## headings, --- rules, - bullet lists, paragraphs (single
    newlines within a block become <br>), and inline links/**bold**/*italic*.
    """
    title = None
    out = []
    for block in re.split(r"\n\s*\n", md.strip("\n")):
        blines = [l for l in block.split("\n") if l.strip()]
        if not blines:
            continue
        first = blines[0].strip()
        if first == "---":
            out.append("<hr>")
        elif first.startswith("# "):
            t = first[2:].strip()
            title = title or t
            out.append(f"<h1>{render_inline(t)}</h1>")
        elif first.startswith("## "):
            out.append(f"<h2>{render_inline(first[3:].strip())}</h2>")
        elif all(l.strip().startswith("- ") for l in blines):
            items = "".join(f"<li>{render_inline(l.strip()[2:])}</li>" for l in blines)
            out.append(f"<ul>{items}</ul>")
        else:
            out.append("<p>" + "<br>".join(render_inline(l.strip()) for l in blines) + "</p>")
    return title, "\n".join(out)


def page(title, body, current_path):
    links = []
    for href, label in NAV:
        cur = ' aria-current="page"' if href == current_path else ""
        links.append(f'<a href="{href}"{cur}>{label}</a>')
    nav = " ".join(links)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)} · DayKeep</title>
<meta name="robots" content="index, follow">
<style>{CSS}</style>
</head>
<body>
<header class="site-header"><a class="brand" href="/">DayKeep</a></header>
<main>
{body}
</main>
<footer class="site-footer">
<nav>{nav}</nav>
<p class="copyright">© {YEAR} {html.escape(OWNER)}</p>
</footer>
</body>
</html>
"""


def write(path, text):
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")
    print(f"wrote {path}")


def main():
    for src, outdir, _ in DOC_PAGES:
        title, body = markdown_to_body((ROOT / src).read_text(encoding="utf-8"))
        write(f"{outdir}/index.html", page(title, body, f"/{outdir}/"))

    support_body = (
        "<h1>DayKeep Support</h1>"
        "<p>Need help with DayKeep, or have a question? Email us and we'll get back "
        "to you — usually within a few working days.</p>"
        f'<p><a href="mailto:{CONTACT}">{CONTACT}</a></p>'
        "<p>DayKeep runs entirely on your device. There are no accounts to recover "
        "and nothing is stored on our servers. Many common questions are answered in "
        "the app under <strong>Settings &rarr; Help &amp; FAQ</strong>.</p>"
    )
    write("support/index.html", page("Support", support_body, "/support/"))

    index_body = (
        "<h1>DayKeep</h1>"
        "<p>DayKeep is a UK contractor take-home calculator for iPhone. These pages "
        "hold the app's legal and support information.</p>"
        '<ul class="link-list">'
        '<li><a href="/privacy/">Privacy Policy</a></li>'
        '<li><a href="/terms/">Terms of Use</a></li>'
        '<li><a href="/support/">Support</a></li>'
        "</ul>"
    )
    write("index.html", page("DayKeep", index_body, "/"))


if __name__ == "__main__":
    main()
