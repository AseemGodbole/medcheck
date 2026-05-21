# Static Medication Checker Demo

This is a static demo you can host on GitHub Pages. It runs an in-browser ACB scoring
and a simple Beers quick-check using the included JSON datasets — no backend required.

To publish on GitHub Pages:

1. Copy the `web_static` folder into a branch named `gh-pages` or set your repository's Pages source to the folder (GitHub supports `docs/` too).
2. Commit and push.
3. Enable GitHub Pages in repository settings and point to the `gh-pages` branch (or `docs/` folder).

Local preview:

Open `index.html` in a browser (some browsers block module JSON imports when opened via `file://`). If that happens, use a tiny static server:

```bash
# Python 3
cd calculators/web_static
python -m http.server 8000
# open http://localhost:8000
```

Notes:
- This is a demonstration-only frontend. The datasets included are a small subset for demo purposes.
- Do not use this as clinical decision software.
