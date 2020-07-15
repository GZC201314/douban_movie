# -*- coding: utf-8 -*-
import pymongo
from scrapy.exceptions import DropItem

from scrapyproject.settings import mongo_db_collection,mongo_db_name,mongo_host,mongo_port
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class ScrapyprojectPipeline(object):
    def __init__(self):
        self.ids_seen = set()
        self.host = mongo_host
        self.port = mongo_port
        self.dbname = mongo_db_name
        self.sheetname = mongo_db_collection


    def open_spider(self, spider):
        self.client =pymongo.MongoClient(host=self.host,port=self.port)
        self.mydb = self.client[self.dbname]

    def close_spider(self, spider):
        self.client.close()
    # 重写插入数据的方法
    def process_item(self, item, spider):
        data = dict(item)
        # 去重
        if item['serial_number'] in self.ids_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.ids_seen.add(item['serial_number'])
            self.post = self.mydb[self.sheetname]
            self.post.insert(data)
            return item
