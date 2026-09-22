// Service Worker — Grimaldo Amazonas
// Estrategia: network-first para el menú (links.json) y la página,
// para que el profesor SIEMPRE vea la versión nueva cuando hay internet.
// El cache es solo respaldo sin señal.

const VERSION = 'grimaldo-hub-v1';
const SHELL = [
  './',
  './index.html',
  './links.json',
  './manifest.webmanifest',
  './icons/icon-192.png',
  './icons/icon-512.png',
  './icons/apple-touch-icon.png'
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
    // network-first: internet primero; si falla, última copia guardada
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

  // íconos y otros archivos: cache-first
  e.respondWith(
    caches.match(req).then((m) => m || fetch(req).then((res) => {
      const copia = res.clone();
      caches.open(VERSION).then((c) => c.put(req, copia));
      return res;
    }))
  );
});
