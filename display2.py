# This was created by Danila Popel and Nikita Popel. This project was originally created on December 20th, 2020.
from bs4 import BeautifulSoup
import urllib.request, os, platform, time, csv, requests
from datetime import datetime, timedelta, date
from scraper import *
from tkinter import *
from tkinter.ttk import *
from tkinter.messagebox import showinfo
import numpy as np
import matplotlib as mpl
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)

class mainMenu(Menu):
    def __init__(self,master=None):
        Menu.__init__(self)
        super().__init__(master)

        # call Menu 'barMenu'
        self.barMenu = Menu(self,tearoff=0)

        # 'File' cascade
        # w/ 'Theme','' commands
        fileMenu = Menu(self,tearoff=0)
        fileMenu.add_command(label='Theme',underline=0,command=self.changeTheme)
        fileMenu.add_separator()
        fileMenu.add_command(label='Ur mom gay!')
        self.add_cascade(label='File',underline=0,menu=fileMenu)

        # 'Edit' cascade
        # w/ '' commands
        editMenu = Menu(self,tearoff=0)
        editMenu.add_separator()
        self.add_cascade(label='Edit',underline=0,menu=editMenu)

        # 'Help' cascade
        # w/ 'About','' commands
        helpMenu = Menu(self,tearoff=0)
        helpMenu.add_command(label='About',underline=0,command=self.about)
        helpMenu.add_separator()
        helpMenu.add_command(label='stonkscraper-v2')
        self.add_cascade(label='Help',underline=0,menu=helpMenu)

        # 'Quit' command
        self.add_command(label='Exit',underline=1,command=self.quit)

    # popup about application
    def about(self):
        showinfo(title='About',message='2020\tstonkscraper-v2')

    # initialize theme change
    def changeTheme(self):
        global currtheme, app
        """
        theme_list = [i for i in theme]
        currtheme_index = theme_list.index(currtheme)
        if currtheme == theme_list[currtheme_index]:
            currtheme_index += 1
            """
        if currtheme == 'light':
            currtheme = 'dark'
        elif currtheme == 'dark':
            currtheme = 'light'
        showinfo(title='Ur mom gay!',message=f'currtheme = {currtheme}')
        app.destroy()
        app = tkui()
        app.mainloop()
        #tkui().changeTheme()

    # Call the standard python quit() function to quit program.
    def quit(self):
        quit()

# main frame
class mainFrame(Frame):
    def __init__(self,master):
        Frame.__init__(self,master)
        super().__init__(master)
        master.configure(borderwidth=1)
        master.geometry(f'{scr_dim[0]}x{scr_dim[1]}')

        # creating our four frames and plotting them onto the grid
        Style().configure('theme.TFrame', background = theme[currtheme]['main']['bg'])
        self.nwFrame = Frame(master, style='theme.TFrame')
        self.neFrame = Frame(master, style='theme.TFrame')
        self.swFrame = Frame(master, style='theme.TFrame')
        self.seFrame = Frame(master, style='theme.TFrame')
        self.nwFrame.grid(row=0,column=0)
        self.neFrame.grid(row=0,column=1)
        self.swFrame.grid(row=1,column=0)
        self.seFrame.grid(row=1,column=1)

        # creating our options for the drop down menu implemented later
        self.range_options = ['SELECT RANGE', 'Week', 'Month', '3 Months', '6 Months', 'Year', 'All Time', 'Custom']
        self.var1 = StringVar(self.swFrame)
        self.var1.set(self.range_options[0])

        # creating all of our required widgets for our southwest frame
        self.userprompt = Label(self.swFrame, font = ('Arial', 16, 'bold'), text = "Enter Stock Name: ", background = theme[currtheme]['main']['bg'], foreground = theme[currtheme]['main']['fg'])
        self.userentry = Entry(self.swFrame, font=('courier new',16,'bold'))
        self.rangedrop = OptionMenu(self.swFrame, self.var1, *self.range_options)
        self.enterbutton = Button(self.swFrame, text = 'Enter', command = self.search)
        self.usererror = Label(self.swFrame, font = ('courier new', 16, 'bold') , text = "" , background = theme[currtheme]['main']['bg'], foreground = 'red')
        self.cusdate_out = Label(self.swFrame, font = ('Arial', 16, 'bold'), text = 'Enter Custom Date (YYYY-MM-DD):', background = theme[currtheme]['main']['bg'], foreground = theme[currtheme]['main']['fg'])
        self.cusdate_entry = Entry(self.swFrame, font=('courier new',16,'bold'))

        # creating all of our required widgets for our northeast frames
        self.stockname = Label(self.neFrame, font = ('Arial', 16, 'bold'), text = "Stock Name: ", background = theme[currtheme]['main']['bg'], foreground = theme[currtheme]['main']['fg'])
        self.current_stockname = Label(self.neFrame, font = ('courier new', 16, 'bold', ), text = "", background = theme[currtheme]['main']['bg'], foreground = theme[currtheme]['main']['fg'])
        self.date = Label(self.neFrame, font = ('Arial', 16, 'bold'), text = "Date: ", background = theme[currtheme]['main']['bg'], foreground = theme[currtheme]['main']['fg'])
        self.current_date = Label(self.neFrame, font = ('courier new', 16, 'bold'), text = "", background = theme[currtheme]['main']['bg'], foreground = theme[currtheme]['main']['fg'])
        self.openingprice = Label(self.neFrame, font = ('Arial', 16, 'bold'), text = "Opening: ", background = theme[currtheme]['main']['bg'], foreground = theme[currtheme]['main']['fg'])
        self.current_openingprice = Label(self.neFrame, font = ('courier new', 16, 'bold'), text = "", background = theme[currtheme]['main']['bg'], foreground = theme[currtheme]['main']['fg'])
        self.closingprice = Label(self.neFrame, font = ('Arial', 16, 'bold'), text = "Closing: ", background = theme[currtheme]['main']['bg'], foreground = theme[currtheme]['main']['fg'])
        self.current_closingprice = Label(self.neFrame, font = ('courier new', 16, 'bold'), text = "", background = theme[currtheme]['main']['bg'], foreground = theme[currtheme]['main']['fg'])
        self.dailylow = Label(self.neFrame, font = ('Arial', 16, 'bold'), text = "Daily Low: ", background = theme[currtheme]['main']['bg'], foreground = theme[currtheme]['main']['fg'])
        self.current_dailylow = Label(self.neFrame, font = ('courier new', 16, 'bold'), text = "", background = theme[currtheme]['main']['bg'], foreground = theme[currtheme]['main']['fg'])
        self.dailyhigh = Label(self.neFrame, font = ('Arial', 16, 'bold'), text = "Daily High: ", background = theme[currtheme]['main']['bg'], foreground = theme[currtheme]['main']['fg'])
        self.current_dailyhigh = Label(self.neFrame, font = ('courier new', 16, 'bold'), text = "", background = theme[currtheme]['main']['bg'], foreground = theme[currtheme]['main']['fg'])
        self.dailyvolume = Label(self.neFrame, font = ('Arial', 16, 'bold'), text = "Daily Volume: " , background = theme[currtheme]['main']['bg'], foreground = theme[currtheme]['main']['fg'])
        self.current_dailyvolume = Label(self.neFrame, font = ('courier new', 16, 'bold') , text = "" , background = theme[currtheme]['main']['bg'], foreground = theme[currtheme]['main']['fg'])
        self.changeout = Label(self.neFrame, font = ('Arial', 16, 'bold') , text = "Change: " , background = theme[currtheme]['main']['bg'], foreground = theme[currtheme]['main']['fg'])
        self.current_change = Label(self.neFrame, font = ('courier new', 16, 'bold') , text = "" , background = theme[currtheme]['main']['bg'], foreground = theme[currtheme]['main']['fg'])

        # plotting all of our required widgets in the southwest frame
        self.userprompt.grid(row = 0, column = 0, sticky = 'e')
        self.userentry.grid(row = 0, column = 1, sticky = 'w')
        self.rangedrop.grid(row = 0, column = 2)
        self.enterbutton.grid(row = 0, column = 3)
        self.usererror.grid(row = 2, column = 0, columnspan = 4)

        # plotting all of our required widgets in the northeast frame
        self.stockname.grid(row = 0, column = 0, sticky='e')
        self.current_stockname.grid(row = 0, column = 1, sticky='w')
        self.date.grid(row = 1, column = 0, sticky='e')
        self.current_date.grid(row = 1, column = 1, sticky='w')
        self.openingprice.grid(row = 2, column = 0, sticky='e')
        self.current_openingprice.grid(row = 2, column = 1, sticky='w')
        self.closingprice.grid(row = 3, column = 0, sticky='e')
        self.current_closingprice.grid(row = 3, column = 1, sticky='w')
        self.dailylow.grid(row = 4, column = 0, sticky='e')
        self.current_dailylow.grid(row = 4, column = 1, sticky='w')
        self.dailyhigh.grid(row = 5, column = 0, sticky='e')
        self.current_dailyhigh.grid(row = 5, column = 1, sticky='w')
        self.dailyvolume.grid(row = 6, column = 0, sticky='e')
        self.current_dailyvolume.grid(row = 6, column = 1, sticky='w')
        self.changeout.grid(row = 7, column = 0, sticky = 'e')
        self.current_change.grid(row = 7, column = 1, sticky = 'w')

        # The code below initializes the program to display the S&P500 data for All Time
        self.userstocksymbol = '%5EGSPC'
        self.currstock = Stock(0,self.userstocksymbol)
        self.current_stockname['text'] = self.currstock.getName()
        self.current_date['text'] = date(year=int(self.currstock.getCurrent()[0][0:4]),month=int(self.currstock.getCurrent()[0][5:7]),day=int(self.currstock.getCurrent()[0][8:10])).strftime('%d %B, %Y (%A)')
        self.current_openingprice['text'] = '$' + str(round(float(self.currstock.getCurrent()[1]),2))
        self.current_closingprice['text'] = '$' + str(round(float(self.currstock.getCurrent()[4]),2))
        self.current_dailylow['text'] = '$' + str(round(float(self.currstock.getCurrent()[3]),2))
        self.current_dailyhigh['text'] = '$' + str(round(float(self.currstock.getCurrent()[2]),2))
        self.current_dailyvolume['text'] = str(round(int(self.currstock.getCurrent()[6]),2)) + ' shares'
        self.current_change['text'] = self.currstock.compareStock(str(self.currstock.getHistory()[0][0]), str(self.currstock.getCurrent()[0]))
        fig = Figure(figsize=(scr_dim[0]/200, scr_dim[1]/200), dpi=100)
        fig.set_facecolor(theme[currtheme]['main']['bg'])
        mpl.rcParams.update({
            'axes.facecolor':theme[currtheme]['main']['bg'],
            'axes.edgecolor':theme[currtheme]['main']['fg'],
            'xtick.color':theme[currtheme]['main']['fg'],
            'ytick.color':theme[currtheme]['main']['fg']
        })
        closingprices = [round(float(i[4]),2) for i in self.currstock.getHistory()]
        dates = [datetime(int(i[0][0:4]),int(i[0][5:7]), int(i[0][8:10])) for i in self.currstock.getHistory()]
        fig.add_subplot(111).plot_date(dates,closingprices, '-', linewidth = 1)
        canvas = FigureCanvasTkAgg(fig, master = self.nwFrame)
        canvas.get_tk_widget().grid(row = 0, column = 0)

        # This line below makes the program listen to the current status of the drop down menu.
        # If the drop down menu's currently highlighted item is changed, the method customdaterange is ran.
        self.var1.trace("w", self.customdaterange)

    # This method defined below enables the custome date entry fields to be visible if the drop down menu is set to 'Custom'.
    def customdaterange(self, *args):
        if(self.var1.get()) == 'Custom':
            self.cusdate_out.grid(row = 1, column = 0, sticky='e')
            self.cusdate_entry.grid(row = 1, column = 1, sticky= 'w')
        else:
            self.cusdate_out.grid_remove()
            self.cusdate_entry.grid_remove()

    # This method defined below searches for the stock entered into the text box.
    def search(self):
        self.userstocksymbol = str(self.userentry.get()).upper()
        self.userdate = str(self.cusdate_entry.get())
        if checkExist(self.userstocksymbol) == True:
            if self.userdate != '':
                correctdateformat = isDate(self.userdate)
                if correctdateformat != True:
                    self.usererror['text'] = '*ERROR*, Date format incorrect'
                else:
                    self.usererror['text'] = ''
            self.currstock = Stock(0,self.userstocksymbol)
            self.currentvalues = self.currstock.plotStock(self.var1.get(), self.userdate)
            fig = Figure(figsize=(scr_dim[0]/200, scr_dim[1]/200), dpi=100)
            fig.set_facecolor(theme[currtheme]['main']['bg'])
            mpl.rcParams.update({
                'axes.facecolor':theme[currtheme]['main']['bg'],
                'axes.edgecolor':theme[currtheme]['main']['fg'],
                'xtick.color':theme[currtheme]['main']['fg'],
                'ytick.color':theme[currtheme]['main']['fg']
            })
            self.closingprices = [round(float(i[1]),2) for i in self.currentvalues]
            self.dates = [datetime(int(i[0][0:4]),int(i[0][5:7]), int(i[0][8:10])) for i in self.currentvalues]
            fig.add_subplot(111).plot_date(self.dates,self.closingprices, '-', linewidth = 1)
            canvas = FigureCanvasTkAgg(fig, master = self.nwFrame)
            canvas.get_tk_widget().grid(row = 0, column = 0)
            self.current_stockname['text'] = self.currstock.getName()
            self.current_date['text'] = date(year=int(self.currstock.getCurrent()[0][0:4]),month=int(self.currstock.getCurrent()[0][5:7]),day=int(self.currstock.getCurrent()[0][8:10])).strftime('%d %B, %Y (%A)')
            self.current_openingprice['text'] = '$' + str(round(float(self.currstock.getCurrent()[1]),2))
            self.current_closingprice['text'] = '$' + str(round(float(self.currstock.getCurrent()[4]),2))
            self.current_dailylow['text'] = '$' + str(round(float(self.currstock.getCurrent()[3]),2))
            self.current_dailyhigh['text'] = '$' + str(round(float(self.currstock.getCurrent()[2]),2))
            self.current_dailyvolume['text'] = str(round(int(self.currstock.getCurrent()[6]),2)) + ' shares'
            self.current_change['text'] = self.currstock.compareStock(str(self.currentvalues[0][0]), str(self.currstock.getCurrent()[0]))
        else:
            self.usererror['text'] = '*ERROR*, try another stock'

    def changeTheme(self):
        pass

# tkinter.Tk() window
class tkui(Tk):
    def __init__(self):
        Tk.__init__(self)
        global scr_dim

        # 'tkui' window configurations:
        self.title('Stonk Scraper')                                                 # title
        self.iconphoto(False, PhotoImage(file='cashmoney.png'))                     # icon
        self.configure(background=theme[currtheme]['main']['bg'])                                          # background
        scr_dim = (self.winfo_screenwidth(), self.winfo_screenheight())
        self.geometry(f'{scr_dim[0]}x{scr_dim[1]}')                                 # screensize
        #self.geometry(f'{self.winfo_screenwidth()}x{self.winfo_screenheight()}')   # old screensize

        """
        width, height = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry('%dx%d+0+0' % (width,height))
        """

        # 'tkui's Frames:
        # In this case, we are using a frame of frames.
        mainFrame(self)

        # Add a top menubar called 'mainMenu' to 'tkui'.
        self.config(menu=mainMenu(self))

def GUI():
    global theme, currtheme, app
    theme = {
        'light':{
            'main':{'fg':'#000','bg':'#fff'},
            'active':{'fg':'#000','bg':'#fff'}
        },
        'dark':{
            'main':{'fg':'#fff','bg':'#000'},
            'active':{'fg':'#fff','bg':'#000'}
        }
    }
    currtheme = 'light'

    app = tkui()
    app.mainloop()


# This is for future possible changes, if we want to come back and implement classes for our four frames
"""
class (XX)Frame(Frame):
    def __init__(self,master=None,*args,**kwargs):
        Frame.__init__(self)
        super().__init__(master)

    def changeTheme(self):
        pass
"""
