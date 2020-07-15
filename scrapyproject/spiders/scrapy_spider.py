# -*- coding: utf-8 -*-
import scrapy
from scrapyproject.items import ScrapyprojectItem


class ScrapySpiderSpider(scrapy.Spider):
    # 爬虫名
    name = "scrapy_spider"
    # 允许的域名,其他的域名将不会爬取
    allowed_domains = ["movie.douban.com"]
    # 入口url
    start_urls = ['http://movie.douban.com/top250']

    def parse(self, response):
        movie_list =  response.xpath('//div[@class="article"]//ol[@class="grid_view"]//li')
        for i_item in movie_list:
            doubanItem = ScrapyprojectItem()
            doubanItem['serial_number'] = i_item.xpath(".//div[@class='item']//em/text()").extract_first()
            doubanItem['picture_address'] = i_item.xpath(".//div[@class='item']//img/@src").extract_first()
            doubanItem['movie_name'] = i_item.xpath(".//div[@class='info']//span[@class='title']/text()").extract_first()
            doubanItem['introduce'] = i_item.xpath(".//div[@class='bd']/p[1]/text()").extract()
            doubanItem["introduce"] = [i.replace(" ", "") for i in doubanItem["introduce"]]
            doubanItem["introduce"] = [i.replace("\xa0", " ") for i in doubanItem["introduce"]]
            doubanItem["introduce"] = "".join([i.replace("\n", " ") for i in doubanItem["introduce"]])

            doubanItem['star'] = i_item.xpath(".//div[@class='star']//span[@class='rating_num']/text()").extract_first()
            doubanItem['evaluate'] = i_item.xpath(".//div[@class='star']//span[4]/text()").extract_first()
            doubanItem['describe'] = i_item.xpath(".//div[@class='bd']//span[@class='inq']/text()").extract_first()
            yield doubanItem

#       下一页的数据处理
        next_link = response.xpath('//span[@class="next"]/link/@href').extract()
        if next_link:
            next_link = next_link[0]
            yield scrapy.Request('https://movie.douban.com/top250'+next_link,callback=self.parse)
