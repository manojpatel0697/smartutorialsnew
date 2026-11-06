# Smart Tutorials website

```
site/       Website source: the HTML pages, assets/ (CSS, JS, fonts, icons), images/, robots.txt, sitemap.xml
scripts/    pages.py (generates the HTML pages), build.mjs, check.mjs, serve.mjs
docs/       DEVELOPER-GUIDE.md (everything for the developer), CLIENT-HANDOVER.md (for the client), and the proposal
archive/    Git history bundle of the client release
dist/       Built website, created by `npm run build`. Upload this folder to the host. Never edit it.
```

## Editing
- Page text, header and footer: edit `scripts/pages.py`, then run `npm run pages` (needs Python). It rewrites the pages in `site/`.
- Styles and scripts: edit `site/assets/site.css` and `site/assets/site.js` directly.

## Commands (Node 18+, no packages to install)
- `npm test` builds `dist/` and checks links, images, SEO tags and claims.
- `npm run serve` previews at http://127.0.0.1:5510/.

## Hosting
`vercel.json` sets the build command `npm run build` and the output directory `dist`. Cloudflare Pages and Netlify read the generated `dist/_headers`.

To restore the git history: `git clone archive/smart-tutorials-git-history.bundle smart-tutorials`.
