# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, Join, TakeFirst

from utils.fieldutils import generate_legal_num


class PcfSec(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    dt = scrapy.Field()
    fund_id = scrapy.Field()
    fund_name = scrapy.Field()
    fund_company = scrapy.Field()
    sec_id = scrapy.Field()
    sec_name = scrapy.Field()
    sec_qty = scrapy.Field()
    sec_tag = scrapy.Field()
    sec_sub_premium_ratio = scrapy.Field()
    sec_red_discount_ratio = scrapy.Field()
    sec_alter_money = scrapy.Field(input_processor=MapCompose(generate_legal_num),
                                   )
    src = scrapy.Field()


class PcfSecItemLoader(ItemLoader):
    # 自定义ItemLoader
    default_output_processor = TakeFirst()
