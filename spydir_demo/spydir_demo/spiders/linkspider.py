# -*- coding: utf-8 -*-
import sys
import scrapy
import logging
from scrapy.linkextractors import LinkExtractor
from ..items import LinkScrapeItem
from scrapy.spiders import Rule, CrawlSpider

ALLOWED_DOMAINS = ['mason.gmu.edu/~abenavi']
BROAD = False

class LinkspiderSpider(CrawlSpider):
    name = "linkspider"
    start_urls = ['http://mason.gmu.edu/~abenavi/index']
    allowed_domains = ['mason.gmu.edu']
    """ if not BROAD:
        allowed_domains = ALLOWED_DOMAINS """
    rules = [Rule(LinkExtractor(canonicalize=True, unique=True), callback="parse_items")]
    
    def parse_items(self, response):
        link_items = []
        links = LinkExtractor(canonicalize=True, unique=True).extract_links(response)
        for link in links:
            """
            if not BROAD:
                allowed_domain = False
                for allowed_domain in ALLOWED_DOMAINS:
                    if allowed_domain in link.url:
                        allowed_domain = True
                if allowed_domain:
                    link_item = LinkScrapeItem()
                    link_item.url_from = response.url
                    link_item.url_to = link.url
            else:
                """
            link_item = LinkScrapeItem()
            link_item['url_from'] = response.url
            link_item['url_to'] = link.url
            print(response.url)
            print(link.url)
            link_items.append(link_item)
        return link_items
