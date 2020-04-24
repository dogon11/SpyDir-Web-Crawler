import scrapy
from scrapy.crawler import CrawlerProcess
from spydir_demo.spiders.linkspider import LinkSpider

import sys
import csv

FILE_NAME = 'output.csv'

#This function takes in a LIST of start urls and allowed domains to start the crawler,
#returning the list of dicts containing where the link was found and where it points.
def getLinks(start_urls, allowed_domains, filename):
    process = CrawlerProcess() #settings={'FEED_FORMAT': 'csv', 'FEED_URI': filename} is the short fancy way, but won't work.
    process.crawl(LinkSpider, start_urls=start_urls, allowed_domains=allowed_domains) #Potential issues with allowed_domains: needs investigating.
    process.start()
    genCSV(filename, start_urls, LinkSpider.link_items)
    return LinkSpider.link_items

def genCSV(filename, start_urls, link_items):
    csv_file = open(filename, 'w', newline='')
    fields = ["url_from", "url_to"]
    writer = csv.DictWriter(csv_file, fieldnames=fields)
    writer.writeheader()
    for link in link_items:
        writer.writerow(link)
    csv_file.close()

#Main function to drive the current testing functionality. Takes two terminal inputs
#of the form [start URL] [allowed domains].
def main():
    returnList = []
    if len(sys.argv) < 3:
        print("Proper usage: >python scrape_driver.py [start URL] [allowed domains]")
    else:
        input_urls = [sys.argv[1]] #This has to be a list or scrapy breaks.
        input_domains = sys.argv[2:] #Ditto here.
        print(input_domains)
        returnList = getLinks(input_urls, input_domains, FILE_NAME)
        print(returnList)

if __name__ == '__main__':
    main()
