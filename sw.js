/* CardioTherapy Atlas — service worker
   Strategia: cache-first sull'applicazione, con aggiornamento in background.
   L'app e' un singolo file autonomo: una volta in cache funziona senza connessione.
   Per forzare l'aggiornamento dopo una modifica, incrementare CACHE_NAME. */
const CACHE_NAME = 'cardiotherapy-atlas-v7';
const CORE = ['./', './index.html', './manifest.webmanifest', './assets/icon.svg',
  './assets/fonts/ibm-plex-mono-latin-400-normal.woff2',
  './assets/fonts/ibm-plex-mono-latin-500-normal.woff2',
  './assets/fonts/ibm-plex-mono-latin-600-normal.woff2',
  './assets/fonts/ibm-plex-mono-latin-ext-400-normal.woff2',
  './assets/fonts/ibm-plex-mono-latin-ext-500-normal.woff2',
  './assets/fonts/ibm-plex-mono-latin-ext-600-normal.woff2',
  './assets/fonts/ibm-plex-sans-latin-400-italic.woff2',
  './assets/fonts/ibm-plex-sans-latin-400-normal.woff2',
  './assets/fonts/ibm-plex-sans-latin-500-normal.woff2',
  './assets/fonts/ibm-plex-sans-latin-600-normal.woff2',
  './assets/fonts/ibm-plex-sans-latin-ext-400-italic.woff2',
  './assets/fonts/ibm-plex-sans-latin-ext-400-normal.woff2',
  './assets/fonts/ibm-plex-sans-latin-ext-500-normal.woff2',
  './assets/fonts/ibm-plex-sans-latin-ext-600-normal.woff2',
  './assets/fonts/space-grotesk-latin-500-normal.woff2',
  './assets/fonts/space-grotesk-latin-600-normal.woff2',
  './assets/fonts/space-grotesk-latin-700-normal.woff2',
  './assets/fonts/space-grotesk-latin-ext-500-normal.woff2',
  './assets/fonts/space-grotesk-latin-ext-600-normal.woff2',
  './assets/fonts/space-grotesk-latin-ext-700-normal.woff2'];

self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(CACHE_NAME)
      .then(c => c.addAll(CORE).catch(() => c.add('./index.html')))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys()
      .then(ks => Promise.all(ks.filter(k => k !== CACHE_NAME).map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', e => {
  const req = e.request;
  if (req.method !== 'GET' || new URL(req.url).origin !== self.location.origin) return;
  e.respondWith(
    caches.match(req, { ignoreSearch: true }).then(hit => {
      const rete = fetch(req).then(res => {
        if (res && res.status === 200 && res.type === 'basic') {
          const copia = res.clone();
          caches.open(CACHE_NAME).then(c => c.put(req, copia));
        }
        return res;
      }).catch(() => hit);
      return hit || rete;
    })
  );
});
