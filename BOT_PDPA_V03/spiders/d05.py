import datetime
import re
import scrapy
from urllib.parse import urlparse
from .__init__ import BaseSpider

class D05(BaseSpider):
    name = 'd05'
    start_urls = [
        'https://thaircy.redcross.or.th',
        'https://thaircy.redcross.or.th/thaircy100Anniversary',
        'https://plant.redcross.or.th',
        'https://youdee.redcross.or.th',

    ]

    allowed_domains = [
        'thaircy.redcross.or.th',
        'thaircy.redcross.or.th/thaircy100Anniversary',
        'plant.redcross.or.th',
        'youdee.redcross.or.th',
    ]

    DENY_PATH = [
        '\/ปฎิทิน\/', 'calendar', 'wp-content', '\?ical', 'events'
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