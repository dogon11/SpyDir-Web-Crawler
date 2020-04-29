import tkinter as tk
import scrape_driver
import tree_visualization
from tkinter.filedialog import askopenfilename
from functools import partial
from subprocess import Popen
from shlex import quote
from os import name as osname
from os.path import basename

ITEM_LIST = []
FILE_NAME = "output"
HAS_BEEN = False

def viewData():
	csv_path = quote(basename(askopenfilename()))
	if csv_path == "''":
		return
	elif osname == 'nt':
		Popen([csv_path], shell=True)
	else:
		Popen(["open", csv_path], shell=True)

def viewTree():
	#unfinished
	tree_visualization.gen_tree(ITEM_LIST, FILE_NAME)

def genList(filename):
	global ITEM_LIST
	ITEM_LIST = scrape_driver.parseCSV(filename)

def changeFilename(listButtons):
	global FILE_NAME
	global HAS_BEEN
	file_store = FILE_NAME
	try:		
		FILE_NAME = scrape_driver.getFile()
	except FileNotFoundError:
		FILE_NAME = file_store
	finally:
		if FILE_NAME is None:
			FILE_NAME = file_store
			return
		genList((FILE_NAME + ".csv"))	
		if not HAS_BEEN:
			for item in listButtons:
				item.pack()
			HAS_BEEN = True
	
def genClick(e1, e2, e3, genLabel, gendLabel, default1, default2, root, hideLabels = [], showLabels = []):
	global ITEM_LIST
	global FILE_NAME
	gendLabel.pack_forget()
	for hide in hideLabels:
		hide.pack_forget()
	arg1 = e1.get()
	arg2 = e2.get()
	FILE_NAME = e3.get()
	if FILE_NAME == "Enter filename for .csv (Default: output)":
		FILE_NAME = "output"
	if(arg1==default1 or arg2==default2):	#tried to make a check for invalid params but couldnt get this to work right
		warnLabel = tk.Label(root, text="Enter parameters!")
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

def runSearch(trueLabel, falseLabel, urlEntry, filename):
	url = urlEntry.get()
	if scrape_driver.search(url, filename):		
		falseLabel.pack_forget()
		trueLabel.pack()
	else:
		trueLabel.pack_forget()
		falseLabel.pack()

def search():
	global FILE_NAME
	searchWindow = tk.Toplevel()
	promptLabel = tk.Label(searchWindow, text="Input the FULL URL you want to search for:")
	enter = tk.Entry(searchWindow, width = 100, borderwidth = 5) #searched url
	trueLabel = tk.Label(searchWindow, text="That URL exists in the tree.")
	falseLabel = tk.Label(searchWindow, text="That URL does not exist in the tree.")
	runSearchButton = tk.Button(searchWindow, text="Search for URL", padx=50, command=partial(runSearch, trueLabel, falseLabel, enter, (FILE_NAME + ".csv")))
	quitButton = tk.Button(searchWindow, text="Go back", command=searchWindow.destroy)
	promptLabel.pack()
	enter.pack()
	runSearchButton.pack()	
	quitButton.pack()
	searchWindow.mainloop()

def main():
	root = tk.Tk()
	root.title("SpyDir ;))")
	cwdLabel = tk.Label(root, text=("Current working directory: " + getcwd()))
	e1 = tk.Entry(root, width = 100, borderwidth = 5) #start URL
	e2 = tk.Entry(root, width = 100, borderwidth = 5) #allowed domain
	e3 = tk.Entry(root, width = 100, borderwidth = 5) #CSV filename
	cwdLabel.pack()
	e1.pack()
	e2.pack()
	e3.pack()

	genLabel = tk.Label(root, text="Generating...")
	gendLabel = tk.Label(root, text="Generated! :)")
	#treeLabel = tk.Label(root, text="Tree:")	
	orLabel = tk.Label(root, text="Or:")

	viewButton = tk.Button(root, text="View dataset", padx=50, command=viewData, bg="#ffffff")
	treeButton = tk.Button(root, text="View Tree", padx=50, command=viewTree, bg="#ffffff")
	searchButton = tk.Button(root, text="Search for URL", padx=50, command=search, bg="#ffffff")
	listButtons = [viewButton, treeButton, searchButton]
	loadButton = tk.Button(root, text="Load .csv on system", padx = 50, command=partial(changeFilename, listButtons), bg="#ffffff")
	quitButton = tk.Button(root, text="Quit", command=root.destroy)

	default1 = "Enter root domain"
	default2 = "Enter domain restriction"
	default3 = "Enter filename for .csv (Default: output)"
	e1.insert(tk.END, default1)
	e2.insert(tk.END, default2)
	e3.insert(tk.END, default3)
	runSpiderButton = tk.Button(root, text="Run Spider !", padx=50, command=partial(genClick, e1, e2, e3, genLabel, gendLabel, default1, default2, root, listButtons, listButtons), bg="#ffffff")
	runSpiderButton.pack()
	orLabel.pack()
	loadButton.pack()
	quitButton.pack()
	root.mainloop()

if __name__ == '__main__':
	main()
