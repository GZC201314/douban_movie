#__author:gzc
#date:2020/7/15
# -- coding: utf-8 --

from scrapy import cmdline
# 注意爬虫名不要写错
cmdline.execute('scrapy crawl doubanBook_spider'.split())