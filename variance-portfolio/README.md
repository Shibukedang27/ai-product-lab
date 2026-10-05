# Freelancing portfolio demos — Mithilesh Kodali / Variance

Three self-contained demos for freelancing outreach. Web work is branded **Variance**. No API keys or secrets required.

| Demo | Path | One-line description |
|------|------|----------------------|
| **Variance landing page** | [`variance-landing/`](variance-landing/) | Mobile-first café landing page (hero, services, about, CTA form) with footer credit “Built by Variance”. |
| **FAQ chatbot** | [`faq-chatbot/`](faq-chatbot/) | Embeddable vanilla-JS FAQ widget with hours/pricing/contact answers and lead capture (console / thank-you). |
| **Data cleaning** | [`data-cleaning/`](data-cleaning/) | Messy → clean CSV pipeline: synthetic sample + `python3 clean.py` → cleaned output. |

## Quick start

```bash
# Landing page (open in browser)
xdg-open variance-landing/index.html   # or: open / start

# FAQ chatbot demo page
xdg-open faq-chatbot/index.html

# Data cleaning
cd data-cleaning && python3 clean.py
```

Each subfolder has its own README with deploy notes (static host for the two web demos).

## GitHub

Live in the public repo: [Shibukedang27/ai-product-lab](https://github.com/Shibukedang27/ai-product-lab) under [`variance-portfolio/`](https://github.com/Shibukedang27/ai-product-lab/tree/main/variance-portfolio).

| Demo | Browse | Raw HTML |
|------|--------|----------|
| Landing | [blob](https://github.com/Shibukedang27/ai-product-lab/blob/main/variance-portfolio/variance-landing/index.html) | [raw](https://raw.githubusercontent.com/Shibukedang27/ai-product-lab/main/variance-portfolio/variance-landing/index.html) |
| FAQ chatbot | [blob](https://github.com/Shibukedang27/ai-product-lab/blob/main/variance-portfolio/faq-chatbot/index.html) | [raw](https://raw.githubusercontent.com/Shibukedang27/ai-product-lab/main/variance-portfolio/faq-chatbot/index.html) |

> Tip: raw HTML won’t run linked CSS/JS from `raw.githubusercontent.com`. Use the blob pages to share, or enable GitHub Pages / open the folder locally. For a single-file preview you can use something like `https://htmlpreview.github.io/?https://github.com/Shibukedang27/ai-product-lab/blob/main/variance-portfolio/variance-landing/index.html`.

