# Toolora

Static site, no build step needed to deploy. All 30 tools are included in English. Arabic (right-to-left, in `ar/`) covers the homepage and the About, Privacy, Terms and Contact pages; all 30 tool pages are translated as well. Have a native Arabic editor review the Arabic text before launch. See TEST-REPORT.md: nothing has been tested in a browser yet, so test before launch.

## Before launch
1. Open `build.py`, set `SITE` to your real domain, then run `python3 build.py` to regenerate all pages, the sitemap and robots.txt.

## Deploy
- **GitHub Pages:** push this folder to a repository, then Settings → Pages → deploy from the main branch, root folder.
- **Vercel:** import the repository, framework preset "Other", no build command, output directory `.`.
- **Custom domain:** add the domain in the host's settings, create the DNS records it shows (CNAME for `www`, A/ALIAS records for the root domain), wait for HTTPS, then update `SITE` and rebuild.

## Adsterra
Slots are `banner`, `inline`, `native` and `footer` in `ADS` at the top of `build.py`. They are empty until you paste the code Adsterra gives you after approval; empty slots output nothing. Rebuild afterwards. Add your `ads.txt` line to `ads.txt`. If you serve visitors in regions that require cookie consent, add a consent tool before enabling ads, and update the Privacy Policy to match what you enable.

## Search Console
Add your site at search.google.com/search-console, verify ownership, open Sitemaps, and submit `sitemap.xml`.

## Known limits
- `404.html` uses relative paths, so on deep URLs or GitHub Pages project sites (`user.github.io/repo/`) its styling may not load. A custom domain at the site root avoids this.
- The QR and PDF tools load libraries from the jsDelivr CDN without integrity hashes and need an internet connection.
