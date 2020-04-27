import scrapy
import sys
import csv
import queue
import tkinter
import shutil
import os
import scrapy.crawler as crawler
from tkinter import filedialog
from scrapy.crawler import CrawlerProcess
from spydir_demo.spiders.linkspider import LinkSpider
from collections import defaultdict
from multiprocessing import Process, Queue, freeze_support
from twisted.internet import reactor

"""
# Code from the forkening:
def f(q, start_urls, allowed_domains):
    try:
        runner = crawler.CrawlerRunner()
        deferred = runner.crawl(LinkSpider, start_urls=start_urls, allowed_domains=allowed_domains)
        deferred.addBoth(lambda _: reactor.stop())
        reactor.run()
        q.put(LinkSpider.link_items)
    except Exception as e:
        q.put(None)
"""

#This function takes in a LIST of start urls and allowed domains to start the crawler,
#returning the list of dicts containing where the link was found and where it points.
def getLinks(start_urls, allowed_domains, filename):  
    #Old code before the forkening:
    process = CrawlerProcess() #settings={'FEED_FORMAT': 'csv', 'FEED_URI': filename} is the short fancy way, but won't work.
    process.crawl(LinkSpider, start_urls=start_urls, allowed_domains=allowed_domains, stop_after_crawl=False) #Potential issues with allowed_domains: needs investigating.
    process.start()
    link_items = removeCycles(start_urls, LinkSpider.link_items)
    genCSV(filename, start_urls, link_items)
    return link_items
    """
    # Code from the forkening:
    freeze_support()
    q = Queue()
    p = Process(target=f, args=(q, start_urls, allowed_domains))
    p.start()    
    p.join()
    result = removeCycles(start_urls, q.get())

    if result is not None:
        genCSV(filename, start_urls, result)
        return result
    """

#Helper function to return a list of all dict items where the "url_from" value matches the specified one.
def findByValue(desired_value, link_items):
    return_list = []
    for item in link_items:
        if item.get("url_from") == desired_value:
            return_list.append(item)
    return return_list

#Helper function to check if a list of dicts contains a certain "url_from" value.
def containsFrom(desired_value, link_items):
    for element in link_items:
        if element.get("url_from") == desired_value:
            return True
    return False

#Helper function to check if a list of dicts contains a certain "url_to" value.
def containsTo(desired_value, link_items):
    for element in link_items:
        if element.get("url_to") == desired_value:
            return True
    return False

#Helper function to check if a list of dicts contains a certain "url_to" or "url_from" value.
def containsEither(desired_value, link_items):
    for element in link_items:
        if (element.get("url_to") == desired_value) or (element.get("url_from") == desired_value):
            return True
    return False

#Helper function to remove all cycles from our graph to make it a tree. Returns a new list of dicts without cycles.
def removeCycles(start_urls, link_items):
    finished_list = []
    item_queue = queue.Queue()
    item_queue.put(start_urls[0])
    while not item_queue.empty():
        current_str = item_queue.get()
        current_items = findByValue(current_str, link_items)
        for item in current_items:
            if not containsEither(item.get("url_to"), finished_list):
                #then the item can be added. put it's "url_to" in the queue and add the item to the finished list.
                item_queue.put(item.get("url_to"))
                finished_list.append(item)
    return finished_list

def genCSV(filename, start_urls, link_items):
    csv_file = open(filename, 'w', newline='')
    fields = ["url_from", "url_to"]
    writer = csv.DictWriter(csv_file, fieldnames=fields)
    writer.writeheader()
    for link in link_items:
        writer.writerow(link)
    csv_file.close()
    
#Tries to open a system-native file browser to allow the user to navigate to a CSV,
#then tries to copy that file to the project directory and gets the new filename.
def getFile():
    filepath = filedialog.askopenfilename()
    shutil.copy(filepath, ".", follow_symlinks=True)
    return os.path.basename(filepath)
    
#Goes through the urls in the .csv file and checks them against a user inputted url.
#Requires a .csv file to work.
def search(filename):
    lables = defaultdict(list)
    isEqual = 0;
    string = input("What URL are you looking for: ")
    print ("\n")
    with open(filename) as f:
        reader = csv.reader(f)
        next(reader)  # skip the first line in the input file
        for i,row in enumerate(reader):
            lables[row[0]].append(row[1])
    for keys,values in lables.items():
        if keys == string:
            isEqual = 1
        for v in values:
            if v == string:
                isEqual = 1
    if isEqual == 1:
        print ("This URL: {} exists in the tree\n".format(string))
    else:
        print ("ERROR: The URL: {} does not exist in the tree\n".format(string))
        
#Main function to drive the current testing functionality. Takes two terminal inputs
#of the form [start URL] [allowed domains].
def main():
    filename = 'output.csv'
    returnList = []
    if len(sys.argv) < 3:
        print("Proper usage: >python scrape_driver.py [start URL] [allowed domains]")
    else:
        input_urls = [sys.argv[1]] #This has to be a list or scrapy breaks.
        input_domains = sys.argv[2:] #Ditto here.
        print(input_domains)
        returnList = getLinks(input_urls, input_domains, filename)
        print(returnList)

if __name__ == '__main__':
    main()
