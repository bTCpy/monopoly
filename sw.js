const CACHE_NAME = 'cashu-monopoly-v1';
const urlsToCache = [
  '/',
  '/index.html',
  '/styles.css',
  '/monopoly.js',
  '/classicedition.js',
  '/ai.js',
  '/images/chance_icon.png',
  '/images/community_chest_icon.png'
  // Add other images here if you want them to load offline
];

self.addEventListener('install', function(event) {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(function(cache) {
        return cache.addAll(urlsToCache);
      })
  );
});

self.addEventListener('fetch', function(event) {
  event.respondWith(
    caches.match(event.request)
      .then(function(response) {
        if (response) {
          return response;
        }
        return fetch(event.request);
      })
  );
});
