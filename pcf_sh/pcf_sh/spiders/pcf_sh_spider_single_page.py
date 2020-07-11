import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.loader import ItemLoader
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.utils.project import get_project_settings

from pcf_sh.items import PcfSec, PcfSecItemLoader


class PcfShSpider(scrapy.Spider):

    name = 'pcf_sh_spider'
    # allowed_domains = ["sse.com.cn"]
    # start_urls = [
    #     "http://www.sse.com.cn/disclosure/fund/etflist/",
    #     #"http://www.sse.com.cn/disclosure/fund/etflist/detail.shtml?type=005&fundid=510010&etfClass=1"
    # ]
    # rules = (
    #     Rule(LinkExtractor(allow=("detail.shtml",
    #                               )
    #                        ),
    #          callback='parse_item'
    #          ),
    # )

    def start_requests(self):
        urls = [
            #'http://www.sse.com.cn/disclosure/fund/etflist/detail.shtml?type=123&fundid=512550&etfClass=2',
            'http://www.sse.com.cn/disclosure/fund/etflist/detail.shtml?type=005&fundid=510010&etfClass=1',
            #'http://www.sse.com.cn/disclosure/fund/etflist/detail.shtml?type=011&fundid=510070&etfClass=1'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        print('###########parse start###########')
        fund_name = response.xpath('//*[@id="tableData_tableData1"]/div[2]/table/tbody/tr[2]/td/text()').get()
        fund_id = response.xpath('//*[@id="tableData_tableData1"]/div[2]/table/tbody/tr[4]/td/text()').get()
        fund_company = response.xpath('//*[@id="tableData_tableData1"]/div[2]/table/tbody/tr[3]/td/text()').get()
        dt = response.xpath('//*[@id="tableData_tableData1"]/div[2]/table/tbody/tr[1]/td/text()').get()
        src = 'sse.com.cn'

        n = 2
        while response.xpath('//*[@id="tableData_tableData4"]/div[2]/table/tbody/tr[%s]/td[1]/text()' % n).get():
            sec_id= response.xpath('//*[@id="tableData_tableData4"]/div[2]/table/tbody/tr[%s]/td[1]/text()' % n).get()
            sec_name = response.xpath('//*[@id="tableData_tableData4"]/div[2]/table/tbody/tr[%s]/td[2]/text()' % n).get()
            sec_qty = response.xpath('//*[@id="tableData_tableData4"]/div[2]/table/tbody/tr[%s]/td[3]/div/text()' % n).get()
            sec_tag = response.xpath('//*[@id="tableData_tableData4"]/div[2]/table/tbody/tr[%s]/td[4]/text()' % n).get()
            sec_sub_premium_ratio = response.xpath('//*[@id="tableData_tableData4"]/div[2]/table/tbody/tr[%s]/td[5]/text()' % n).get()

            # pcf目前有两种版本，如果带有赎回现金替代折价比率，表格需要往后再推一列
            if_both_cash_ratio = response.xpath('//*[@id="tableData_tableData4"]/div[2]/table/tbody/tr[1]/th[6]/text()').get()
            if if_both_cash_ratio.find('赎回现金') != -1:
                sec_red_discount_ratio = response.xpath('//*[@id="tableData_tableData4"]/div[2]/table/tbody/tr[%s]/td[6]/text()' % n).get()
                sec_alter_money = response.xpath('//*[@id="tableData_tableData4"]/div[2]/table/tbody/tr[%s]/td[7]/div/text()' % n).get()
            else:
                sec_red_discount_ratio = 'INVALID'
                sec_alter_money= response.xpath('//*[@id="tableData_tableData4"]/div[2]/table/tbody/tr[%s]/td[6]/div/text()' % n).get()


            # 启用 Itemloader 通过input_processor为每个属性创建一个列表，再通过output_processor把列表的值赋给每个属性
            # 特别注意，此时赋值给属性的是类别，如果要取出列表中的单个值，可以以用TakeFirst()或Join()方法给output_processor
            # 这里用Itemloader的子类，default_output_processor = TakeFirst()，这样就不用给每个属性都定义output_processor
            psl = PcfSecItemLoader(item=PcfSec())
            # pcf_sec = PcfSec()
            for field in PcfSec.__dict__.get('fields').keys():
                try:
                    # pcf_sec[field] = eval(field)
                    psl.add_value(field, eval(field))
                except NameError:
                    pass

            # print(pcf_sh_item)
            n += 1
            # yield pcf_sec
            yield psl.load_item()


if __name__ == "__main__":
    #start crawl
    process = CrawlerProcess(get_project_settings())
    process.crawl(PcfShSpider)
    process.start()