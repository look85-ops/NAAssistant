// Lightweight service worker for PWA cache
const CACHE_NAME = 'message-accidental-v1';
const ASSETS = [
  './message-accidental.html',
  './manifest.webmanifest'
  // Иконки добавятся, когда их добавим в repo
];

self.addEventListener('install', (e) => {
  e.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(ASSETS))
  );
});

self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys().then((keys) => Promise.all(keys.map(k => k !== CACHE_NAME ? caches.delete(k) : undefined)))
  );
});

// Network-first for HTML, cache-first for static
self.addEventListener('fetch', (e) => {
  const url = new URL(e.request.url);
  const isDoc = e.request.destination === 'document' || url.pathname.endsWith('.html');
  if (isDoc) {
    e.respondWith(
      fetch(e.request).then((resp) => {
        const copy = resp.clone();
        caches.open(CACHE_NAME).then((c) => c.put(e.request, copy));
        return resp;
      }).catch(() => caches.match(e.request))
    );
  } else {
    e.respondWith(
      caches.match(e.request).then((cached) => cached || fetch(e.request))
    );
  }
});
