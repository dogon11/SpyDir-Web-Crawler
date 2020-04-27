Edit (4/26/20, Justin Maddox):

Added Chris Tato's search by filename functionality inside scrape_driver.py, and added Chris Renfro's GUI driving script as "gui_test.py". GUI can be run from the command line by:

>python gui_test.py

Edit (4/24/20, Justin Maddox):

Changed again. Code runs from scrape_driver.py and outputs everything to 'output.csv'. Still prints to terminal. Added example CSV file to demonstrate format of output. 

Edit (4/23/20, Justin Maddox):

Changed this to add the ability to run the scraper from inside a python script. Currently, by running scrape_driver.py, the code will scrape the target demo website and print a list of dicts containing each found link and on what page it was found to the terminal. 

Edit (4/22/20, Justin Maddox):

Changed this to upload my proof-of-concept program that enables the traversal and pulling of links in scrapy. Output everything to a .csv file by navigating to the root directory of the project (spydir_demo) and typing:

>scrapy crawl -o [filename].[file extension(.csv works)] linkspider

=======================================================
https://docs.scrapy.org/en/latest/intro/tutorial.html
https://www.youtube.com/watch?v=ALizgnSFTwQ
https://www.youtube.com/watch?v=Wp6LRijW9wg

^^ mostly used the scrapy docs but those videos helped clarify a few things in the begining
