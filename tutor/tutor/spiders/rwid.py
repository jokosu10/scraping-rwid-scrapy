# -*- coding: utf-8 -*-
from typing import List

import scrapy
from cssselect import Selector


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
            url='http://localhost:5000/login',
            formdata=params,
            callback=self.after_login,
            dont_filter=True,
        )

    def after_login(self, response):
        # get detail products
        detail_products = response.css(".card .card-title a")
        for detail_product in detail_products:
            url_href = detail_product.attrib.get("href")
            yield response.follow(url_href, callback=self.parse_detail, dont_filter=True)

        # get pagination
        paginations = response.css("ul.pagination a.page-link")
        for pagination in paginations:
            url_href = pagination.attrib.get("href")
            yield response.follow(url_href, callback=self.after_login, dont_filter=True)

    def parse_detail(self, response):
        image = response.css(".card-img-top").attrib.get("src")
        title = response.css(".card-title::text").get()
        stock = response.css(".card-stock::text").get()
        description = response.css(".card-text::text").get()

        return {
            "image": image,
            "title": title,
            "stock": stock,
            "description": description
        }
