# # -*- coding: utf-8 -*-
# import pymongo
# from scrapy.exceptions import DropItem
# import pymysql
# from douban_movie.scrapyproject.settings import mongo_db_collection,mongo_db_name,mongo_host,mongo_port
# # Define your item pipelines here
# #
# # Don't forget to add your pipeline to the ITEM_PIPELINES setting
# # See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
#
#
# class DoubanBookPipeline(object):
#     def __init__(self):
#         self.ids_seen = set()
#     # 重写插入数据的方法
#     def process_item(self, item, spider):
#         data = dict(item)
#         # 去重
#         if item['isbn'] in self.ids_seen:
#             raise DropItem("Duplicate item found: %s" % item)
#         else:
#             self.ids_seen.add(item['isbn'])
#             # mongodb 入库
#             # self.post = self.mydb[self.sheetname]
#             # self.post.insert(data)
#             # mysql 入库
#             sdb = pymysql.connect(host='localhost',
#                                        user='root',
#                                        password='abc123123',
#                                        db='bookmanager',
#                                        charset='utf8mb4',
#                                        cursorclass=pymysql.cursors.DictCursor)
#             cursor = sdb.cursor()
#             table = 'doubanBook'
#             keys = ', '.join(data.keys())
#             values = ', '.join(['%s'] * len(data))
#             sql = 'INSERT INTO {table}({keys}) VALUES ({values})'.format(table=table, keys=keys, values=values)
#             try:
#                 values = tuple(data.values())
#                 cursor.execute(sql, values)
#                 print('Successful')
#                 sdb.commit()
#             except Exception as e:
#                 print('Failed   ',str(e))
#                 sdb.rollback()
#             cursor.close()
#             sdb.close()
#             return item
