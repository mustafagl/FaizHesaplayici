import tkinter as tk
from tkinter import ttk
import pandas as pd
import os.path
from datetime import datetime,timedelta
import os
from sys import platform
from tkcalendar import DateEntry
from tkcalendar import Calendar
import json
from functools import partial
from dateutil.relativedelta import relativedelta
import pages 

class Application:
    def __init__(self,master):
        self.master = master
        self.master.title("Faiz Hesaplama Uygulaması")
        style = ttk.Style()
        style.theme_use('default')
        self.master.geometry("{0}x{1}+0+0".format(self.master.winfo_screenwidth(), self.master.winfo_screenheight()))
        
        page = pages.Pages(self.master)
        page.create_homepage()   


def main():
    root = tk.Tk()
    app = Application(root)
    root.mainloop()

if __name__ == "__main__":
    main()