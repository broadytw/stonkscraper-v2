# This was created by Danila Popel and Nikita Popel. This project was originally created on December 20th, 2020.
from bs4 import BeautifulSoup
import urllib.request, os, platform, time, csv, requests
from datetime import datetime, timedelta, date
from scraper import *
from tkinter import *
from tkinter.ttk import *
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
"""
def dateTranslate(inputDate):


    return date
"""
class GUI:
    def __init__(self):
        self.window = Tk()
        self.window.resizable(width = False, height = False)
        self.window.title("Stonk Scraper")
        self.window.geometry('1280x480')
        photo = PhotoImage(file = "cashmoney.png")
        self.window.iconphoto(False, photo)
        fig = Figure(figsize=(5, 4), dpi=100)
        t = np.arange(0, 3, .01)
        fig.add_subplot(111).plot(t, 2 * np.sin(2 * np.pi * t))
        canvas = FigureCanvasTkAgg(fig, master = self.window)
        canvas.get_tk_widget().grid(row = 0, column = 0, rowspan = 7, columnspan = 3)

        self.userprompt = Label(self.window, font = ('Arial', 16, 'bold'), text = "Enter Stock Name: ")
        self.userentry = Entry(self.window, font=('courier new',16,'bold'))
        self.enterbutton = Button(self.window, text = "Enter", command = self.search)
        self.stockname = Label(self.window, font = ('Arial', 16, 'bold'), text = "Stock Name: ")
        self.current_stockname = Label(self.window, font = ('courier new', 16, 'bold'), text = "")
        self.date = Label(self.window, font = ('Arial', 16, 'bold'), text = "Date: ")
        self.current_date = Label(self.window, font = ('courier new', 16, 'bold'), text = "")
        self.openingprice = Label(self.window, font = ('Arial', 16, 'bold'), text = "Opening: ")
        self.current_openingprice = Label(self.window, font = ('courier new', 16, 'bold'), text = "")
        self.closingprice = Label(self.window, font = ('Arial', 16, 'bold'), text = "Closing: ")
        self.current_closingprice = Label(self.window, font = ('courier new', 16, 'bold'), text = "")
        self.dailylow = Label(self.window, font = ('Arial', 16, 'bold'), text = "Daily Low: ")
        self.current_dailylow = Label(self.window, font = ('courier new', 16, 'bold'), text = "")
        self.dailyhigh = Label(self.window, font = ('Arial', 16, 'bold'), text = "Daily High: ")
        self.current_dailyhigh = Label(self.window, font = ('courier new', 16, 'bold'), text = "")
        self.dailyvolume = Label(self.window, font = ('Arial', 16, 'bold'), text = "Daily Volume: " )
        self.current_dailyvolume = Label(self.window, font = ('courier new', 16, 'bold') , text = "" )
        self.userprompt.grid(row = 7, column = 0, sticky='e')
        self.userentry.grid(row = 7, column = 1)
        self.enterbutton.grid(row = 7, column = 2, sticky='w')
        self.stockname.grid(row = 0, column = 3, sticky='e')
        self.current_stockname.grid(row = 0, column = 4, sticky='w')
        self.date.grid(row = 1, column = 3, sticky='e')
        self.current_date.grid(row = 1, column = 4, sticky='w')
        self.openingprice.grid(row = 2, column = 3, sticky='e')
        self.current_openingprice.grid(row = 2, column = 4, sticky='w')
        self.closingprice.grid(row = 3, column = 3, sticky='e')
        self.current_closingprice.grid(row = 3, column = 4, sticky='w')
        self.dailylow.grid(row = 4, column = 3, sticky='e')
        self.current_dailylow.grid(row = 4, column = 4, sticky='w')
        self.dailyhigh.grid(row = 5, column = 3, sticky='e')
        self.current_dailyhigh.grid(row = 5, column = 4, sticky='w')
        self.dailyvolume.grid(row = 6, column = 3, sticky='e')
        self.current_dailyvolume.grid(row = 6, column = 4, sticky='w')
        self.window.mainloop()

    def search(self):
        self.userstocksymbol = self.userentry.get()
        self.currstock = Stock(0,self.userstocksymbol)
        self.current_stockname['text'] = self.currstock.getName()
        self.current_date['text'] = date(year=int(self.currstock.getCurrent()[0][0:4]),month=int(self.currstock.getCurrent()[0][5:7]),day=int(self.currstock.getCurrent()[0][8:10])).strftime('%d %B, %Y (%A)')
        self.current_openingprice['text'] = '$' + str(round(float(self.currstock.getCurrent()[1]),2))
        self.current_closingprice['text'] = '$' + str(round(float(self.currstock.getCurrent()[4]),2))
        self.current_dailylow['text'] = '$' + str(round(float(self.currstock.getCurrent()[3]),2))
        self.current_dailyhigh['text'] = '$' + str(round(float(self.currstock.getCurrent()[2]),2))
        self.current_dailyvolume['text'] = str(round(int(self.currstock.getCurrent()[6]),2)) + ' shares'


if __name__ == '__main__':
    mygui = GUI()
    """
    # Welcome to the StonkScraper V1 (terminal)!
    prompt_inputstock = 'Enter the stock that you would like to look up?\n> '
    print('\n*********************************\n* Welcome to the Stonk Scraper! *\n*********************************')
    introloop = 1
    while introloop == 1:
        userstocksymbol = input(prompt_inputstock).upper()

        # If the 'userstocksymbol' exists in 'tickersymbols' stock symbol directory within 'checkExist()' on 'scraper.py'
        # After the 'userstocksymbol' input above, run 'checkExist()' from 'scraper.py' to check if the stock exists and return a bool value that allows the variable to pass into 'mainloop' wihle loop.
        # But if the 'userstocksymbol' does not pass 'checkExist()', the user is notified that their stock does not exist and 'introloop' while loop reruns to reprompt the user for a new input.
        if checkExist(userstocksymbol) == True:
            mainloop = 1
            while mainloop == 1:
                currstock = Stock(0,userstocksymbol)
                date_string = 'Date: ' + str(currstock.getCurrent()[0]) + ' ' * (40 - len('Date: ' + str(currstock.getCurrent()[0])))
                opening_string = 'Opening Price($): ' + str(round(float(currstock.getCurrent()[1]),2)) + ' ' * (40 - len('Opening Price($): ' + str(round(float(currstock.getCurrent()[1]),2))))
                closing_string = 'Closing Price($): ' + str(round(float(currstock.getCurrent()[4]),2)) + ' ' * (40 - len('Closing Price($): ' + str(round(float(currstock.getCurrent()[4]),2))))
                low_string = 'Daily Low($): ' + str(round(float(currstock.getCurrent()[3]),2)) + ' ' * (40 - len('Daily Low($): ' + str(round(float(currstock.getCurrent()[3]),2))))
                high_string = 'Daily High($): ' + str(round(float(currstock.getCurrent()[2]),2)) + ' ' * (40 - len('Daily High($): ' + str(round(float(currstock.getCurrent()[2]),2))))
                volume_string = 'Daily Volume: ' + str(round(float(currstock.getCurrent()[6]),2)) + ' ' * (40 - len('Daily Volume: ' + str(round(float(currstock.getCurrent()[6]),2))))
                name_string = '| ' + currstock.getName() + ' |\tExchange: ' + currstock.getExchange()
                out_line1 = '| ' + date_string + opening_string + closing_string + ' |'
                out_line2 = '| ' + low_string + high_string + volume_string + ' |'
                namelen = len(currstock.getName())
                print('\n' + (' ' * int((120 - namelen) / 2)) + '+' + ('-' * (namelen + 2)) + '+\n' + (' ' * int((120 - namelen) / 2)) + name_string)
                print('+' + ('-' * (int((120 - namelen) / 2)-1)) + '+' + ('-' * (namelen + 2)) + '+' + ('-' * (120 - (int((120 - namelen) / 2) - 1) - (namelen + 2))) + '+\n' + out_line1 + '\n' + out_line2 + '\n+' + ('-' * (len(out_line1)-2)) + '+')

                # 'stockloop' while loop is to prevent the user from wasting time continuously requesting info from the scraper using the 'Stock()'(currstock) from 'scraper.py'.
                # 'stockloop' asks for the 'userinput' input to retrieve content from stock.
                stockloop = 1
                while stockloop == 1:
                    userinput = input('\nWhat would you like to do next?\n[S]earch by Date\t[C]ompare over Time\t[N]ew Stock\t[Q]uit\n> ').upper()

                    # userinput Input: [S]earch by Date
                    # Search by Date asks for YYYY-MM-DD formatted date, checks for correct formatting.
                    # If the market was closed on the user's given day, the day's value will subtract until it reaches a market open day.
                    # As an output, the item in currstock.getHistory() with a matching date will be printed.
                    if userinput == 'S':
                        dateloop = 1
                        while dateloop == 1:
                            userinput_date = input('Input your desired date (Format: YYYY-MM-DD): ')
                            if isDate(userinput_date) == True:
                                print(currstock.fixDate(userinput_date))
                                dateloop = 0

                    # userinput Input: [C]ompare over Time
                    # Same checking process as in '[S]earch by Date' but for two user inputted values: date1(old date) & date2(new date)
                    # As an output, the percent return of the 'current price' between the date1(old date) and date2(new date) will be printed
                    elif userinput == 'C':
                        print('Input the dates in chronological order (Start Date first, then more Latest Date).')
                        dateloop = 1
                        while dateloop == 1:
                            userinput_date1 = input('Start Date (Format: YYYY-MM-DD): ')
                            if isDate(userinput_date1) == True:
                                userinput_date1 = currstock.fixDate(userinput_date1)[0]
                                dateloop = 0
                        dateloop = 1
                        while dateloop == 1:
                            userinput_date2 = input('Latest Date (Format: YYYY-MM-DD): ')
                            if isDate(userinput_date2) == True:
                                userinput_date2 = currstock.fixDate(userinput_date2)[0]
                                dateloop = 0
                        print(currstock.compareStock(userinput_date1,userinput_date2))

                    # userinput Input: [N]ew Stock
                    # Close the 'stockloop' while loop, reprompt user with 'mainloop' while loop
                    # In 'mainloop', if userinput is 'N', close 'mainloop', reprompt user with 'introloop' while loop
                    # In 'introloop', user is reprompted with 'userstocksymbol' input to select a new stock symbol to rerun the program.
                    elif userinput == 'N':
                        stockloop = 0

                    # userinput Input: [Q]uit
                    # Quit the program.
                    elif userinput == 'Q':
                        print('Quitting Program!')
                        quit()
                    else:
                        print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n! Try Again. That was not one of the options! !\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')

                # Continuation of 'stockloop' "if userinput == 'N'" statement!
                # If the 'stockloop' while loop is closed, the if statement below is prompted.
                # If the 'userinput' from 'stockloop' is 'N', close 'mainloop', reprompt user with 'introloop' while loop
                # In 'introloop', user is reprompted with 'userstocksymbol' input to select a new stock symbol to rerun the program.
                if userinput == 'N':
                    mainloop = 0
        else:
            print('You entry is not a valid stock symbol.')
"""
print('8===D')
