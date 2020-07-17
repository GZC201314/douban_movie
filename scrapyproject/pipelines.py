# -*- coding: utf-8 -*-
import pymongo
from scrapy.exceptions import DropItem
import pymysql
from douban_movie.scrapyproject.settings import mongo_db_collection,mongo_db_name,mongo_host,mongo_port
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class ScrapyprojectPipeline(object):
    def __init__(self):
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
            # mongodb 入库
            # self.post = self.mydb[self.sheetname]
            # self.post.insert(data)
            # mysql 入库
            sdb = pymysql.connect(host='localhost',
                                       user='root',
                                       password='abc123123',
                                       db='bookmanager',
                                       charset='utf8mb4',
                                       cursorclass=pymysql.cursors.DictCursor)
            cursor = sdb.cursor()
            table = 'tmovie'
            keys = ', '.join(data.keys())
            values = ', '.join(['%s'] * len(data))
            sql = 'INSERT INTO {table}({keys}) VALUES ({values})'.format(table=table, keys=keys, values=values)
            try:
                values = tuple(data.values())
                cursor.execute(sql, values)
                print('Successful')
                sdb.commit()
            except Exception as e:
                print('Failed   ',str(e))
                sdb.rollback()
            cursor.close()
            sdb.close()
            return item

class DoubanBookPipeline(object):
    #重写插入数据的方法
    def process_item(self, item, spider):
        data = dict(item)
        # 去重
        sdb = pymysql.connect(host='localhost',
                              user='root',
                              password='abc123123',
                              db='bookmanager',
                              charset='utf8mb4',
                              cursorclass=pymysql.cursors.DictCursor)
        cursor = sdb.cursor()

        sql = 'select * from doubanBook where isbn =%s'
        cursor.execute(sql, (item['isbn']))
        rows = cursor.fetchone()

        if rows:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            # mongodb 入库
            # self.post = self.mydb[self.sheetname]
            # self.post.insert(data)
            table = 'doubanBook'
            keys = ', '.join(data.keys())
            values = ', '.join(['%s'] * len(data))
            sql = 'INSERT INTO {table}({keys}) VALUES ({values})'.format(table=table, keys=keys, values=values)
            try:
                values = tuple(data.values())
                cursor.execute(sql, values)
                print('Successful')
                sdb.commit()
            except Exception as e:
                print('Failed   ',str(e))
                sdb.rollback()
            cursor.close()
            sdb.close()
            return item