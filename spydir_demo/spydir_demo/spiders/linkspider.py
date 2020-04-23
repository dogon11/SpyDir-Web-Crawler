# -*- coding: utf-8 -*-
import sys
import scrapy
import logging
from scrapy.linkextractors import LinkExtractor
from ..items import LinkScrapeItem
from scrapy.spiders import Rule, CrawlSpider

class LinkSpider(CrawlSpider):
    name = "linkspider"
    rules = [Rule(LinkExtractor(canonicalize=True, unique=True), callback="parse_items")] #Gets all links in a webpage, calling parse_items.
    link_items = [] #Needs to exist in some form. Used to retrieve list of dicts storing the links found and their web location.
    
    def parse_items(self, response):
        links = LinkExtractor(canonicalize=True, unique=True).extract_links(response) #Extracts all links on the page.
        for link in links:
            link_item = LinkScrapeItem() #Produces an Item that contains the scraped link to fill out fields.
            link_item['url_from'] = response.url
            link_item['url_to'] = link.url
            self.link_items.append(link_item) #Appends to returnable list.
