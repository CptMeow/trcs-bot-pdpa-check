import datetime
import re
import scrapy
from urllib.parse import urlparse
from .__init__ import BaseSpider
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class AllSite(BaseSpider):
    name = 'allsite'
    start_urls = [
        'http://medcertificate.somdej.or.th',
        'https://www.redcross.or.th',
        'https://adminis.redcross.or.th',
        'https://audit.redcross.or.th',
        'https://blooddonationthai.com',
        'https://centralb.redcross.or.th',
        'https://centralb.redcross.or.th/sawangkanives',
        'https://chapter.redcross.or.th',
        'https://chapternews.redcross.or.th',
        'https://clipping.redcross.or.th',
        'https://covid19.redcross.or.th',
        'https://ebook.redcross.or.th',
        'https://elearning.redcross.or.th',
        'https://english.redcross.or.th',
        'https://eyebankthai.redcross.or.th',
        'https://finance.redcross.or.th',
        'https://hrtrcs.redcross.or.th',
        'https://intranet.redcross.or.th',
        'https://it.redcross.or.th',
        'https://jobtrc.redcross.or.th',
        'http://jobtrc.redcross.or.th/newjob/admin/new-pdpa.php',
        'https://khaolan.redcross.or.th'
        'https://ncp.redcross.or.th/',
        'https://oim.redcross.or.th/',
        'https://plant.redcross.or.th',
        'https://portal.redcross.or.th',
        'https://procurement.redcross.or.th',
        'https://property.redcross.or.th',
        'https://rehab.redcross.or.th',
        'https://somdej.or.th',
        'https://strategy.redcross.or.th/',
        'https://thaircy.redcross.or.th',
        'https://thaircy.redcross.or.th/thaircy100Anniversary',
        'https://thethairedcrosssociety.sharepoint.com/SitePages/สำนักกฎหมาย-สภากาชาดไทย.aspx',
        'https://trcch.redcross.or.th',
        'https://trcroadsafety.redcross.or.th',
        'https://vb.redcross.or.th',
        'https://www.redcross.or.th',
        'https://youdee.redcross.or.th',
    ]

    allowed_domains = [
        'adminis.redcross.or.th',
        'audit.redcross.or.th',
        'blooddonationthai.com',
        'centralb.redcross.or.th',
        # 'centralb.redcross.or.th/sawangkanives',
        'chapter.redcross.or.th',
        'chapternews.redcross.or.th',
        'clipping.redcross.or.th',
        'covid19.redcross.or.th',
        'ebook.redcross.or.th',
        'elearning.redcross.or.th',
        'english.redcross.or.th',
        'eyebankthai.redcross.or.th',
        'finance.redcross.or.th',
        'hrtrcs.redcross.or.th',
        'intranet.redcross.or.th',
        'it.redcross.or.th',
        'jobtrc.redcross.or.th',
        'khaolan.redcross.or.th'
        'medcertificate.somdej.or.th',
        'ncp.redcross.or.th',
        'oim.redcross.or.th',
        'plant.redcross.or.th',
        'portal.redcross.or.th',
        'procurement.redcross.or.th',
        'property.redcross.or.th',
        'rehab.redcross.or.th',
        'somdej.or.th',
        'strategy.redcross.or.th',
        'thaircy.redcross.or.th',
        'thaircy.redcross.or.th/thaircy100Anniversary',
        'thethairedcrosssociety.sharepoint.com',
        'trcch.redcross.or.th',
        'trcroadsafety.redcross.or.th',
        'vb.redcross.or.th',
        'www.redcross.or.th',
        'youdee.redcross.or.th',
    ]
    # rules = (
    #     Rule(LinkExtractor(allow_domains=('redcross\.or\.th','somdej\.or\.th' ),deny=('.+\.com', ))),
    # )


    def parse(self, response):

        for item in response.css('label, input[type=text], input[type=hidden], textarea, select>option'):
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