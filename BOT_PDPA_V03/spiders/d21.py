import datetime
import re
import scrapy
from urllib.parse import urlparse
from .__init__ import BaseSpider

class D21(BaseSpider):
    name = 'd21'
    start_urls = [
        'https://www.redcross.or.th',
        'https://english.redcross.or.th',
        'https://covid19.redcross.or.th',
        'https://procurement.redcross.or.th',
        'https://it.redcross.or.th',
        'https://intranet.redcross.or.th',
        'https://elearning.redcross.or.th',
        'https://portal.redcross.or.th',
        'https://portal.redcross.or.th/signing',
        'https://ebook.redcross.or.th',
        'https://clipping.redcross.or.th',
    ]

    allowed_domains = [
        'www.redcross.or.th',
        'english.redcross.or.th',
        'covid19.redcross.or.th',
        'procurement.redcross.or.th',
        'it.redcross.or.th',
        'intranet.redcross.or.th',
        'elearning.redcross.or.th',
        'portal.redcross.or.th',
        'ebook.redcross.or.th',
        'clipping.redcross.or.th',
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