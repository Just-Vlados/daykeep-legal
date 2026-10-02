# daykeep-legal

Public legal and support site for the **DayKeep** iOS app, served via GitHub
Pages at **https://daykeep-legal.vilae.uk/**.

| Page | URL |
|------|-----|
| Privacy Policy | https://daykeep-legal.vilae.uk/privacy |
| Terms of Use   | https://daykeep-legal.vilae.uk/terms |
| Support        | https://daykeep-legal.vilae.uk/support |

## Structure

- `DayKeep-Privacy-Policy.md`, `DayKeep-Terms-of-Use.md` — the source documents (edit these).
- `privacy/`, `terms/`, `support/`, `index.html` — generated static pages that are served.
- `tools/build_legal_pages.py` — regenerates the HTML from the Markdown (stdlib only).
- `CNAME` — custom domain. `.nojekyll` — serve files as-is (no Jekyll build).

## Updating

Edit the Markdown source, then rebuild and commit:

```sh
python3 tools/build_legal_pages.py
git add -A && git commit -m "Update legal pages" && git push
```
