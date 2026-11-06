// Copies the website files from site/ into dist/, so nothing else in this folder is ever published.
import { createHash } from 'node:crypto';
import { cpSync, existsSync, mkdirSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const src = join(root, 'site');
const dist = join(root, 'dist');
const INCLUDE = [
  'index.html', 'class-8-9-tuition-vijayanagar.html', 'class-10-tuition-vijayanagar.html',
  'puc-tuition-vijayanagar.html', 'disclosures.html', 'privacy.html', 'terms.html', '404.html',
  'robots.txt', 'sitemap.xml', 'favicon.ico', 'apple-touch-icon.png', 'assets', 'images',
];

rmSync(dist, { recursive: true, force: true });
mkdirSync(dist);
for (const item of INCLUDE) {
  const from = join(src, item);
  if (!existsSync(from)) throw new Error(`Missing site file: ${item}`);
  cpSync(from, join(dist, item), { recursive: true });
}

// Stylesheet and script links carry a content hash, so returning visitors get updates despite long caching.
const hash = (file) => createHash('sha256').update(readFileSync(join(dist, file))).digest('hex').slice(0, 10);
const versions = { 'assets/site.css': hash('assets/site.css'), 'assets/site.js': hash('assets/site.js') };
for (const page of INCLUDE.filter((i) => i.endsWith('.html'))) {
  let html = readFileSync(join(dist, page), 'utf8');
  for (const [file, v] of Object.entries(versions)) html = html.replaceAll(`"${file}"`, `"${file}?v=${v}"`);
  writeFileSync(join(dist, page), html);
}

// Cloudflare Pages and Netlify read _headers. It is generated from vercel.json so the rules never drift apart.
const { headers } = JSON.parse(readFileSync(join(root, 'vercel.json'), 'utf8'));
const toPath = (source) => (source === '/(.*)' ? '/*' : null);
const blocks = headers.flatMap(({ source, headers: list }) => {
  if (source === '/(assets|images)/(.*)') {
    return ['/assets/*', '/images/*'].map((p) => [p, list]);
  }
  return [[toPath(source), list]];
});
const text = blocks
  .map(([path, list]) => `${path}\n${list.map((h) => `  ${h.key}: ${h.value}`).join('\n')}`)
  .join('\n\n');
writeFileSync(join(dist, '_headers'), text + '\n');

console.log(`Built ${INCLUDE.length} items into dist/`);
