# -*- coding: utf-8 -*-
import scrapy
import re
from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from BaiDuTieBa.items import BaidutiebaItem,BaiDuTieBaItemLoader

class TiebaSpider(CrawlSpider):
    name = 'TieBa'
    allowed_domains = ['tieba.baidu.com']
    base_urls =  'https://tieba.baidu.com/'
    start_urls = ['https://tieba.baidu.com/f?kw=' + input('input a tieba name:')]


    rules = (
        Rule(LinkExtractor(allow=r'/p/\d+'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item_loader = BaiDuTieBaItemLoader(item=BaidutiebaItem(), response=response)
        item_loader.add_value("title", re.search('class="core_title_txt.*?title=(.*?)" style="width:.*?',response.text,re.S).group(1))
        item_loader.add_xpath("author_name", '//*[@id="j_p_postlist"]/div[1]/div[2]/ul/li[3]/a/text()')
        item_loader.add_value("created_time", re.search('\d{4}-\d{2}-\d{2} \d{2}:\d{2}', response.text, re.S).group())
        item_loader.add_xpath("content",'//*[@class="d_post_content j_d_post_content  clearfix"]/text()')
        item_loader.add_css("comments_num",
                            '#thread_theme_5 > div.l_thread_info > ul > li:nth-child(2) > span:nth-child(1)::text')
        item_loader.add_value("url", response._url)
        item_loader.add_value("crawl_time", datetime.now())
        tieba_item = item_loader.load_item()
        return tieba_item
