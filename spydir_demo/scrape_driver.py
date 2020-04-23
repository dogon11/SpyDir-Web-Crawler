import scrapy
from scrapy.crawler import CrawlerProcess
from spydir_demo.spiders.linkspider import LinkSpider

import sys

#This function takes in a LIST of start urls and allowed domains to start the crawler,
#returning the list of dicts containing where the link was found and where it points.
def getLinks(start_urls, allowed_domains):
    process = CrawlerProcess()
    process.crawl(LinkSpider, start_urls=start_urls, allowed_domains=allowed_domains)
    process.start()
    return LinkSpider.link_items

#Main function to drive the current testing functionality. Takes two terminal inputs
#of the form [start URL] [allowed domains].
def main():
    returnList = []
    if len(sys.argv) < 3:
        print("Proper usage: >python scrape_driver.py [start URL] [allowed domains]")
    else:
        input_urls = [sys.argv[1]] #This has to be a list or scrapy breaks.
        input_domains = [sys.argv[2]] #Ditto here.
        returnList = getLinks(input_urls, input_domains)
        print(returnList)

if __name__ == '__main__':
    main()