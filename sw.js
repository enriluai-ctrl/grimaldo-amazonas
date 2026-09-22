// Service Worker — Grimaldo Amazonas
// Estrategia: network-first para links.json, cache-first para shell, diapositivas y logos.

const VERSION = 'grimaldo-hub-v7';
const SHELL = [
  './',
  './index.html',
  './diapositivas.html',
  './links.json',
  './manifest.webmanifest',
  './icons/icon-192.png',
  './icons/icon-512.png',
  './icons/apple-touch-icon.png',
  './material/grimaldo-avatar.png',
  './material/grimaldo-oficial.png',
  './material/simbolo-victoria.png',
  './material/cedula-voto-x.png',
  './material/simbolo-marcado-x.png',
  './material/badge-marca-x.png'
];

self.addEventListener('install', (e) => {
  e.waitUntil(
    caches.open(VERSION).then((c) => c.addAll(SHELL)).then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(keys.filter((k) => k !== VERSION).map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (e) => {
  const req = e.request;
  if (req.method !== 'GET') return;

  const url = new URL(req.url);
  if (url.origin !== self.location.origin) return; // enlaces externos: no interceptar

  const esDatos = url.pathname.endsWith('links.json');
  const esNavegacion = req.mode === 'navigate' ||
    (req.headers.get('accept') || '').includes('text/html');

  if (esDatos || esNavegacion) {
    // network-first: internet primero para ver siempre novedades; si falla, cache local
    e.respondWith(
      fetch(req, { cache: 'no-store' })
        .then((res) => {
          const copia = res.clone();
          caches.open(VERSION).then((c) => c.put(req, copia));
          return res;
        })
        .catch(() => caches.match(req).then((m) => m || caches.match('./index.html')))
    );
    return;
  }

  // imágenes, íconos y assets: cache-first (ultra rápido) con respaldo de red
  e.respondWith(
    caches.match(req).then((m) => m || fetch(req).then((res) => {
      const copia = res.clone();
      caches.open(VERSION).then((c) => c.put(req, copia));
      return res;
    }))
  );
});
