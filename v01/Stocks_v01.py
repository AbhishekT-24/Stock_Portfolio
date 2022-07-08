# Tkinter: Used to create and mould the GUI
import tkinter as tk
from tkinter import ttk

# Datetime: Used to access and format today's and other dates
# to be used as x points for stock plots (domain)
import datetime as dt
from datetime import timedelta

# Pandas: Used to access stock information Yahoo finance API
# and to manipulate it for use in matplotlib graphing

import pandas_datareader as web


# Yahoo Finance: Also used to access stock info from Yahoo finance

from yahoo_fin import stock_info as si  # current stock

# Matplotlib: Used to plot, manipulate and style plots of the stock

import matplotlib
import matplotlib.pyplot as pt

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

# Implement the default mpl key bindings and toolbar support (for plot
# manipulation)

from matplotlib.figure import Figure


# Creates default font used for majority of app
MAIN_FONT = "times new roman"
NAV_COL = '#141d26'
FRA_BG = '#99AAB5'
FRA_FG = 'black'

# Tracks colour change
colC = False

# New default font size for stock plots
matplotlib.rc('xtick', labelsize=6)
matplotlib.rc('ytick', labelsize=6)

# Creates default for variables to be
# used throughout the program

stockFg = 'green'
lineC = 'green'
arrow = 'green'
livP = 'Stocks Price (placehold)'
table = 'Stock Table (placehold)'

# For file saving and loading for portfolio
tickerList = []  # stores stock ticker when bought
priceList = []  # stores ticker price when bought
transList = []  # stores transaction history
timeList = []  # stores time at which transaction occured


class Stocks(tk.Frame):

    def __init__(self, master, controller):
        style = ttk.Style()

        # Used in details function for repitition
        self.tickerNameD = 'Ticker Name in details (Placehold)'

        # Initiates navigational frame (bottom)
        tk.Frame.__init__(self, master, bg=NAV_COL)

        # Creates actual stock page frame (create first to be ontop)
        stockFrame = tk.Frame(self, width=500, height=600, bg=FRA_BG)
        stockFrame.pack()

        # to delete on reexecution if exists.
        self.tool = False
        self.open = False
        self.i = False

        # FRAME Setup

        labelTitle = tk.Label(stockFrame, text="Welcome to Winterfell!", font=(MAIN_FONT, 20, 'bold'), bg=FRA_BG, fg='black',)
        labelTitle.place(relx=0.5, rely=0.03, anchor='n')

        # Entry widget to enter ticker of stock to be plotted
        tickerEntry = ttk.Entry(stockFrame)
        tickerEntry.place(relx=0.18, rely=0.90, anchor='n')

        # Upon button press, access stock info and plot it (below function)
        tickerButton = ttk.Button(stockFrame, text="Confirm",
                                  command=lambda: pressPlot(tickerEntry.get()))
        tickerButton.place(relx=0.38, rely=0.90, anchor='n')

        # Creates radiobuttons to choose length of stock history
        style.configure("TRadiobutton", background=FRA_BG, selectcolor='green', font=(MAIN_FONT, 10))
        style.map("TRadiobutton", foreground=[('pressed', 'green')])

        # 5 days
        Radio_1 = ttk.Radiobutton(stockFrame, text='5d', value=1,
                                  command=lambda: setDate(5))
        Radio_1.place(relx=0.05, rely=0.76, anchor='nw')

        # 1 month
        Radio_2 = ttk.Radiobutton(stockFrame, text='1m', value=2,
                                  command=lambda: setDate(30))
        Radio_2.place(relx=0.15, rely=0.76, anchor='nw')

        # 6 months
        Radio_3 = ttk.Radiobutton(stockFrame, text='6m', value=3,
                                  command=lambda: setDate(180))
        Radio_3.place(relx=0.25, rely=0.76, anchor='nw')

        # 1 year
        Radio_4 = ttk.Radiobutton(stockFrame, text='1yr', value=4,
                                  command=lambda: setDate(365))
        Radio_4.place(relx=0.35, rely=0.76, anchor='nw')

        # 5 years
        Radio_5 = ttk.Radiobutton(stockFrame, text='5yr', value=5,
                                  command=lambda: setDate(1826))
        Radio_5.place(relx=0.45, rely=0.76, anchor='nw')

        # Refreshes the frame (for background change)
        def refresh():
            global colC
            if colC:
                stockFrame.configure(bg=FRA_BG)
                labelTitle.configure(bg=FRA_BG, fg='white')
                style.configure("TRadiobutton", background=FRA_BG, foreground='white')

        # Upon call from a radio button, sets various variables to match current date
        # and previous date according to inputed time delta
        def setDate(x):
            # These globals make the variables available to the entrie script
            # usable by any definition that follows
            global year2
            global month2
            global date2
            global year1
            global month1
            global date1

            # -Current Date-
            # uses datetime to create string of current date (x2)
            now = dt.datetime.now()
            current = str(now)
            # Sorts through string to store year, month and date which is needed
            # to plot the day and acquire stock data (for pandas and numpy)
            year2 = int(current[0:4])
            month2 = int(current[5:7])
            date2 = int(current[8:10])
            currentList = [year2, month2, date2]

            # Uses timedelta to find the prior date (x1)
            before = dt.datetime.now() - timedelta(days=x)

            # -Prior Date-
            # Creates prior date string which is also sorted to find
            # year, month and date for same reasons
            prior = str(before)
            year1 = int(prior[0:4])
            month1 = int(prior[5:7])
            date1 = int(prior[8:10])
            priorList = [year1, month1, date1]

            # Prints both dates in shell (mainly for debug)
            print()
            print('Start Date: ', year1, month1, date1)
            print('End Date: ', year2, month2, date2)




            def show():

                # Creates 2 lists to hold required frames and buttons for
                # each stock info frame (each ticker will have one - according to ticker and price lists)
                frameList = []
                buttonList = []

                # Creates the required number of variable names for frames and buttons
                for i in range(len(tickerList)):
                    frameList.append('stockFrame' + str(i))
                    buttonList.append('stockB' + str(i))

                # Creates and displays the stock info
                for i in frameList:

                    # Calls API for each share bought to display price and money made
                    x = tickerList[frameList.index(i)]

                    table = si.get_quote_table(x)
                    opnP = table['Open']
                    pclP = table['Previous Close']

                    netPrise = opnP - pclP
                    prcntrise = (netPrise / pclP) * 100

                    # Sets colour of net gain to red(loss) or green(gain)
                    if netPrise >= 0:
                        stockFg = 'green'
                        lineC = 'g'
                        arrow = '↑'
                    else:
                        stockFg = 'red'
                        lineC = 'r'
                        arrow = '↓'


        # Displays further details on selected stock(x-table, y-stock ticker)
        def Details(x, y):
            # Checks if this is a repeated tab, in that case, destroy the repeat window.
            if self.tickerNameD == y.upper():
                try:
                    self.d.destroy()
                # In case client closes page first (TCLerror is not supported)
                except Exception:
                    pass

            # Creates new window with the "Ticker - More Info" Name
            self.d = tk.Tk()
            self.d.title("Stock Details")
            self.d.wm_iconbitmap('favicon.ico')  # sets app icon

            # Creates details frame
            detailFrame = tk.Frame(self.d, width=400, height=400, bg=NAV_COL)
            detailFrame.pack()

            self.tickerNameD = y.upper()
            # Places stock ticker as title label
            titleL = tk.Label(detailFrame, text=y.upper(), bg=NAV_COL, fg='light green', font=(MAIN_FONT, 15))
            titleL.pack()

            # Displays the additional information from the yahoo API table
            for item in x:
                infoL = tk.Label(detailFrame, text=item + " :  " + str(x[item]), bg=NAV_COL, fg='white',
                                 font=(MAIN_FONT, 10), anchor='w')
                infoL.pack(pady=3, fill='x')

        # ---------------------------------
        # Stock Graphing onto matplot graph

        # ---------------------------------
        def pressPlot(x):
            global stockFg, lineC, arrow

            # Updates UI theme
            refresh()

            # Calls yahoo finance API (slow) to acquire current live stock data
            def acquireData(x):
                global livP, table, lineC
                # Getting stock open price, live price and %netrise
                livP = si.get_live_price(x)  # not very live
                table = si.get_quote_table(x)
                opnP = table['Open']
                pclP = table['Previous Close']

                netPrise = opnP - pclP
                prcntrise = (netPrise / pclP) * 100

                print("Open {0}, Previous Close {1}, Current {2}".format(opnP, pclP, round(livP, 2)))

                # Sets colour of net gain to red(loss) or green(gain)
                if netPrise >= 0:
                    stockFg = 'green'
                    lineC = 'g'
                    arrow = '↑'
                else:
                    stockFg = 'red'
                    lineC = 'r'
                    arrow = '↓'

                    # destroys any existing toolbars or labels if they already existed
                # prior to a new plot
                if self.tool:
                    self.tickerPriceL.destroy()
                    self.tickerRiseL.destroy()
                    self.tickerprcntL.destroy()
                    self.tickerTitleL.destroy()

                # Plots ticker and ticker Price Live
                self.tickerPrice = round(livP, 2)
                self.tickerPriceL = tk.Label(stockFrame, text=str(self.tickerPrice) + ' USD', font=(MAIN_FONT, 15),
                                             bg=FRA_BG, fg='white')
                self.tickerPriceL.place(relx=0.41, rely=0.8, anchor='n')

                self.tickerRiseL = tk.Label(stockFrame, text=round(netPrise, 2), font=(MAIN_FONT, 10, "bold"),
                                            bg=FRA_BG, fg=stockFg)
                self.tickerRiseL.place(relx=0.05, rely=0.85, anchor='nw')

                self.tickerprcntL = tk.Label(stockFrame, text='(' + str(round(prcntrise, 2)) + '%) ' + arrow,
                                             font=(MAIN_FONT, 10, "bold"), bg=FRA_BG, fg=stockFg)
                self.tickerprcntL.place(relx=0.41, rely=0.85, anchor='nw')

                self.tickerName = x.upper()
                self.tickerTitleL = tk.Label(stockFrame, text=self.tickerName, font=(MAIN_FONT, 25), bg=FRA_BG,
                                             fg='white')
                self.tickerTitleL.place(relx=0.05, rely=0.8, anchor='nw')
                stockPlot(x, livP, table, lineC)

            # Plots actual stock graph from panda stock database (and creates

            # linC is for plot colour
            def stockPlot(x, livy, tablez, linC):

                # Plotting the graph of given stock (Ticker)
                pt.style.use("ggplot")
                start = dt.datetime(year1, month1, date1)  # Start date, xi on plot
                end = dt.datetime(year2, month2, date2)  # End date as today,xf on plot

                # Creates button which opens window for displaying additional information
                self.infoB = ttk.Button(stockFrame, text="Stock Fundamentals",
                                        command=lambda: Details(tablez, x))
                self.infoB.place(relx=0.75, rely=0.878, anchor='n')

                # Displays user info as logged in (must be in function and not load up, since load up runs at startup of app
                # before a username has been entered)
                logName = tk.Label(stockFrame, font=(MAIN_FONT, 15), bg=FRA_BG,
                                   fg='#E8E8E8')
                logName.place(relx=0.75, rely=0.77, anchor='n')

                # Acquires data of given stock (ticker) from
                # Yahoo Finance API
                df = web.get_data_yahoo(str(x), start, end)

                # Plots given data, with identifier "Adj Close" on axes
                df["Adj Close"].plot()

                # Prints title for Stock graph
                print(x.upper(), "stock price from " + str(start) + " to " + str(end))

                # Graph styling on size
                f = Figure(figsize=(5, 4), dpi=100)
                a = f.add_subplot(111)

                # Makes plot visible on select frame
                f.patch.set_facecolor(FRA_BG)  # sets AXES colour
                a.patch.set_facecolor('xkcd:grey')  # sets actual PLOT colour
                a.set_title(
                    str(x.upper()) + " stock price from " + str(year1) + " " + str(month1) + " " + str(date1) + " \nto "
                    + str(year2) + " " + str(month2) + " " + str(date2), color=FRA_FG)
                a.set_xlabel('Date')  # sets x axis label to "date"
                a.set_ylabel('Price($)')  # sets y axis label to "price"
                a.plot(df["Adj Close"], linC)

                # Allocates canvas area to display graph (embeds mtplot graph
                # using FigureCanvasTkAgg function
                canvas = FigureCanvasTkAgg(f, stockFrame)
                canvas.draw()
                canvas.get_tk_widget().place(relx=0.5, rely=0.9, anchor='n')
                canvas._tkcanvas.place(relx=0.5, rely=0.1, anchor="n")

                # destroys any existing toolbars
                if self.tool:
                    self.toolbar.destroy()
                    self.tool = False

                # Creates toolbar to manipulate stock graph
                self.toolbar = NavigationToolbar2Tk(canvas, self)
                self.toolbar.configure(bg=NAV_COL)
                self.toolbar.update()
                self.tool = True  # holds if a previous stock was viewed



                # destroys warning label upon viewing valid stock.
                if self.i:
                    self.LabelI.destroy()
                    self.i = False

            # Code starts here, upon plotting - checks if the entry is just a time change, in that
            # case don't acquire API data, just plot again. Else, acquire data then plot.
            try:
                if self.tool and x.upper() == self.tickerName:
                    global livP, table, lineC
                    print()
                    print('Loading... Plotting...')
                    stockPlot(x, livP, table, lineC)
                    self.LabelI.destroy()

                else:
                    print()
                    print('Loading... Fetching stock data...')
                    acquireData(x)
                    self.LabelI.destroy()


                # Exception handling in case that invalid ticker is entered
            except AssertionError:
                # Creates error instructions label to display
                if self.i == False:
                    self.LabelI = tk.Label(stockFrame, text="Invalid ticker or viewing date, ensure NYSE stock code.",
                                           bg=FRA_BG, fg="red", font=(MAIN_FONT, 14, 'bold'))
                    self.LabelI.place(relx=0.5, rely=0.95, anchor="n")
                    self.i = True  # shows error was shown

