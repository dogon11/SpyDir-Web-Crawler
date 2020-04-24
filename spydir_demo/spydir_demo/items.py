# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LinkScrapeItem(scrapy.Item):
    url_from = scrapy.Field() # The source URL the link exists at.
    url_to = scrapy.Field() # The target URL the link points to.
