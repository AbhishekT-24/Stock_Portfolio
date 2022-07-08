# Tkinter: Used to create the main User Interface
import tkinter as tk
from tkinter import ttk

# Yahoo Finance: Also used to access stock info from Yahoo finance
# API but namely to acquire current stock price values
from yahoo_fin import stock_info as si  # current stock

#Creating some variables for defining fonts and various colors used in the program

MAIN_FONT = "times new roman"
NAV_COL = '#141d26'
FRA_BG = '#a9c5cc' #We have used a whitish blue for the background
FRA_FG = 'black'

# Tracks colour change
colC = False

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
    '''Stocks class sets up the mainframe to show stock details and information'''
    def __init__(self, master, controller):
        style = ttk.Style()

        # Used in details function for repeatition
        self.tickerNameD = 'Ticker Name in details (Placehold)'

        # Initiates navigational frame (bottom)
        tk.Frame.__init__(self, master, bg=NAV_COL)

        # Creates actual stock page frame (create first to be on top)
        stockFrame = tk.Frame(self, width=900, height=1100, bg=FRA_BG)
        stockFrame.pack()

        # to delete on re-execution if exists.
        self.tool = False
        self.open = False
        self.i = False

        # FRAME Setup
        labelWelcome = tk.Label(stockFrame, text="Welcome to Winterfell!",
                              font=(MAIN_FONT, 30), bg=FRA_BG, fg='black')
        labelWelcome.place(relx=0.5, rely=0.10, anchor='n')

        labelTitle = tk.Label(stockFrame, text="Enter the NYSE stock code to see current price \n and day's movement", font=(MAIN_FONT, 30), bg=FRA_BG, fg='black')
        labelTitle.place(relx=0.5, rely=0.20, anchor='n')

        # Entry widget to enter ticker of stock to be plotted
        tickerEntry = ttk.Entry(stockFrame)
        tickerEntry.place(relx=0.50, rely=0.55, anchor='n')

        # Upon button press, access stock info

        tickerButton = ttk.Button(stockFrame, text="Confirm",
                                  command=lambda: Stock_Details(tickerEntry.get()))
        tickerButton.place(relx=0.50, rely=0.60, anchor='n')

        def Stock_Details(x):
            '''To get info about stock_details. x is the NYSE code of the stock'''
            # Calls yahoo finance API to acquire real time stock data
            def acquireData(x):
                global livP, table, lineC

                # Getting stock open price, live price and %netrise
                livP = si.get_live_price(x)
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
                    arrow = ''
                else:
                    stockFg = 'red'
                    lineC = 'r'
                    arrow = ''

                # destroys any existing toolbars or labels if they already existed
                if self.tool:
                    self.tickerPriceL.destroy()
                    self.tickerRiseL.destroy()
                    self.tickerprcntL.destroy()
                    self.tickerTitleL.destroy()

                # Displays ticker and ticker Price Live
                self.tickerPrice = round(livP, 2)
                self.tickerPriceL = tk.Label(stockFrame, text=str(self.tickerPrice) + ' USD', font=(MAIN_FONT, 25),
                                             bg=FRA_BG, fg='white')
                self.tickerPriceL.place(relx=0.65, rely=0.40, anchor='n')

                self.tickerRiseL = tk.Label(stockFrame, text=round(netPrise, 2), font=(MAIN_FONT, 20, "bold"),
                                            bg=FRA_BG, fg=stockFg)
                self.tickerRiseL.place(relx=0.65, rely=0.45, anchor='nw')

                self.tickerprcntL = tk.Label(stockFrame, text='(' + str(round(prcntrise, 2)) + '%) ' + arrow,
                                             font=(MAIN_FONT, 20, "bold"), bg=FRA_BG, fg=stockFg)
                self.tickerprcntL.place(relx=0.25, rely=0.45, anchor='nw')

                self.tickerName = x.upper()
                self.tickerTitleL = tk.Label(stockFrame, text=self.tickerName, font=(MAIN_FONT, 25), bg=FRA_BG,
                                             fg='white')
                self.tickerTitleL.place(relx=0.25, rely=0.40, anchor='nw')
                self.tool = True #this line ensures that there doesnt exist an overlap of text from previous entry by user
                Fundamentals(x, livP, table, lineC)

            def Fundamentals(x, livy, tablez, linC):
                '''sets up a new frame to display the fundamental information about different stocks'''
                # Creates button which opens window for displaying additional information
                self.infoB = ttk.Button(stockFrame, text="Stock Fundamentals")
                self.infoB.place(relx=0.75, rely=0.878, anchor='n')

            try:
                print()
                print('Loading... Fetching stock data...')
                acquireData(x)
                try:
                    self.LabelI.destroy() #destroys the existing error label (if any)
                except:
                    pass

                # Exception handling in case that invalid ticker is entered
            except AssertionError:
                # Creates error instructions label to display
                if self.i == False:
                    self.LabelI = tk.Label(stockFrame, text="Invalid ticker entered -  must be NYSE stock code.",
                                           bg=FRA_BG, fg="red", font=(MAIN_FONT, 20, 'bold'))
                    self.LabelI.place(relx=0.5, rely=0.70, anchor="n")
                    self.i = True  # shows error was shown
