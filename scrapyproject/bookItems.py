# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BookItem(scrapy.Item):
    # define the fields for your item here like:
    #
    isbn = scrapy.Field()
    name = scrapy.Field()
    englishName = scrapy.Field()
    title = scrapy.Field()
    seriesName = scrapy.Field()
    author = scrapy.Field()
    introduction = scrapy.Field()
    publisher = scrapy.Field()
    publishingTime = scrapy.Field()
    edition = scrapy.Field()
    score = scrapy.Field()
    translate = scrapy.Field()
    editor = scrapy.Field()
    folio = scrapy.Field()
    size = scrapy.Field()
    weight = scrapy.Field()
    price = scrapy.Field()
    image = scrapy.Field()

