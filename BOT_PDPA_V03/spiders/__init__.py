# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
from scrapy import Spider
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from urllib.parse import urlparse
import datetime
import re
import logging

class BaseSpider(Spider):
    # Do not give it a name so that it does not show up in the spiders list.
    # This contains only common functions.

    UNIQUE_DATA = set()

    UNIQUE_URL = set()

    DATASET_DATE = datetime.datetime.now()
    
    ALLOW_PROTOCALS = [
        'http://', 'https://',
    ]
# 1. `response.url.lower().endswith(tuple(self.IGNORED_EXTENSIONS)):`
#         - check if the url ends with any of the IGNORED_EXTENSIONS
#     2. `for item in response.css('label, input[type=text], input[type=hidden], textarea,
# select>option'):`
#         - loop through all the items in the response
#     3. `exists = self.checkPageDuplicate(item, response)`
#         - check if the item exists in the UNIQUE_DATA
#     4. `item = self.createRow(item, response)`
#         - create a row for the item
#     5. `if exists and (exists not in self.UNIQUE_DATA):`
#         - if the item exists and it's not in the UNIQUE_DATA
#     6. `self.UNIQUE_DATA.add(exists)`
#         - add the item to the UNIQUE_DATA
#     7. `yield item`
#         -

    DENY_PATH = [
        '\/ปฎิทิน\/', 
        'calendar', 
        'wp-content', 
        '\?ical', 
        'events', 
        '\?download', 
        'files', 
        '\?jet_download', 
        '\?month', 
        'attachments', 
        '\&uid', 
        'download',
        '\?c\=annual_report'
    ]

    DENY_DOMAIN = [
        'clipping.redcross.or.th',
        'eservice.redcross.or.th',
        'fmis.redcross.or.th',
        'fmislog.redcross.or.th',
        'room.redcross.or.th',
    ]

    POLICY_PAGES = [
        'policy',
        'นโยบาย',
        # 'cookie',
        'pdpa'
    ]

    IGNORED_EXTENSIONS = [
        # images
        'mng', 'pct', 'bmp', 'gif', 'jpg', 'jpeg', 'png', 'pst', 'psp', 'tif',
        'tiff', 'ai', 'drw', 'dxf', 'eps', 'ps', 'svg',

        # audio
        'mp3', 'wma', 'ogg', 'wav', 'ra', 'aac', 'mid', 'au', 'aiff',

        # video
        '3gp', 'asf', 'asx', 'avi', 'mov', 'mp4', 'mpg', 'qt', 'rm', 'swf', 'wmv',
        'm4a',

        # other
        'css', 'pdf', 'doc', 'exe', 'bin', 'rss', 'zip', 'rar', 'msi', 'docx', 'pptx', 'ppt', 'xlsx', 'xls', 'iso'
    ]

    def checkPageDuplicate(self, page, response, options=[]):


        parsed_uri = urlparse(response.url)
        domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)

        css = "'css': " + str(page.css('::attr(class)').get())
        id = "'id': " + str(page.css('::attr(id)').get())
        name = "'name': " + str(page.css('::attr(name)').get())
        text = "'text': " + str(page.css('::text, ::attr(placeholder)').get())
        # url = "'url': " + str(response.url)
        # exists = domain + css + id + name + text + url
        return domain + css + id + name + text
    
    def checkPDPA(self, next_page , response, options=[]):
        next_page = response.urljoin(next_page.get())
        parsed_uri = urlparse(next_page)
        domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
        
        IGNORED_EXTENSIONS = self.IGNORED_EXTENSIONS if not 'IGNORED_EXTENSIONS' in options else options['IGNORED_EXTENSIONS']

        if not next_page.lower().endswith(tuple(IGNORED_EXTENSIONS)): 
            if re.search("("+")|(".join(self.POLICY_PAGES)+")", next_page.lower()):
                logging.info('\033[92mPDPA PASS on %s\033[0m', response.url)
                return {
                    'domain': domain,
                    'css': '',
                    'id': '',
                    'name': '',
                    'text': 'PDPA_PASS',
                    'url': next_page.lower(),
                    'dataset_date': self.DATASET_DATE.strftime('%Y-%m-%d %H:%M:%S'),
                    'selector_type': ''
                }

    def selector(self, selector, response):
        for item in response.css(selector):
                exists = self.checkPageDuplicate(item, response)
                item = self.createRow(item, response, selector)
                if exists and (exists not in self.UNIQUE_DATA):
                    self.UNIQUE_DATA.add(exists)
                    return item

    def createRow(self, item, response, selector, options=[]):
        next_page = response.urljoin(item.get())
        parsed_uri = urlparse(next_page)
        domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
        
        ALLOW_PROTOCALS = self.ALLOW_PROTOCALS if not 'ALLOW_PROTOCALS' in options else options['ALLOW_PROTOCALS']
        DENY_PATH = self.DENY_PATH if not 'DENY_PATH' in options else options['DENY_PATH']
        IGNORED_EXTENSIONS = self.IGNORED_EXTENSIONS if not 'IGNORED_EXTENSIONS' in options else options['IGNORED_EXTENSIONS']

        if not next_page.lower().endswith(tuple(IGNORED_EXTENSIONS)): 
            return {
                    'domain': domain,
                    'css': item.css('::attr(class)').get(),
                    'id': item.css('::attr(id)').get(),
                    'name': item.css('::attr(name)').get(),
                    'text': str(item.css('::text, ::attr(placeholder)').get()).replace("\r\n", "").replace("\n", "").replace("\r", "").replace("\t", "").replace(" ", ""),
                    'url': response.url,
                    'dataset_date': self.DATASET_DATE.strftime('%Y-%m-%d %H:%M:%S'),
                    'selector_type': selector
                }

    # def validateRule(self, next_page ,response, options=[]):
    #     exists = next_page.get()
    #     next_page = response.urljoin(exists)
    def validateRule(self, response, options=[]):
        current_page = response
        ALLOW_PROTOCALS = self.ALLOW_PROTOCALS if not 'ALLOW_PROTOCALS' in options else options['ALLOW_PROTOCALS']
        DENY_DOMAIN = self.DENY_DOMAIN if not 'DENY_DOMAIN' in options else options['DENY_DOMAIN']
        DENY_PATH = self.DENY_PATH if not 'DENY_PATH' in options else options['DENY_PATH']
        IGNORED_EXTENSIONS = self.IGNORED_EXTENSIONS if not 'IGNORED_EXTENSIONS' in options else options['IGNORED_EXTENSIONS']

        if not re.search("("+")|(".join(DENY_DOMAIN)+")", current_page): 
            if current_page.startswith(tuple(ALLOW_PROTOCALS)): 
                if not current_page.endswith(tuple(IGNORED_EXTENSIONS)): 
                    if not re.search("("+")|(".join(DENY_PATH)+")", current_page):
                        return True
                    else:
                        logging.warning('\033[93mDENY PATH on %s\033[0m', current_page)
                        return False
                else:
                    logging.warning('\033[93mDENY EXTENSION on %s\033[0m', current_page)
                    return False
            else:
                logging.warning('\033[93mDENY PROTOCAL on %s\033[0m', current_page)
                return False
        else:
            logging.warning('\033[93mDENY DOMAIN on %s\033[0m', current_page)
            return False