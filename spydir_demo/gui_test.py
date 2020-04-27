from tkinter import *
import scrape_driver
from tkinter.filedialog import askopenfilename
from functools import partial

def viewData():
	global v
	csv_path = askopenfilename()
	print(csv_path)
	v.set(csv_path)

def viewTree():
	#unfinished
	treeLabel = Label(root, text="Tree")

def genClick(e1, e2, default1, default2, root):
	arg1 = e1.get()
	arg2 = e2.get()
	if(arg1 is default1 or arg2 is default2):	#tried to make a check for invalid params but couldnt get this to work right
		warnLabel = Label(root, text="Enter parameters!")
		warnLabel.pack()
	else:
		returnList = []
		input_urls = [arg1] #This has to be a list or scrapy breaks
		input_domains = [arg2] #Ditto here.
		print(input_domains)
		returnList = scrape_driver.getLinks(input_urls, input_domains, "output.csv")
		print(returnList)
		myLabel = Label(root, text="Generating...")
		myLabel.pack()
		myButton2 = Button(root, text="View Data Set", padx=50, command=viewData, bg="#ffffff")
		myButton2.pack()
		myButton3 = Button(root, text="View Tree", padx=50, command=viewTree, bg="#ffffff")
		myButton3.pack()

def main():
	root = Tk()
	root.title("SpyDir ;))")
	e1 = Entry(root, width = 100, borderwidth = 5) #start URL
	e2 = Entry(root, width = 100, borderwidth = 5) #allowed domain
	#e3 = Entry(root, width = 100, borderwidth = 5)
	e1.pack()
	e2.pack()
	#e3.grid(row = 0, column = 2, columnspan=3, padx = 10, pady = 10)
	default1 = "Enter root domain"
	default2 = "Enter domain restriction"
	e1.insert(END, default1)
	e2.insert(END, default2)
	#e3.insert(0, "(Optional) Enter string to search")
	runSpiderButton = Button(root, text="Run Spider !", padx=50, command=partial(genClick, e1, e2, default1, default2, root), bg="#ffffff")
	quit = Button(root, text="Quit", command=root.destroy)
	runSpiderButton.pack()
	quit.pack()
	root.mainloop()

if __name__ == '__main__':
	main()