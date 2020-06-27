import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.loader import ItemLoader
from scrapy.mail import MailSender

from tutorial.items import TutorialItem


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        urls = [
            'http://quotes.toscrape.com/page/1/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        item = TutorialItem()
        item['name'] = 'ABC'
        print('first item: ' + str(item))
        request = scrapy.Request(url='http://quotes.toscrape.com/page/2/', callback=self.parse2, meta={'item':item})
        yield request

    def parse2(self, response):
        # 如果需要多次爬网站构建一个对象，可以把中途的对象存放在meta里
        item = response.meta['item']
        item['price'] = 123
        try:
            print('after item: ' + str(item))
            # a = 1/0
        except Exception:
            self.logger.error('not work') # 可以自定义展示的报错

        yield item


#启动爬虫
process = CrawlerProcess()
process.crawl(QuotesSpider)
process.start()

