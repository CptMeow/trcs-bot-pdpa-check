import datetime
import re
import scrapy
from urllib.parse import urlparse
from .__init__ import BaseSpider
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class AllSite(BaseSpider):
    name = 'd16'
    start_urls = [
        'https://jobtrc.redcross.or.th',
    ]

    allowed_domains = [
        'jobtrc.redcross.or.th',
    ]
    # rules = (
    #     Rule(LinkExtractor(allow_domains=('redcross\.or\.th','somdej\.or\.th' ),deny=('.+\.com', ))),
    # )


    def parse(self, response):

        for item in response.css('label, input[type=text], input[type=hidden], textarea, select, select>option'):
            exists = self.checkPageDuplicate(item, response)
            item = self.createRow(item, response)
            if exists and (exists not in self.UNIQUE_DATA):
                self.UNIQUE_DATA.add(exists)
                yield item

        for next_page in response.css('a::attr(href)'):
            next_page_check = response.urljoin(next_page.get())
            if next_page_check and (next_page_check not in self.UNIQUE_URL):
                self.UNIQUE_URL.add(next_page_check)
                if self.validateRule(next_page,response):
                    yield self.checkPDPA(next_page,response)
                    yield response.follow(next_page, callback=self.parse)