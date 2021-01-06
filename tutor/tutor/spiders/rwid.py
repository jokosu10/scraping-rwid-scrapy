# -*- coding: utf-8 -*-
import scrapy


class RwidSpider(scrapy.Spider):
    name = 'rwid'
    allowed_domains = ['localhost:5000']
    start_urls = ['http://localhost:5000/']

    def parse(self, response):
        params = {
            "username": "user",
            "password": "user12345"
        }

        return scrapy.FormRequest(
            dont_filter=True,
            url='http://localhost:5000/login',
            formdata=params,
            callback=self.after_login
        )

    def after_login(self, response):
        yield {"title": response.css("title::text").get()}
        pass
