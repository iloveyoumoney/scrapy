# -*- coding: utf-8 -*-
__author__ = 'JS'
__data__ = '2018.3.25'


import scrapy
from XicidailiSpider.items import XiciItem

class XicidlSpider(scrapy.Spider):
    name = 'xicidl'
    allowed_domains = ['www.xicidaili.com']
    start_urls = [
        'http://www.xicidaili.com/nn/',
        'http://www.xicidaili.com/nt/',
        'http://www.xicidaili.com/wn/',
        'http://www.xicidaili.com/wt/',
        'http://www.xicidaili.com/qq/'
    ]
    host = 'http://www.xicidaili.com'

    def parse(self, response):
        print('正在抓取的url：{}'.format(response.url))
        selector = response.xpath('//table[@id="ip_list"]/tr')
        item = XiciItem()
        for sel in selector[1:]:
            ip = sel.xpath('td[2]/text()').extract()
            port = sel.xpath('td[3]/text()').extract()
            address = sel.xpath('td[4]/a/text()').extract()
            status = sel.xpath('td[5]/text()').extract()
            style = sel.xpath('td[6]/text()').extract()
            item['ip'] = ip[0] if ip else ""
            item['port'] = port[0] if port else ""
            item['address'] = address[0] if address else ""
            item['status'] = status[0] if status else ""
            item['style'] = style[0] if style else ""
            yield item
        next_page = response.css('a.next_page::attr(href)')
        if next_page:
            next_page_url = '{}{}'.format(self.host, next_page.extract()[0])
            yield scrapy.Request(next_page_url, callback=self.parse)