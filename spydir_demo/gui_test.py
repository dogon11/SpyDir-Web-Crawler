from tkinter import *
import scrape_driver
import tree_visualization
from tkinter.filedialog import askopenfilename
from functools import partial
from spydir_demo.spiders.linkspider import LinkSpider
from scrapy.crawler import CrawlerProcess, CrawlerRunner, Crawler
ITEM_LIST = []
FILE_NAME = "output"

def viewData():
	global v
	csv_path = askopenfilename()
	print(csv_path)
	v.set(csv_path)

def viewTree():
	#unfinished
	tree_visualization.gen_tree(ITEM_LIST, FILE_NAME)

def genList(filename):
	global ITEM_LIST
	ITEM_LIST = scrape_driver.parseCSV(filename)

def changeFilename():
	global FILE_NAME
	try:
		FILE_NAME = scrape_driver.getFile()
	except FileNotFoundError:
		FILE_NAME = FILE_NAME
	finally:
		genList((FILE_NAME + ".csv"))	
	
def genClick(e1, e2, e3, genLabel, gendLabel, default1, default2, root, hideLabels = [], showLabels = []):
	global ITEM_LIST
	global FILE_NAME
	gendLabel.pack_forget()
	for hide in hideLabels:
		hide.pack_forget()
	arg1 = e1.get()
	arg2 = e2.get()
	FILE_NAME = e3.get()
	if(arg1==default1 or arg2==default2):	#tried to make a check for invalid params but couldnt get this to work right
		warnLabel = Label(root, text="Enter parameters!")
		warnLabel.pack()
	else:
		input_urls = [arg1] #This has to be a list or scrapy breaks
		input_domains = [arg2] #Ditto here.
		genLabel.pack()
		ITEM_LIST = scrape_driver.getLinks(input_urls, input_domains, (FILE_NAME + ".csv"))
		genLabel.pack_forget()
		gendLabel.pack()
		for show in showLabels:
			show.pack()

def main():
	root = Tk()
	root.title("SpyDir ;))")
	e1 = Entry(root, width = 100, borderwidth = 5) #start URL
	e2 = Entry(root, width = 100, borderwidth = 5) #allowed domain
	e3 = Entry(root, width = 100, borderwidth = 5) #CSV filename
	e1.pack()
	e2.pack()
	e3.pack()

	genLabel = Label(root, text="Generating...")
	gendLabel = Label(root, text="Generated! :)")
	treeLabel = Label(root, text="Tree:")

	viewButton = Button(root, text="View dataset", padx=50, command=viewData, bg="#ffffff")
	treeButton = Button(root, text="View Tree", padx=50, command=viewTree, bg="#ffffff")
	loadButton = Button(root, text="Load .csv on system", padx = 50, command=changeFilename, bg="#ffffff")

	listButtons = [viewButton, treeButton, loadButton]
	default1 = "Enter root domain"
	default2 = "Enter domain restriction"
	default3 = "Enter filename for .csv (Default: output)"
	e1.insert(END, default1)
	e2.insert(END, default2)
	e3.insert(END, default3)
	#e3.insert(0, "(Optional) Enter string to search")
	runSpiderButton = Button(root, text="Run Spider !", padx=50, command=partial(genClick, e1, e2, e3, genLabel, gendLabel, default1, default2, root, listButtons, listButtons), bg="#ffffff")
	quit = Button(root, text="Quit", command=root.destroy)
	runSpiderButton.pack()
	loadButton.pack()
	quit.pack()
	root.mainloop()

if __name__ == '__main__':
	main()
