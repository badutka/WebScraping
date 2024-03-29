import re
from urllib.parse import urlparse

import scrapy
from scrapy import signals


# scrapy crawl pajaczek
class LinkCheckerSpider(scrapy.Spider):
    name = 'pajaczek'
    # Set the HTTP error codes that should be handled
    handle_httpstatus_list = [404]
    valid_url = ['pl.wikipedia.org']
    allowed_domains = ['pl.wikipedia.org']
    invalid_url = []
    # Set the maximum depth
    maxdepth = 5;
    domain = ''
    # https: // pl.wikipedia.org / wiki / Alianci
    # https: // pl.wikipedia.org / wiki / G % C5 % 82 % C3 % B3wna_(dop % C5 % 82yw_Warty)
    def __init__(self, url='https://pl.wikipedia.org/wiki/Krywicze', *args, **kwargs):
        super(LinkCheckerSpider, self).__init__(*args, **kwargs)
        self.start_urls = [url]

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(LinkCheckerSpider, cls).from_crawler(crawler, *args, **kwargs)
        # Register the spider_closed handler on spider_closed signal
        crawler.signals.connect(spider.spider_closed, signals.spider_closed)
        return spider

    def spider_closed(self):
        """ Handler for spider_closed signal."""
        print('----------')
        print('There are', len(self.valid_url), 'working links and',
              len(self.invalid_url), 'broken links.', sep=' ')
        if len(self.invalid_url) > 0:
            print('Broken links are:')
            for invalid in self.invalid_url:
                print(invalid)
        print('----------')

    @classmethod
    def parse(self, response):
        """ Main method that parse downloaded pages. """
        # Set defaults for the first page that won't have any meta information
        from_url = ''
        from_text = ''
        depth = 0;
        # Extract the meta information from the response, if any
        if 'from' in response.meta: from_url = response.meta['from']
        if 'text' in response.meta: from_text = response.meta['text']
        if 'depth' in response.meta: depth = response.meta['depth']

        # If first response, update domain (to manage redirect cases)
        if len(self.domain) == 0:
            parsed_uri = urlparse(response.url)
            self.domain = parsed_uri.netloc

        # 404 error, populate the broken links array
        if response.status == 404:
            self.invalid_url.append({'url': response.url,
                                     'from': from_url,
                                     'text': from_text})
        else:
            # print(response.text)
            # Populate the working links array
            self.valid_url.append({'url': response.url,
                                   'from': from_url,
                                   'text': from_text})

            # Extract domain of current page
            parsed_uri = urlparse(response.url)

            # ========= WRITING TO FILE =========

            cont = response.xpath('//p/text()').extract()
            cont = " ".join(cont)

            filepath = 'zapisy2/'
            filename = response.url[-15:].replace("/", "-")

            if len(cont) > 20:
                with open(filepath+filename+'.txt', "w", encoding="utf-8") as f:
                    f.write(cont)

            # ========= WRITING TO FILE =========

            # Parse new links only:
            #   - if current page is not an extra domain
            #   - and depth is below maximum depth
            if parsed_uri.netloc == self.domain and depth < self.maxdepth:
                # Get all the <a> tags
                a_selectors = response.xpath("//a")
                # Loop on each tag
                for selector in a_selectors:
                    # Extract the link text
                    text = selector.xpath('text()').extract_first()
                    # Extract the link href
                    link = selector.xpath('@href').extract_first()
                    # Create a new Request object
                    request = response.follow(link, callback=self.parse)
                    request.meta['from'] = response.url;
                    request.meta['text'] = text
                    # Return it thanks to a generator
                    yield request
