# This was created by Danila Popel and Nikita Popel. This project was originally created on December 24th, 2020.

# local packages
from scraper import *
from display import *

# python3 standard libraries
import urllib.request, os, platform, time, csv, requests
from datetime import datetime, timedelta, date
from tkinter import *
from tkinter.ttk import *


# pip packages
from bs4 import BeautifulSoup
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)

if __name__ == '__main__':
    GUI()
