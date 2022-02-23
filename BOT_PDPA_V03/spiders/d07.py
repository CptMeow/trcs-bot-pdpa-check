import datetime
import re
import scrapy
from urllib.parse import urlparse
from .__init__ import BaseSpider

class D07(BaseSpider):
    name = 'd07'
    start_urls = [
        'https://blooddonationthai.com',

    ]

    allowed_domains = [
        'blooddonationthai.com',
    ]

    def parse(self, response):

        for item in response.css('label, input[type=text], input[type=hidden], textarea, select>option'):

            exists = self.checkPageDuplicate(item, response)
            item = self.createRow(item, response)
            if exists and (exists not in self.UNIQUE_DATA):
                self.UNIQUE_DATA.add(exists)
                yield item

        for next_page in response.css('a::attr(href)'):
            if self.validateRule(next_page,response):
                next_page_check = response.urljoin(next_page.get())
                if next_page_check and (next_page_check not in self.UNIQUE_URL):
                    self.UNIQUE_URL.add(next_page_check)
                    yield self.checkPDPA(next_page,response)
                    yield response.follow(next_page, callback=self.parse)