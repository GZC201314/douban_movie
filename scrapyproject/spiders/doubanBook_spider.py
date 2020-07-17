# -*- coding: utf-8 -*-
import scrapy
from douban_movie.scrapyproject.bookItems import BookItem

class ScrapySpiderSpider(scrapy.Spider):
    # 爬虫名
    name = "doubanBook_spider"
    # 允许的域名,其他的域名将不会爬取
    allowed_domains = ["book.douban.com"]
    # 入口url
    start_urls = ['https://book.douban.com/tag/%E5%B0%8F%E8%AF%B4']

    def parse(self, response):
        # 获取图书详细信息的url
        bookurl_list = response.xpath('//ul[@class="subject-list"]//li[@class="subject-item"]//div[@class="info"]//h2//a/@href').extract()
        for i_item in bookurl_list:
            doubanItem = BookItem()
            yield scrapy.Request(i_item,callback=self.bookparse)

#       下一页的数据处理
        next_link = response.xpath('//span[@class="next"]/link/@href').extract()
        if next_link:
            next_link = next_link[0]
            yield scrapy.Request('https://book.douban.com'+next_link,callback=self.parse)
    def bookparse(self, response):
        bookItems = BookItem()
        bookItems['name'] = response.xpath('//span[@property="v:itemreviewed"]/text()').extract_first()
        bookItems['isbn'] = response.xpath('//span[contains(text(),"ISBN")]/following::text()[1]').extract_first()
        bookItems['author'] = response.xpath('//span[contains(text(),"作者")]/following::text()[2]').extract_first()
        if bookItems["author"]:
            bookItems["author"] = [i.replace(" ", "") for i in bookItems["author"]]
            bookItems["author"] = "".join([i.replace("\n", " ") for i in bookItems["author"]])
        bookItems['edition'] = response.xpath('//span[contains(text(),"出品方")]/following::text()[2]').extract_first()
        bookItems['translate'] = response.xpath('//span[contains(text(),"译者")]/following::text()[2]').extract_first()
        if bookItems['translate']:
            bookItems["translate"] = [i.replace(" ", "") for i in bookItems["translate"]]
            bookItems["translate"] = "".join([i.replace("\n", " ") for i in bookItems["translate"]])
        bookItems['score'] = response.xpath('//strong/text()').extract_first()
        bookItems['publisher'] = response.xpath('//span[contains(text(),"出版社")]/following::text()[1]').extract_first()
        bookItems['publishingTime'] = response.xpath('//span[contains(text(),"出版年")]/following::text()[1]').extract_first()
        bookItems['folio'] = response.xpath('//span[contains(text(),"页数")]/following::text()[1]').extract_first()
        bookItems['price'] = response.xpath('//span[contains(text(),"定价")]/following::text()[1]').extract_first()
        bookItems['size'] = response.xpath('//span[contains(text(),"装帧")]/following::text()[1]').extract_first()
        bookItems['seriesName'] = response.xpath('//span[contains(text(),"丛书")]/following::text()[2]').extract_first()
        bookItems['introduction'] = response.xpath('//div[@class="indent"]//div//div[@class="intro"]//p/text()').extract_first()
        bookItems['image'] = response.xpath('//div[@id="mainpic"]//img/@src').extract_first()
        yield bookItems