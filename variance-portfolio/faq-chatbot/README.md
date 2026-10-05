# FAQ chatbot demo — Variance

Embeddable FAQ chatbot widget (vanilla HTML/CSS/JS) for a sample business: **Roast Lane Café**.

## Features

- Floating chat launcher + panel
- Preloaded Q&A: hours, pricing, contact, Wi-Fi, bookings, dietary notes
- Quick-reply chips
- Lead capture (name/email) → thank-you message + `console.log` (no backend)
- Footer credit inside the widget: **Built by Variance**

## How to open / demo

```bash
# From this folder — no build step
open index.html          # macOS
xdg-open index.html      # Linux
start index.html         # Windows
```

Or:

```bash
python3 -m http.server 8081
# visit http://localhost:8081
```

1. Click the chat bubble (bottom-right).
2. Ask “What are your hours?” or tap a chip.
3. Use **Leave my details**, submit name/email, and check the browser console for the lead payload.

## Embed on another page

Copy `chatbot.js` + widget CSS rules (or load `styles.css`), add:

```html
<div id="variance-faq-root"></div>
<script src="chatbot.js"></script>
<script>
  VarianceFAQ.init({ brand: "Your Business", accent: "#c45c26" });
</script>
```

## Deploy notes

Fully static. No API keys. Safe for GitHub Pages / Netlify / Vercel static hosting.
