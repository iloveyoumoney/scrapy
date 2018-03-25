# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class XiciItem(scrapy.Item):

    ip = scrapy.Field()  # ip
    port = scrapy.Field()  # 端口
    address = scrapy.Field()  # 地址
    status = scrapy.Field()  # ip状态,透明、高匿等
    style = scrapy.Field()  # ip类型,http或https等
