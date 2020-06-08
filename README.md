# splashWithJavaScriptWebsiteLuaScript

This is a Scrapy Splash project to scrape car information from  http://www.baierl.com/new-inventory/.

This project is only meant for educational purposes.

## Installation


Install scrapy-splash using pip::

    $ pip install scrapy-splash

Scrapy-Splash uses Splash_ HTTP API, so you also need a Splash instance.
Usually to install & run Splash, something like this is enough::

    $ docker run -p 8050:8050 scrapinghub/splash

Check Splash `install docs`_ for more info.

.. _install docs: http://splash.readthedocs.org/en/latest/install.html

## Configuration


1. Add the Splash server address to ``settings.py`` of your Scrapy project
   like this::

      SPLASH_URL = 'http://192.168.59.103:8050'

2. Enable the Splash middleware by adding it to ``DOWNLOADER_MIDDLEWARES``
   in your ``settings.py`` file and changing HttpCompressionMiddleware
   priority::

      DOWNLOADER_MIDDLEWARES = {
          'scrapy_splash.SplashCookiesMiddleware': 723,
          'scrapy_splash.SplashMiddleware': 725,
          'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
      }

   Order `723` is just before `HttpProxyMiddleware` (750) in default
   scrapy settings.

   HttpCompressionMiddleware priority should be changed in order to allow
   advanced response processing; see https://github.com/scrapy/scrapy/issues/1895
   for details.

3. Enable ``SplashDeduplicateArgsMiddleware`` by adding it to
   ``SPIDER_MIDDLEWARES`` in your ``settings.py``::

      SPIDER_MIDDLEWARES = {
          'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
      }

   This middleware is needed to support ``cache_args`` feature; it allows
   to save disk space by not storing duplicate Splash arguments multiple
   times in a disk request queue. If Splash 2.1+ is used the middleware
   also allows to save network traffic by not sending these duplicate
   arguments to Splash server multiple times.

4. Set a custom ``DUPEFILTER_CLASS``::

      DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'

5. If you use Scrapy HTTP cache then a custom cache storage backend
   is required. scrapy-splash provides a subclass of
   ``scrapy.contrib.httpcache.FilesystemCacheStorage``::

      HTTPCACHE_STORAGE = 'scrapy_splash.SplashAwareFSCacheStorage'

   If you use other cache storage then it is necesary to subclass it and
   replace all ``scrapy.util.request.request_fingerprint`` calls with
   ``scrapy_splash.splash_request_fingerprint``.

## Extracted data

This project extracts car details.
The extracted data looks like this sample:

          {
           "name": "2021 Chevrolet Trailblazer RS",
           "price": " $28,530",
           "stock": "MB005347",
           "vin": "KL79MTSL1MB005347",
           "modelnumber": "1TT56",
           "body": "Sport Utility",
           "extcolorgeneric": "Black",
           "intcolor": "Jet Black with Red accents",
           "engdescription": "Gas I3 1.3L/",
           "transdescription": "1-Speed Automatic",
           "drivetrain": "FWD",
           "dealername": "Baierl Chevrolet"
         }


## Spiders

This project contains one spider and you can list them using the `list`
command:

    $ scrapy list
    splashWithJavaScriptWebsiteLuaScriptSpider

Spider extract the data from quotes page and visit author hyperlink and extract auther infomation also.




## Running the spiders

You can run a spider using the `scrapy crawl` command, such as:

    $ scrapy crawl splashWithJavaScriptWebsiteLuaScriptSpider

If you want to save the scraped data to a file, you can pass the `-o` option:
    
    $ scrapy crawl splashWithJavaScriptWebsiteLuaScriptSpider -o output.json
