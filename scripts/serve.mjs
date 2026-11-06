// Local preview of dist/ with the same headers and compression as a live host. Usage: npm run serve [-- port]
import { existsSync, readFileSync, statSync } from 'node:fs';
import { createServer } from 'node:http';
import { dirname, extname, join, normalize, sep } from 'node:path';
import { fileURLToPath } from 'node:url';
import { gzipSync } from 'node:zlib';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const dist = join(root, 'dist');
const port = Number(process.argv[2] || 5510);
const TYPES = {
  '.html': 'text/html; charset=utf-8', '.css': 'text/css', '.js': 'text/javascript', '.svg': 'image/svg+xml',
  '.webp': 'image/webp', '.jpg': 'image/jpeg', '.png': 'image/png', '.ico': 'image/x-icon',
  '.woff2': 'font/woff2', '.xml': 'application/xml', '.txt': 'text/plain',
};
const TEXT = new Set(['.html', '.css', '.js', '.svg', '.xml', '.txt']);
const config = JSON.parse(readFileSync(join(root, 'vercel.json'), 'utf8')).headers;
// HTTPS-only rules are left out because this preview runs on plain http.
const headers = Object.fromEntries(
  config[0].headers
    .filter((h) => h.key !== 'Strict-Transport-Security')
    .map((h) => [h.key, h.value.replace('; upgrade-insecure-requests', '')]),
);
const assetCache = config[1].headers[0].value;

createServer((req, res) => {
  let path;
  try {
    path = normalize(decodeURIComponent(new URL(req.url, 'http://x').pathname)).replace(/^([/\\])+/, '');
  } catch {
    res.writeHead(400, headers);
    return res.end('Bad request');
  }
  let file = join(dist, path);
  const inside = (f) => f === dist || f.startsWith(dist + sep);
  if (inside(file) && existsSync(file) && statSync(file).isDirectory()) file = join(file, 'index.html');
  const found = inside(file) && existsSync(file);
  const send = found ? file : join(dist, '404.html');
  const ext = extname(send);
  const out = { ...headers, 'Content-Type': TYPES[ext] || 'application/octet-stream' };
  if (/^(assets|images)[/\\]/.test(path)) out['Cache-Control'] = assetCache;
  let body = readFileSync(send);
  if (TEXT.has(ext) && /gzip/.test(req.headers['accept-encoding'] || '')) {
    body = gzipSync(body);
    out['Content-Encoding'] = 'gzip';
  }
  res.writeHead(found ? 200 : 404, out);
  res.end(body);
}).listen(port, '127.0.0.1', () => console.log(`Preview: http://127.0.0.1:${port}/`));
