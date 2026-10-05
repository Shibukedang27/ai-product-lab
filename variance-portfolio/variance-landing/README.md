# Roast Lane Café — Variance landing page demo

Polished single-page landing site for a fictional Hyderabad specialty café. Built as a **Variance** freelancing portfolio piece: mobile-first layout, hero, services/menu, about + hours, and a non-functional contact form.

## How to open

No build step. Open the file in a browser:

```bash
# From this folder
open index.html          # macOS
xdg-open index.html      # Linux
start index.html         # Windows
```

Or serve locally:

```bash
python3 -m http.server 8080
# then visit http://localhost:8080
```

## Files

| File | Role |
|------|------|
| `index.html` | Structure & content |
| `styles.css` | Mobile-first styling |
| `script.js` | Nav toggle + form thank-you (logs to console) |

## Branding

Footer credit: **Built by Variance**.

## Deploy notes

Static only — drop the folder on Netlify, Vercel, GitHub Pages, or any static host. Google Fonts load from the CDN; offline viewers still work with system fonts as fallbacks.
