# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from scrapy_splash import SplashRequest


class SplashwithjavascriptwebsiteluascriptspiderSpider(scrapy.Spider):
    name = 'splashWithJavaScriptWebsiteLuaScriptSpider'
    allowed_domains = ['www.baierl.com']
    start_urls = ['http://www.baierl.com/new-inventory/']

    def start_requests(self):
        # script for action filters
        filters_script = """function main(splash)
                                assert(splash:go(splash.args.url))
                                splash:wait(5)

                                local get_element_dim_by_xpath = splash:jsfunc([[
                                    function(xpath) {
                                        var element = document.evaluate(xpath, document, null,
                                            XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                                        var element_rect = element.getClientRects()[0];
                                        return {"x": element_rect.left, "y": element_rect.top}
                                    }
                                ]])

                                -- -- Find the YEAR drop down
                                local year_drop_dimensions = get_element_dim_by_xpath(
                                    '//h2[contains(@class, "label ") and contains(text(), "Year ")]')
                                splash:set_viewport_full()
                                splash:mouse_click(year_drop_dimensions.x, year_drop_dimensions.y)
                                splash:wait(1.5)

                                -- -- Clicks the 2021 year
                                local year_dimensions = get_element_dim_by_xpath(
                                    '//li[contains(@data-value, "2021")]/span')
                                splash:set_viewport_full()
                                splash:mouse_click(year_dimensions.x, year_dimensions.y)
                                splash:wait(5)

                                -- Find the MAKE drop down
                                local make_drop_dimensions = get_element_dim_by_xpath(
                                    '//h2[contains(@class, "label ") and contains(text(), "Make ")]')
                                splash:set_viewport_full()
                                splash:mouse_click(make_drop_dimensions.x, make_drop_dimensions.y)
                                splash:wait(1.5)

                                -- Clicks the Chevrolet make
                                local make_dimensions = get_element_dim_by_xpath(
                                    '//li[contains(@data-filters, "make_chevrolet")]/span')
                                splash:set_viewport_full()
                                splash:mouse_click(make_dimensions.x, make_dimensions.y)
                                splash:wait(5)

                                return splash:html()
                            end"""
        # extract urls from webpage
        for url in self.start_urls:
            yield SplashRequest(url=url,
                                callback=self.parse,
                                endpoint='execute',
                                args={'lua_source': filters_script})

    def parse(self, response):
        # extract hyperlink with title
        cars_urls = response.xpath('//*[@class="title"]/a/@href').extract()
        # extract urls from one page
        for car_url in cars_urls:
            absolute_car_url = response.urljoin(car_url)
            yield Request(absolute_car_url,
                          callback=self.parse_car)

        script_at_page_1 = """function main(splash)
                                assert(splash:go(splash.args.url))
                                splash:wait(5)

                                local get_element_dim_by_xpath = splash:jsfunc([[
                                    function(xpath) {
                                        var element = document.evaluate(xpath, document, null,
                                            XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                                        var element_rect = element.getClientRects()[0];
                                        return {"x": element_rect.left, "y": element_rect.top}
                                    }
                                ]])

                                -- -- Find the YEAR drop down
                                local year_drop_dimensions = get_element_dim_by_xpath(
                                    '//h2[contains(@class, "label ") and contains(text(), "Year ")]')
                                splash:set_viewport_full()
                                splash:mouse_click(year_drop_dimensions.x, year_drop_dimensions.y)
                                splash:wait(1.5)

                                -- -- Clicks the 2021 year
                                local year_dimensions = get_element_dim_by_xpath(
                                    '//li[contains(@data-value, "2021")]/span')
                                splash:set_viewport_full()
                                splash:mouse_click(year_dimensions.x, year_dimensions.y)
                                splash:wait(5)

                                -- Find the MAKE drop down
                                local make_drop_dimensions = get_element_dim_by_xpath(
                                    '//h2[contains(@class, "label ") and contains(text(), "Make ")]')
                                splash:set_viewport_full()
                                splash:mouse_click(make_drop_dimensions.x, make_drop_dimensions.y)
                                splash:wait(1.5)

                                -- Clicks the Chevrolet make
                                local make_dimensions = get_element_dim_by_xpath(
                                    '//li[contains(@data-filters, "make_chevrolet")]/span')
                                splash:set_viewport_full()
                                splash:mouse_click(make_dimensions.x, make_dimensions.y)
                                splash:wait(5)

                                next_button = splash:select("*[class='page-next ']")
                                next_button.mouse_click()
                                splash:wait(4)
                                return {
                                    url = splash:url(),
                                    html = splash:html()
                                }
                            end"""

        script_at_page_2 = """function main(splash)
                                assert(splash:go(splash.args.url))
                                splash:wait(5)

                                next_button = splash:select("*[class='page-next ']")
                                next_button.mouse_click()
                                splash:wait(4)
                                return {
                                    url = splash:url(),
                                    html = splash:html()
                                }
                            end"""

        # checking present url and according url perform actions
        script = None
        if response.url is not self.start_urls[0]:
            script = script_at_page_2
        else:
            script = script_at_page_1

        yield SplashRequest(url=response.url,
                            callback=self.parse,
                            endpoint='execute',
                            args={'lua_source': script})

    def parse_car(self, response):
        # extract car details
        name = ''.join(response.xpath('//h1//text()').extract())
        price = response.xpath('//*[@class="finalPrice"]/span/text()').extract_first()
        vin = response.xpath('//li[@class="vin"]/span[@class="value"]/text()').extract_first()
        stock = response.xpath('//li[@class="stock"]/span[@class="value"]/text()').extract_first()
        modelnumber = response.xpath('//li[@class="modelnumber"]/span[@class="value"]/text()').extract_first()
        body = response.xpath('//li[@class="body"]/span[@class="value"]/text()').extract_first()
        extcolorgeneric = response.xpath('//li[@class="extcolorgeneric"]/span[@class="value"]/text()').extract_first()
        intcolor = response.xpath('//li[@class="intcolor"]/span[@class="value"]/text()').extract_first()
        engdescription = response.xpath('//li[@class="engdescription"]/span[@class="value"]/text()').extract_first()
        transdescription = response.xpath('//li[@class="transdescription"]/span[@class="value"]/text()').extract_first()
        drivetrain = response.xpath('//li[@class="drivetrain"]/span[@class="value"]/text()').extract_first()
        dealername = response.xpath('//li[@class="dealername"]/span[@class="value"]/text()').extract_first()

        yield {'name': name,
               'price': price,
               'stock': stock,
               'vin': vin,
               'modelnumber': modelnumber,
               'body': body,
               'extcolorgeneric': extcolorgeneric,
               'intcolor': intcolor,
               'engdescription': engdescription,
               'transdescription': transdescription,
               'drivetrain': drivetrain,
               'dealername': dealername}
