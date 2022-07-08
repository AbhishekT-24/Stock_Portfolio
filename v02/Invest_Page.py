"""Import necessary modules"""
# Tkinter: Used to create and mould app GUI
import os
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
# API but namely to acquire current stock price values
from yahoo_fin import stock_info as si  # current stock
import yfinance as yf

# Matplotlib: Used to plot, manipulate and style plots of the stock
# information acquired from Yahoo finance.
import matplotlib
import matplotlib.pyplot as pt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

from matplotlib.figure import Figure


"""Create app default variables"""
# Creates default font used for majority of app
MAIN_FONT = "palatino"
NAV_COL = 'white'
FRA_BG = '#AF7366'
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
tickerList = []  # stores stock ticker when bough
priceList = []  # stores ticker price when bought
transList = []  # stores transaction history
timeList = []  # stores time at which transaction occured


class Stocks(tk.Frame):

    # For file saving and loading for portfolio
    global tickerList
    global priceList
    global transList
    global timeList
    global uname, pword

    def __init__(self, master, controller):
        filename=""
        try: #checks whether the tempfile is present
            f1 = open("tempfile.txt","r+") #to get the name of the user file
            filename = f1.readline()
            os.remove("tempfile.txt")
        except FileNotFoundError:
            pass

        try:
            f1 = open(filename + ".txt","r+")
            information = f1.readlines()  # creates list of file info

            # sorts through the list and formats it to show stock owned and price bought at
            for i in range(len(information) - 1):
                tickerList.append(information[i + 1].partition(" ")[0])
                priceList.append(float(information[i + 1].partition(" ")[-1].strip('\n')))

            # Notifies user they have logged before and that their info was found
            # prints the user's saved data
            print("Loaded Profile! Welcome Back!")
            print()

            print("Shares Owned Currently: ")
            for i in range(len(tickerList)):
                print(tickerList[i].upper() + "  $" + str(priceList[i]))
                print()

            # If file is not found, user has not logged in before and so
            # notifies user
        except Exception as e:
            f1 = open(filename + ".txt","w+")
            f1.close()

        style = ttk.Style()

        # Used in details function for repetition
        self.tickerNameD = 'Ticker Name in details (Placehold)'

        # Initiates navigational frame (bottom)
        tk.Frame.__init__(self, master, bg=NAV_COL)

        self.portfolio_value = 0
        # Creates actual stock page frame (create first to be on top)
        stockFrame = tk.Frame(self, width=600, height=600, bg=FRA_BG)
        stockFrame.pack()

        # Creates stock page title and nav buttons on navigational frame
        navLabel = tk.Label(self, text="Stocks", font=(MAIN_FONT, 15), bg=NAV_COL, fg=FRA_FG)
        navLabel.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Portfolio Summary",
                             command=lambda: PortfolioSummary())
        button1.pack()


        # Verfification for existing toolbar and invalid text indicator
        # to delete on re-execution if exists.
        self.tool = False
        self.open = False
        self.i = False

        # FRAME Setup
        labelTitle = tk.Label(stockFrame, text="Stocks", font=(MAIN_FONT, 20), bg=FRA_BG, fg='black')
        labelTitle.place(relx=0.5, rely=0.03, anchor='n')

        # Entry widget to enter ticker of stock to be plotted
        tickerEntry = ttk.Entry(stockFrame)
        tickerEntry.place(relx=0.18, rely=0.938, anchor='n')

        # Upon button press, access stock info and plot it (below function)
        tickerButton = ttk.Button(stockFrame, text="Confirm",
                                  command=lambda: pressPlot(tickerEntry.get()))
        tickerButton.place(relx=0.38, rely=0.938, anchor='n')

        # Creates radiobuttons to choose length of stock history
        style.configure("TRadiobutton", background=FRA_BG, selectcolor='green', font=(MAIN_FONT, 10))
        style.map("TRadiobutton", foreground=[('pressed', 'green')])

        # 5 days
        Radio_1 = ttk.Radiobutton(stockFrame, text='5dy', value=1,
                                  command=lambda: setDate(5))
        Radio_1.place(relx=0.05, rely=0.76, anchor='nw')

        # 1 month
        Radio_2 = ttk.Radiobutton(stockFrame, text='1mo', value=2,
                                  command=lambda: setDate(30))
        Radio_2.place(relx=0.15, rely=0.76, anchor='nw')

        # 6 months
        Radio_3 = ttk.Radiobutton(stockFrame, text='6mo', value=3,
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

        # -------------------------------------
        # Creates [Investing] Window + Page

        # -------------------------------------
        # Opens new sub window that allows user to invest money (from balance)
        # into defined stock at the live price
        # Money made is "simulated" as if the user invested at the open price since there is no
        # simple manner to acquire and update current stock information to find the actual gain
        def Invest(price):
            # price is price of current stock
            global tickerList, priceList
            global stockFg, lineC, arrow

            x = tickerEntry.get()  # stores current name of viewed ticker

            # destroys an existing investing window if one is open
            if self.open:
                try:
                    self.r.destroy()
                # In case client closes page first (TCLerror is not supported)
                except Exception:
                    pass

            self.open = True  # sets variable to show the invest page was opened

            # Create new investing window
            self.r = tk.Tk()
            self.r.title("Invest")
            self.r.wm_iconbitmap('favicon.ico')  # sets app icon

            # Creates actual stock page frame (create first to be ontop)
            investFrame = tk.Frame(self.r, width=400, height=450, bg=FRA_BG)
            investFrame.pack()

            # Creates middle label to show current price of shares to be bought
            # according to slider position
            Pinst = tk.Label(investFrame, text='Shares Price', bg=FRA_BG, fg='darkgreen', font=(MAIN_FONT, 8))
            Pinst.pack()
            PLabel = tk.Label(investFrame, text='$' + '0', bg=FRA_BG, fg=FRA_FG, font=(MAIN_FONT, 20))
            PLabel.pack()

            # Creates scale bar and displays its value to represent
            # amount of shares to buy
            scalevar = tk.IntVar()
            scalevar.set(0)

            # Creates shares label to display number of shares to be bought
            # according to slider
            sharesinst = tk.Label(investFrame, text='Number of Shares', bg=FRA_BG, fg='darkgreen', font=(MAIN_FONT, 8))
            sharesinst.pack()
            shares = tk.Label(investFrame, textvariable=scalevar, bg=FRA_BG, fg=FRA_FG, font=(MAIN_FONT, 20))
            shares.pack()

            # Updates PLabel
            def showP(x):
                PLabel['text'] = '$' + str(round(x, 2))

            # Creates slider to select and show number shares to buy and shows their price
            PLabelPrice = scalevar.get()

            slidStock = tk.Scale(investFrame, from_=0, to_=100, length=394, variable=scalevar, orient="horizontal",
                                 bg=FRA_BG,
                                 command=lambda PLabelPrice: showP(int(PLabelPrice) * price))
            slidStock.pack()

            # Function that will show currently owned stocks, their price bought at
            # and how much money made
            def show():
                # Creates second frame to put stock info on
                self.investFrame2 = tk.Frame(self.r, width=400, height=50, bg=FRA_BG)
                self.investFrame2.pack()



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
                    # Creates an actual frame under the name of each item in frameList
                    frame = i
                    frame = tk.Frame(self.investFrame2, relief='groove', bd=3, width=400, height=50, bg=NAV_COL)
                    frame.pack()

                    # Calls API for each share bought to display price and money made
                    x = tickerList[frameList.index(i)]

                    table = si.get_quote_table(x)
                    opnP = table['Open']
                    pclP = table['Previous Close']

                    netPrise = opnP - pclP
                    prcntrise = (netPrise / pclP) * 10

                    # Sets colour of net gain to red(loss) or green(gain)
                    if netPrise >= 0:
                        stockFg = 'green'
                        lineC = 'g'
                        arrow = '↑'
                    else:
                        stockFg = 'red'
                        lineC = 'r'
                        arrow = '↓'

                        # Creates the stock label showing the ticker, price the shares were bought at
                    sL = tk.Label(frame, text=tickerList[frameList.index(i)].upper() + " " + str(
                        priceList[frameList.index(i)]), bg="black", fg='white', font=(MAIN_FONT, 8))
                    sL.place(relx=0.2, rely=0.5, anchor='center')

                    # Creates the net stock profit label to place (different label since needs colour)
                    sP = tk.Label(frame, text='$' + str(round(priceList[frameList.index(i)] * prcntrise, 2)) + arrow,
                                  bg=NAV_COL, fg=stockFg, font=(MAIN_FONT, 8))
                    sP.place(relx=0.6, rely=0.5, anchor='center')

                    # Creates unique sell button (with unique sell() call parameter pertaining to stock it is
                    # associated with) for each button in button list
                    button = buttonList[frameList.index(i)]

                    # must use i=i to save the frame (and its index position) at the time the
                    # button was created (so we'll have buttons 0 to n and not just all n)
                    button = ttk.Button(frame, text="Sell",
                                        command=lambda i=i: sell(frameList.index(i)))  # i=i to store i at the time
                    button.place(relx=0.8, rely=0.5, anchor='center')

            # New function that will sell the shares of the ticker it is
            # associated with upon sell button press
            def sell(x):
                print(x)

                table = si.get_quote_table(tickerList[x])

                tickerList.remove(tickerList[x])
                priceList.remove(priceList[x])

                # destroys stock info frame and calls show again to update and register changes
                # (more efficient than updating the whole r window)
                self.investFrame2.destroy()
                show()

            # Calls show from r window startup to display currently owned shares
            # from load data (if any).
            show()

            # Trans function to show bought stock, amount made and update balance
            def Trans():

                global stocksDict
                global tickerList, priceList

                # stores stock and share price in 2 seperate lists to
                # save and access data

                # if the ticker is already listed, won't add a new object in the list,
                # rather just add the value to the current pricelist value at the appropriate
                # position
                if x in tickerList:
                    ticker = tickerList.index(x)  # stores the position of ticker in tickerlist
                    iPrice = priceList[ticker]  # old price

                    # updates to new price at appropriate position in pricelist
                    fPrice = round(iPrice + slidStock.get() * price, 2)
                    priceList[ticker] = fPrice

                # else creates new objects in both ticker and price lists at the end
                else:
                    tickerList.append(x)
                    priceList.append(round(slidStock.get() * price, 2))

                # same as above to update the stock info
                self.investFrame2.destroy()
                show()



            # Upon save button press, will save current balance value and ticker/price lists
            # for stock info
            def Save():
                '''Saves the portfolio of the user'''
                global uname, tickerList, priceList

                # Saves info under unique file pertaining to username and password as the name
                # (if already there will open it, else will create one)
                f = open(filename + ".txt", "r+")
                f.write('\n')  # skips to new line

                # for each item in ticker list, store it and its value beside it (each ticker
                # and its price are in the same index position in their according lists)
                for i in range(len(tickerList)):
                    f.write(tickerList[i] + " " + str(priceList[i]))
                    f.write('\n')

                f.close

            # Button to confirm purchase of shares
            iB = ttk.Button(investFrame, text="Confirm", command=lambda: Trans())
            iB.pack(pady=10)

            # Button to save current portfolio info
            saveB = ttk.Button(investFrame, text="Save Portfolio", command=lambda: Save())
            saveB.pack()
        # -------------------------------------
        # Creates [Details] Window + Page

        # -------------------------------------
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
            detailFrame = tk.Frame(self.d, width=400, height=400, bg='black')
            detailFrame.pack()

            self.tickerNameD = y.upper()
            # Places stock ticker as title label
            titleL = tk.Label(detailFrame, text=y.upper(), bg='black', fg='light green', font=(MAIN_FONT, 18))
            titleL.pack()

            # Displays the additional information from the yahoo API table
            for item in x:
                infoL = tk.Label(detailFrame, text=item + " :  " + str(x[item]), bg='black', fg='white',
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
                self.tickerPriceL.place(relx=0.41, rely=0.81, anchor='n')

                self.tickerRiseL = tk.Label(stockFrame, text=round(netPrise, 2), font=(MAIN_FONT, 10, "bold"),
                                            bg=FRA_BG, fg=stockFg)
                self.tickerRiseL.place(relx=0.05, rely=0.875, anchor='nw')

                self.tickerprcntL = tk.Label(stockFrame, text='(' + str(round(prcntrise, 2)) + '%) ' + arrow,
                                             font=(MAIN_FONT, 10, "bold"), bg=FRA_BG, fg=stockFg)
                self.tickerprcntL.place(relx=0.13, rely=0.875, anchor='nw')

                self.tickerName = x.upper()
                self.tickerTitleL = tk.Label(stockFrame, text=self.tickerName, font=(MAIN_FONT, 25), bg=FRA_BG,
                                             fg='white')
                self.tickerTitleL.place(relx=0.05, rely=0.8, anchor='nw')
                stockPlot(x, livP, table, lineC)

            # Plots actual stock graph from panda stock database (and creates
            # investing button - passes live price as y) and (creates details tab - passes table as z)
            # linC is for plot colour
            def stockPlot(x, livy, tablez, linC):

                # Updates label theme incase of settings change
                self.tickerPriceL.configure(bg=FRA_BG, fg=FRA_FG)
                self.tickerRiseL.configure(bg=FRA_BG)
                self.tickerprcntL.configure(bg=FRA_BG)
                self.tickerTitleL.configure(bg=FRA_BG, fg=FRA_FG)

                # Plotting the graph of given stock (Ticker)
                pt.style.use("ggplot")
                start = dt.datetime(year1, month1, date1)  # Start date, xi on plot
                end = dt.datetime(year2, month2, date2)  # End date as today,xf on plot

                # Creates button which opens window for allowing investing
                self.investB = ttk.Button(stockFrame, text="Invest",
                                          command=lambda: Invest(livy))
                self.investB.place(relx=0.75, rely=0.938, anchor='n')

                # Creates button which opens window for displaying additional information
                self.infoB = ttk.Button(stockFrame, text="Stock Fundamentals",
                                        command=lambda: Details(tablez, x))
                self.infoB.place(relx=0.75, rely=0.878, anchor='n')

                # Displays user info as logged in (must be in function and not load up, since load up runs at startup of app
                # before a username has been entered)
                logName = tk.Label(stockFrame, text="Logged in!", font=(MAIN_FONT, 15), bg=FRA_BG, fg='#E8E8E8')
                logName.place(relx=0.75, rely=0.77, anchor='n')

                # Acquires data of given stock (ticker) from
                # Yahoo Finance API
                df = web.get_data_yahoo(str(x), start, end)

                # Plots given data, with identifier "Adj Close" on axes
                df["Adj Close"].plot()

                # Prints title for Stock graph
                print(x.upper(), "stock price from " + str(start) + " to " + str(end))

                # Graph styling on size
                f = Figure(figsize=(6, 4), dpi=100)
                a = f.add_subplot(111)

                # Makes plot visible on select frame
                f.patch.set_facecolor(FRA_BG)  # sets AXES colour
                a.patch.set_facecolor('xkcd:white')  # sets actual PLOT colour
                a.set_title(
                    str(x.upper()) + " stock price from " + str(year1) + " " + str(month1) + " " + str(date1) + " \nto "
                    + str(year2) + " " + str(month2) + " " + str(date2), color=FRA_FG)
                a.set_xlabel('Date', fontsize=12)  # sets x axis label to "date"
                a.set_ylabel('Price($)', fontsize=12)  # sets y axis label to "price"
                a.xaxis.label.set_color('black')
                a.yaxis.label.set_color('black')
                a.tick_params(colors='black', which='both')
                a.plot(df["Adj Close"], linC)

                # Allocates canvas area to display graph (embeds matplot graph)
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

                # destroys invest frame upon changing stocks (avoid confusion)
                if self.open:
                    try:
                        self.r.destroy()
                        # self.d.destroy() #if want to destroy details page, kept for comparing
                        self.open = False
                    # In case client closes page first (TCLerror is not supported)
                    except Exception:
                        pass

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

                else:
                    print()
                    print('Loading... Fetching stock data...')
                    acquireData(x)

                # Exception handling in case that invalid ticker is entered
            except ValueError:
                # Creates error instructions label to display
                if self.i == False:
                    self.LabelI = tk.Label(stockFrame, text="Invalid ticker or viewing date, try again - must be NYSE.",
                                           bg=FRA_BG, fg="red", font=(MAIN_FONT, 7, 'bold'))
                    self.LabelI.place(relx=0.3, rely=0.91, anchor="n")
                    self.i = True  # shows error was shown

                # In case of error, destroy buttons since no valid ticker entered
                if self.tool:
                    self.infoB.destroy()
                    self.investB.destroy()
                print("Invalid name or viewing date, try again.")
        # -------------------------------------
        # Creates [Portfolio Summary] Window + Page
        # -------------------------------------

        def PortfolioSummary():
            # destroys an existing investing window if one is open

            global tickerList
            global priceList
            if self.open:
                try:
                    r.destroy()
                # In case client closes page first (TCLerror is not supported)
                except Exception:
                    pass

            self.open = True

            portfolio_value=0
            print(portfolio_value)
            # Create new investing window
            r = tk.Tk()
            r.title("Portfolio Summary")
            r.wm_iconbitmap('favicon.ico')  # sets app icon
            frameList=[]
            # Creates the required number of variable names for frames and buttons
            print(len(tickerList))
            for i in range(len(tickerList)):
                frameList.append('stockFrame' + str(i))
            print("Checkpoint2")
            # Creates and displays the stock info
            for i in frameList:
                portfolio_value += priceList[frameList.index(i)]
            print("Checkpoint3")
            # Creates actual stock page frame (create first to be ontop)
            PortfolioFrame = tk.Frame(r, width=500, height=500, bg=FRA_BG)
            PortfolioFrame.pack()
            print("Checkpoint4")
            # Creates top label to show total value of the portfolio
            Vinst = tk.Label(PortfolioFrame, text='Total Portfolio value', bg=FRA_BG, fg='darkgreen',
                             font=(MAIN_FONT, 10))
            Vinst.pack()
            VLabel = tk.Label(PortfolioFrame, text='$' + str(portfolio_value), bg=FRA_BG, fg=FRA_FG,
                              font=(MAIN_FONT, 20, "bold"))
            VLabel.pack()
            print("Checkpoint5")
            # Creates second frame to put stock info on
            self.investFrame2 = tk.Frame(r, width=450, height=500, bg=FRA_BG)
            self.investFrame2.pack()
            print("Checkpoint6")

            # Creates and displays the stock info
            for i in frameList:
                # Creates an actual frame under the name of each item in frameList
                frame = i
                frame = tk.Frame(self.investFrame2, relief='groove', bd=3, width=450, height=50,
                                 bg="black")  # relief is border
                frame.pack()

                # Calls API for each share bought to display price and money made
                x = tickerList[frameList.index(i)]
                ticker = yf.Ticker(x)
                name = ticker.info["longName"]
                table = si.get_quote_table(x)
                opnP = table['Open']
                pclP = table['Previous Close']

                netPrise = opnP - pclP  # net price rise for the day
                prcntrise = (netPrise / pclP) * 10

                # Sets colour of net gain to red(loss)+arrow down or green(gain)+arrow up
                if netPrise >= 0:
                    stockFg = 'green'
                    arrow = '↑'
                else:
                    stockFg = 'red'
                    arrow = '↓'

                # Creates the stock label showing the ticker, price the shares were bought at
                sL = tk.Label(frame,text=name.upper(), bg="black", fg='white', font=(MAIN_FONT, 12))
                sL.place(relx=0.2, rely=0.5, anchor='center')

                # Creates the net stock profit label to place (different label since needs colour)
                sP = tk.Label(frame, text='$' + str(round(priceList[frameList.index(i)], 2)) + arrow, bg="black", fg=stockFg, font=(MAIN_FONT, 12))
                sP.place(relx=0.6, rely=0.5, anchor='center')
