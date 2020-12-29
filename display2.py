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
        print('Ur mom gay!')

    # Call the standard python quit() function to quit program.
    def quit(self):
        quit()

class nwFrame(Frame):
    def __init__(self,master=None):
        Frame.__init__(self)
        super().__init__(master)

        #
        self.userstocksymbol = 'AAPL'
        self.currstock = Stock(0,self.userstocksymbol)
        #fig = Figure(figsize=(19.2, 10.8), dpi=100)
        fig = Figure(figsize=(scr_dim[0]/200, scr_dim[1]/200), dpi=100)
        #fig.patch.set_facecolor('#000')
        fig.set_facecolor(theme[currtheme]['main']['bg'])
        mpl.rcParams['axes.facecolor'] = theme[currtheme]['main']['bg']
        #print(str(self.winfo_screenwidth()) + ' x ' + str(self.winfo_screenheight()))
        closingprices = [round(float(i[4]),2) for i in self.currstock.getHistory()]
        dates = [datetime(int(i[0][0:4]),int(i[0][5:7]), int(i[0][8:10])) for i in self.currstock.getHistory()]
        fig.add_subplot(111).plot_date(dates,closingprices, '-', linewidth = 1)
        canvas = FigureCanvasTkAgg(fig, master = master)
        canvas.get_tk_widget().grid(row = 0, column = 0)

    def changeTheme(self):
        pass

class neFrame(Frame):
    def __init__(self,master=None):
        Frame.__init__(self)
        super().__init__(master)

        #
        self.dspl_main = Label(
            text='Hello World!'
        )
        self.dspl_main.grid(row=0,column=1)
    def changeTheme(self):
        pass

class swFrame(Frame):
    def __init__(self,master=None):
        Frame.__init__(self)
        super().__init__(master)

        #
        self.dspl_main = Label(
            text='Hello World!'
        )
        self.dspl_main.grid(row=1,column=0)
    def changeTheme(self):
        pass

class seFrame(Frame):
    def __init__(self,master=None):
        Frame.__init__(self)
        super().__init__(master)

        #
        self.dspl_main = Label(
            text='Hello World!'
        )
        self.dspl_main.grid(row=1,column=1)
    def changeTheme(self):
        pass

# main frame
class mainFrame(Frame):
    def __init__(self,master=None):
        Frame.__init__(self,master)
        super().__init__(master)
        master.configure(borderwidth=1)
        master.geometry(f'{scr_dim[0]}x{scr_dim[1]}')

        #
        self.grid()
        [self.master.rowconfigure(i,weight=1) for i in range(4)]
        [self.master.columnconfigure(i,weight=1) for i in range(4)]

        self.nwFrame = nwFrame(master)
        self.neFrame = neFrame(master)
        self.swFrame = swFrame(master)
        self.seFrame = seFrame(master)

        #self.nwFrame.grid(row=0,column=0,rowspan=1,colspan=1,sticky='nsew')

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

    def changeTheme():
        pass

def GUI():
    global theme, currtheme
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
    currtheme = 'dark'

    app = tkui()
    app.mainloop()


"""
app = tkui()
app.mainloop()
"""
