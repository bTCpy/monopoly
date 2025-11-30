const CACHE_NAME = 'cashu-monopoly-v1';
const urlsToCache = [
  '/',
  '/index.html',
  '/styles.css',
  '/monopoly.js',
  '/classicedition.js',
  '/ai.js',
  '/images/chance_icon.png',
  '/images/community_chest_icon.png',
  '/images/arrow.png',
  '/images/arrow_icon.png',
  '/images/chance_icon.png',
  '/images/close.png',
  '/images/community_chest_icon.png',
  '/images/Die_1.png',
  '/images/Die_2.png',
  '/images/Die_3.png',
  '/images/Die_4.png',
  '/images/Die_5.png',
  '/images/Die_6.png',
  '/images/electric_icon.png',
  '/images/free_parking_icon.png',
  '/images/hori-bar.png',
  '/images/hotel.png',
  '/images/hotel_faded.png',
  '/images/house.png',
  '/images/house_faded.png',
  '/images/jake_icon.png',
  '/images/menu_background.png',
  '/images/menu_background_hover.png',
  '/images/tax_icon.png',
  '/images/train_icon.png',
  '/images/vert-bar.png',
  '/images/water_icon.png'
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
