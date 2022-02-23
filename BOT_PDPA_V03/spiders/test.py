import datetime
import re
import scrapy
from urllib.parse import urlparse
from .__init__ import BaseSpider
from scrapy.linkextractors import LinkExtractor

class Test(BaseSpider):
    name = 'test'
    start_urls = [
        # 'http://localhost/test/test_bot_pdpa.html',
        'http://jobtrc.redcross.or.th/newjob/admin/new-pdpa.php'
    ]

    allowed_domains = [
        # 'localhost',
        'jobtrc.redcross.or.th'
    ]

    handle_httpstatus_list = [200]

    def parse(self, response):
        if not response.url.lower().endswith(tuple(self.IGNORED_EXTENSIONS)): 
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
        else:
            print('skip ',response.url.lower())
            for next_page in response.css('a::attr(href)'):
                for detail_page_url in LinkExtractor(restrict_css='a::attr(href)').extract_links(next_page):
                    url = response.urljoin(detail_page_url);
                    print('mkung',url)
                    yield response.follow(url, callback=self.parse)

        for next_page in LinkExtractor(restrict_css='a').extract_links(response):
            next_page_check = next_page.url
            if next_page_check and (next_page_check not in self.UNIQUE_URL):
                print('mkung',next_page.url,' ',response.url)
                yield response.follow(next_page.url, callback=self.parse, meta={'dont_redirect': True})