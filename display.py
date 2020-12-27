# This was created by Danila Popel and Nikita Popel. This project was originally created on December 24th, 2020.
from bs4 import BeautifulSoup
import urllib.request, os, platform, time, csv, requests
from datetime import datetime, timedelta, date
from scraper import *
from tkinter import *
from tkinter.ttk import *
import numpy as np
import matplotlib.dates as mdates
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
"""
"""

class GUI:
    def __init__(self):
        #tk_theme = [['light',['#000','#fff'],['#888','#fff'],['#aaa','#000']],['dark',['#fff','#000'],['#fff','#888'],['#000','#aaa']]]
        self.gui_theme = ['white','']


        self.window = Tk()
        width, height = self.window.winfo_screenwidth(), self.window.winfo_screenheight()
        self.window.geometry('%dx%d+0+0' % (width,height))
        #self.window.resizable(width = False, height = False)
        self.window.title("Stonk Scraper")
        #self.window.geometry('1400x480')
        photo = PhotoImage(file = "cashmoney.png")
        self.range_options = ['SELECT RANGE', 'Week', 'Month', '3 Months', '6 Months', 'Year', 'All Time']
        self.var1 = StringVar(self.window)
        self.var1.set(self.range_options[0])
        self.window.iconphoto(False, photo)
        self.window.configure(background = self.gui_theme[0])
        self.userprompt = Label(self.window, font = ('Arial', 16, 'bold'), text = "Enter Stock Name: ", background = self.gui_theme[0])
        self.userentry = Entry(self.window, font=('courier new',16,'bold'))
        self.rangedrop = OptionMenu(self.window, self.var1, *self.range_options)
        self.enterbutton = Button(self.window, text = 'Enter', command = self.search)
        self.stockname = Label(self.window, font = ('Arial', 16, 'bold'), text = "Stock Name: ", background = self.gui_theme[0])
        self.current_stockname = Label(self.window, font = ('courier new', 16, 'bold', ), text = "", background = self.gui_theme[0])
        self.date = Label(self.window, font = ('Arial', 16, 'bold'), text = "Date: ", background = self.gui_theme[0])
        self.current_date = Label(self.window, font = ('courier new', 16, 'bold'), text = "", background = self.gui_theme[0])
        self.openingprice = Label(self.window, font = ('Arial', 16, 'bold'), text = "Opening: ", background = self.gui_theme[0])
        self.current_openingprice = Label(self.window, font = ('courier new', 16, 'bold'), text = "", background = self.gui_theme[0])
        self.closingprice = Label(self.window, font = ('Arial', 16, 'bold'), text = "Closing: ", background = self.gui_theme[0])
        self.current_closingprice = Label(self.window, font = ('courier new', 16, 'bold'), text = "", background = self.gui_theme[0])
        self.dailylow = Label(self.window, font = ('Arial', 16, 'bold'), text = "Daily Low: ", background = self.gui_theme[0])
        self.current_dailylow = Label(self.window, font = ('courier new', 16, 'bold'), text = "", background = self.gui_theme[0])
        self.dailyhigh = Label(self.window, font = ('Arial', 16, 'bold'), text = "Daily High: ", background = self.gui_theme[0])
        self.current_dailyhigh = Label(self.window, font = ('courier new', 16, 'bold'), text = "", background = self.gui_theme[0])
        self.dailyvolume = Label(self.window, font = ('Arial', 16, 'bold'), text = "Daily Volume: " , background = self.gui_theme[0])
        self.current_dailyvolume = Label(self.window, font = ('courier new', 16, 'bold') , text = "" , background = self.gui_theme[0])
        self.userprompt.grid(row = 7, column = 0)
        self.userentry.grid(row = 7, column = 1)
        self.rangedrop.grid(row = 7, column = 2)
        self.enterbutton.grid(row = 7, column = 3)
        self.stockname.grid(row = 0, column = 4, sticky='e')
        self.current_stockname.grid(row = 0, column = 5, sticky='w')
        self.date.grid(row = 1, column = 4, sticky='e')
        self.current_date.grid(row = 1, column = 5, sticky='w')
        self.openingprice.grid(row = 2, column = 4, sticky='e')
        self.current_openingprice.grid(row = 2, column = 5, sticky='w')
        self.closingprice.grid(row = 3, column = 4, sticky='e')
        self.current_closingprice.grid(row = 3, column = 5, sticky='w')
        self.dailylow.grid(row = 4, column = 4, sticky='e')
        self.current_dailylow.grid(row = 4, column = 5, sticky='w')
        self.dailyhigh.grid(row = 5, column = 4, sticky='e')
        self.current_dailyhigh.grid(row = 5, column = 5, sticky='w')
        self.dailyvolume.grid(row = 6, column = 4, sticky='e')
        self.current_dailyvolume.grid(row = 6, column = 5, sticky='w')

        self.userstocksymbol = '%5EGSPC'
        self.currstock = Stock(0,self.userstocksymbol)
        self.current_stockname['text'] = self.currstock.getName()
        self.current_date['text'] = date(year=int(self.currstock.getCurrent()[0][0:4]),month=int(self.currstock.getCurrent()[0][5:7]),day=int(self.currstock.getCurrent()[0][8:10])).strftime('%d %B, %Y (%A)')
        self.current_openingprice['text'] = '$' + str(round(float(self.currstock.getCurrent()[1]),2))
        self.current_closingprice['text'] = '$' + str(round(float(self.currstock.getCurrent()[4]),2))
        self.current_dailylow['text'] = '$' + str(round(float(self.currstock.getCurrent()[3]),2))
        self.current_dailyhigh['text'] = '$' + str(round(float(self.currstock.getCurrent()[2]),2))
        self.current_dailyvolume['text'] = str(round(int(self.currstock.getCurrent()[6]),2)) + ' shares'

        fig = Figure(figsize=(10, 8), dpi=100)
        closingprices = [round(float(i[4]),2) for i in self.currstock.getHistory()]
        dates = [datetime(int(i[0][0:4]),int(i[0][5:7]), int(i[0][8:10])) for i in self.currstock.getHistory()]
        fig.add_subplot(111).plot_date(dates,closingprices, '-', linewidth = 0.5)
        canvas = FigureCanvasTkAgg(fig, master = self.window)
        canvas.get_tk_widget().grid(row = 0, column = 0, rowspan = 7, columnspan = 4)

        #self.menu_thing()

        self.window.mainloop()

    def search(self):
        self.userstocksymbol = self.userentry.get()
        self.currstock = Stock(0,self.userstocksymbol)
        self.currentvalues = self.currstock.plotStock(self.var1.get())
        fig = Figure(figsize=(10, 8), dpi=100)
        self.closingprices = [round(float(i[1]),2) for i in self.currentvalues]
        self.dates = [datetime(int(i[0][0:4]),int(i[0][5:7]), int(i[0][8:10])) for i in self.currentvalues]
        fig.add_subplot(111).plot_date(self.dates,self.closingprices, '-', linewidth = 0.5, linestyle = 'solid')
        canvas = FigureCanvasTkAgg(fig, master = self.window)
        canvas.get_tk_widget().grid(row = 0, column = 0, rowspan = 7, columnspan = 3)
        self.current_stockname['text'] = self.currstock.getName()
        self.current_date['text'] = date(year=int(self.currstock.getCurrent()[0][0:4]),month=int(self.currstock.getCurrent()[0][5:7]),day=int(self.currstock.getCurrent()[0][8:10])).strftime('%d %B, %Y (%A)')
        self.current_openingprice['text'] = '$' + str(round(float(self.currstock.getCurrent()[1]),2))
        self.current_closingprice['text'] = '$' + str(round(float(self.currstock.getCurrent()[4]),2))
        self.current_dailylow['text'] = '$' + str(round(float(self.currstock.getCurrent()[3]),2))
        self.current_dailyhigh['text'] = '$' + str(round(float(self.currstock.getCurrent()[2]),2))
        self.current_dailyvolume['text'] = str(round(int(self.currstock.getCurrent()[6]),2)) + ' shares'

    def menu_thing(self):
        # call main 'menubar'
        menubar = Menu(self.window)

        # call 'menubar' 'File' submenu
        menubar_file = Menu(menubar, tearoff=0)
        menubar.add_cascade(label='File',underline=0,menu=menubar_file)
        menubar_file.add_command(label='Theme',underline=0,command=self.theme)
        menubar_file.add_separator()

        # call 'menubar' 'help' submenu
        menubar_help = Menu(menubar, tearoff=0)
        menubar.add_cascade(label='Help',underline=0,menu=menubar)
        menubar_help.add_command(label='About',underline=0,command=print('About'))
        menubar_help.add_separator()
        menubar_help.add_command(label='stonkscraper-v2')

        # add quit to end of 'menubar'
        menubar.add_command(label='Exit',underline=0,command=self.quit)

        # add main 'menubar' to tkinter.Tk() 'window'
        self.window.config(menu=menubar)

    def quit(self):
        quit()

    def theme(self):
        print('CHANGE THEME!!!')

    #def quit(self):
    #    quit()
