// static/js/serviceworker.js

self.addEventListener('install', function (e) {
    console.log('[ServiceWorker] Installing...');
    e.waitUntil(
        caches.open('projectsite-cache-v1').then(function (cache) {
            return cache.addAll([
                '/',  // main page
                '/static/css/bootstrap.min.css',
                '/static/js/ready-fixed.js',
                '/static/js/core/jquery.3.2.1.min.js',
            ]);
        }).catch(function (err) {
            console.error('⚠️ Caching failed:', err);
        })
    );
});

self.addEventListener('fetch', function (e) {
    e.respondWith(
        caches.match(e.request).then(function (response) {
            return response || fetch(e.request);
        })
    );
});

self.addEventListener('activate', function (e) {
    console.log('[ServiceWorker] Activated');
});
