# This was created by Danila Popel and Nikita Popel. This project was originally created on December 23rd, 2020.

from bs4 import BeautifulSoup
import urllib.request, os, platform, time, csv, requests
from datetime import datetime, timedelta
from scraper import *
#import tkinter
from tkinter import *

class App(Frame):
    def __init__(self, Frame):
        self.window = Tk()
        self.window.title("Stonk Scraper")
        self.stockname = Label(window, text = "Welcome to the Stonk Scraper")
        self.stockname.grid(column = 0, row =0)


    def setStockname(self, userinput):
        self.stockname = userinput
