"""

@version 1.0.0

This implentation was a test run for just getting the spider to 
pull data from a website. its pulling quotes from a test website
scrapy has provided however the urls can be swapped

This assumes that the user knows a little bit about the metadata of
the site theyre pulling such as certain tags that the website uses
to identify different pieces of data (i.e this site used the tag quotes to 
classify the text that is a quote. I think tags and tag names are defined by the
web dev).
Therefore, someone using a spider needs to inspect the element of 
the site theyre trying to scrape and find the tags that they want to
look for

in our case, a strings search could be done simply by pulling ALL html
code from a site and then we could just run a basic string search on that
data and return the line from the data

however, scrapy has tools for this i just dont know how to use them yet lmao

so basically the biggest hurdle for right now is just creating a generic spider that
can just be given parameters like a url and tags/strings to look for
and it will generate a spider based off of that info 

"""
import sys
import scrapy
import logging

class QuotesSpider(scrapy.Spider):
    name = "quotes" #every spider needs a name for calling. basically identifier
    start_urls = [	#url(s) to traverse. In this implenetation, they are traversed recursively so only the one is needed
        'http://quotes.toscrape.com/page/1/',
    ]

    def parse(self, response):		#parsing function. where the data being pulled is defined and how it is being stored is also defined
        for quote in response.css('div.quote'):	#scrapy uses css and xml code to identify strings of data
            yield {
                'text': quote.css('span.text::text').get(),
                'author': quote.css('small.author::text').get(),
                'tags': quote.css('div.tags a.tag::text').getall(),
            }
        #the recursive call. Basically, if there are no more pages to look at in this domain, 
        #the spider is done scraping
        next_page = response.css('li.next a::attr(href)').get() 
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
