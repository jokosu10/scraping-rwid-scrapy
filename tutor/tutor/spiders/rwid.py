# -*- coding: utf-8 -*-
import scrapy


class RwidSpider(scrapy.Spider):
    name = 'rwid'
    allowed_domains = ['localhost:5000']
    start_urls = ['http://localhost:5000/']

    def parse(self, response):
        yield {"title": response.css("title::text").get()}
