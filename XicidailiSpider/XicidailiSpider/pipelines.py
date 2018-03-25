# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
import pymysql
from scrapy.conf import settings

class XicidailispiderPipeline(object):

    def __init__(self):
        client = pymongo.MongoClient(host=settings['MONGODB_HOST'],
                                     port=settings['MONGODB_PORT'])
        db_name = client[settings['MONGODB_DBNAME']]
        self.doc_name = db_name[settings['MONGODB_DOCNAME']]

    def process_item(self, item, spider):
        proxy_info = dict(item)
        self.doc_name.insert(proxy_info)
        return item


class XicidailiMysqlPipeline(object):
    #采用同步的机制写入mysql
    def __init__(self):
        self.conn = pymysql.connect('localhost', 'root', 'root', 'xicidl', charset="utf8", use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        insert_sql = """
            insert into xicidaili(ip, port, address, status,style)
            VALUES (%s, %s, %s,%s, %s)
        """
        self.cursor.execute(insert_sql, (item["ip"], item["port"], item["address"], item["status"],item["style"]))
        self.conn.commit()