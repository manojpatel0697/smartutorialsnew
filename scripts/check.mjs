// Checks the built site in dist/ and exits with an error if anything is wrong. Run: npm test
import { existsSync, readFileSync, readdirSync, statSync } from 'node:fs';
import { dirname, join, relative, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const dist = process.argv[2] ? resolve(process.argv[2]) : join(root, 'dist');
if (!existsSync(dist)) { console.error('dist/ not found. Run: npm run build'); process.exit(1); }

const SITE = 'https://smartstudycenters.com';
const PHONE = '+919731045709';
const MAX_IMAGE_KB = 300;
// Claims the coaching advertising rules make risky. Add proof and consent before allowing any of these.
const BANNED = [/best tuition/i, /100\s*%\s*(guarantee|guaranteed|selection|placement|job)/i, /no\.?\s*1\b/i, /top[- ]ranked/i, /guaranteed (marks|rank|result|selection|admission)/i, /we guarantee/i];
const NOT_PUBLIC = ['docs', 'archive', 'scripts', 'site', 'DEVELOPER-GUIDE.md', 'CLIENT-HANDOVER.md', 'package.json', 'vercel.json'];

const errors = [];
const fail = (file, msg) => errors.push(`${file}: ${msg}`);
const walk = (d) => readdirSync(d).flatMap((n) => {
  const p = join(d, n);
  return statSync(p).isDirectory() ? walk(p) : [p];
});
const decode = (s) => s.replace(/&amp;/g, '&').replace(/&nbsp;/g, ' ').replace(/&#39;/g, "'").replace(/&quot;/g, '"');
const attr = (tag, name) => (tag.match(new RegExp(`\\s${name}="([^"]*)"`)) || [])[1];

const files = walk(dist);
const pages = files.filter((f) => f.endsWith('.html'));
const docs = Object.fromEntries(pages.map((f) => [f, readFileSync(f, 'utf8')]));
const idsIn = (html) => new Set([...html.matchAll(/\sid="([^"]+)"/g)].map((m) => m[1]));

for (const name of NOT_PUBLIC) {
  if (existsSync(join(dist, name))) fail('dist', `must not publish ${name}`);
}
for (const f of files) {
  if (/\.(webp|jpe?g|png)$/.test(f) && statSync(f).size > MAX_IMAGE_KB * 1024) {
    fail(relative(dist, f), `image is over ${MAX_IMAGE_KB} KB`);
  }
}

const icons = readFileSync(join(dist, 'assets/icons.svg'), 'utf8');
const iconIds = idsIn(icons);
const css = readFileSync(join(dist, 'assets/site.css'), 'utf8');
for (const [, u] of css.matchAll(/url\(([^)"']+)\)/g)) {
  if (!existsSync(join(dist, 'assets', u))) fail('assets/site.css', `missing font ${u}`);
}

for (const [file, html] of Object.entries(docs)) {
  const name = relative(dist, file);
  const is404 = name === '404.html';
  const title = decode((html.match(/<title>([^<]*)<\/title>/) || [])[1] || '');
  const desc = decode((html.match(/<meta name="description" content="([^"]*)"/) || [])[1] || '');
  const h1s = (html.match(/<h1[\s>]/g) || []).length;
  const canonical = (html.match(/<link rel="canonical" href="([^"]+)"/) || [])[1];

  if (!/<html lang="en-IN">/.test(html)) fail(name, 'missing page language');
  if (!title || title.length > 60) fail(name, `title must be 1 to 60 characters, is ${title.length}`);
  if (desc.length < 50 || desc.length > 160) fail(name, `description must be 50 to 160 characters, is ${desc.length}`);
  if (h1s !== 1) fail(name, `needs exactly one h1, has ${h1s}`);
  if (is404) {
    if (!/content="noindex"/.test(html)) fail(name, 'must be noindex');
  } else {
    const want = `${SITE}/${name === 'index.html' ? '' : name}`;
    if (canonical !== want) fail(name, `canonical should be ${want}, is ${canonical}`);
    if (!html.includes('property="og:image"')) fail(name, 'missing share image');
  }

  // The security policy blocks inline code, so any of these would silently break on the live site.
  if (/\sstyle="/.test(html)) fail(name, 'inline style attribute');
  if (/\son[a-z]+="/.test(html)) fail(name, 'inline event handler');
  for (const m of html.matchAll(/<script\b([^>]*)>/g)) {
    if (!/type="application\/ld\+json"/.test(m[1]) && !/\ssrc="assets\//.test(m[1])) fail(name, `unexpected script: ${m[0]}`);
  }
  if (/<style[\s>]/.test(html)) fail(name, 'inline style block');
  if (/fonts\.googleapis|googletagmanager/.test(html)) fail(name, 'third-party request on page load');

  for (const m of html.matchAll(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/g)) {
    try { JSON.parse(m[1]); } catch { fail(name, 'invalid structured data'); }
  }

  for (const m of html.matchAll(/<img\b[^>]*>/g)) {
    const src = attr(m[0], 'src');
    if (!attr(m[0], 'alt')) fail(name, `image without alt text: ${src}`);
    if (!attr(m[0], 'width') || !attr(m[0], 'height')) fail(name, `image without size: ${src}`);
    if (!src || !existsSync(join(dist, src))) fail(name, `missing image: ${src}`);
    for (const c of (attr(m[0], 'srcset') || '').split(',').map((x) => x.trim().split(' ')[0]).filter(Boolean)) {
      if (!existsSync(join(dist, c))) fail(name, `missing image size: ${c}`);
    }
  }

  // Every indexable page must be reachable from the home page and listed in the sitemap
  if (!is404 && name !== 'index.html') {
    if (!docs[join(dist, 'index.html')].includes(`href="${name}"`)) fail(name, 'not linked from the home page');
    if (!readFileSync(join(dist, 'sitemap.xml'), 'utf8').includes(`${SITE}/${name}<`)) fail(name, 'not in sitemap');
  }

  for (const m of html.matchAll(/<use href="assets\/icons\.svg#([^"]+)"/g)) {
    if (!iconIds.has(m[1])) fail(name, `missing icon: ${m[1]}`);
  }

  for (const m of html.matchAll(/<a\b[^>]*\shref="([^"]+)"[^>]*>/g)) {
    const href = m[1];
    if (/^(mailto:|https?:)/.test(href)) {
      if (/target="_blank"/.test(m[0]) && !/rel="noopener"/.test(m[0])) fail(name, `new-tab link without noopener: ${href}`);
      continue;
    }
    if (href.startsWith('tel:')) {
      if (href.startsWith('tel:+') && href !== `tel:${PHONE}`) fail(name, `unexpected phone number: ${href}`);
      continue;
    }
    const [path, hash] = href.split('#');
    const target = path === '' ? file : path === './' ? join(dist, 'index.html') : join(dist, path);
    if (!existsSync(target)) { fail(name, `broken link: ${href}`); continue; }
    if (hash && !idsIn(docs[target] || readFileSync(target, 'utf8')).has(hash)) fail(name, `broken anchor: ${href}`);
  }

  const visible = html.replace(/<script[\s\S]*?<\/script>/g, '').replace(/<[^>]+>/g, ' ');
  for (const re of BANNED) {
    if (re.test(visible)) fail(name, `risky claim matched ${re}`);
  }
}

const sitemap = readFileSync(join(dist, 'sitemap.xml'), 'utf8');
const locs = [...sitemap.matchAll(/<loc>([^<]+)<\/loc>/g)].map((m) => m[1]);
if (!locs.length) fail('sitemap.xml', 'no URLs');
for (const loc of locs) {
  const p = loc.replace(`${SITE}/`, '') || 'index.html';
  if (!existsSync(join(dist, p))) fail('sitemap.xml', `URL has no page: ${loc}`);
}
if (!readFileSync(join(dist, 'robots.txt'), 'utf8').includes(`Sitemap: ${SITE}/sitemap.xml`)) fail('robots.txt', 'sitemap line missing');
if (!existsSync(join(dist, '_headers'))) fail('dist', '_headers missing');

if (errors.length) {
  console.error(`\n${errors.length} problem(s) found:\n- ${errors.join('\n- ')}\n`);
  process.exit(1);
}
console.log(`All checks passed: ${pages.length} pages, ${files.length} files.`);
