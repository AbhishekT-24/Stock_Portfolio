#Winterfell

Winterfell is useful to keep track of a user's Stock Portfolio.\
Winterfell uses Yahoo Finance API to keep a track of current stock portfolio. \
The application will give you useful information, like the current price of a stock, basic trends to see how a company has been performing in a given time period. A user also has the ability to store their entire portfolio and manage the portfolio's value at any point of time. The user has the ability to sell their shares of a particular company at any time, and the application would modify their portfolio accordingly.\

##Requirements:
1. pandas_datareader
2. yfinance
3. numpy
4. matplotlib
5. os
6. tkinter

##Login:
At login, a first time user has to create a username and password, with which they are able to log in to the system. The user will be asked to enter their details again to log into the platform.

##Graph Visualisation

<img height="250" src="../../../../../../../var/folders/0c/fgrnvq111ws10lt92j11hlfh0000gn/T/TemporaryItems/NSIRD_screencaptureui_2kdjX3/Screenshot 2021-12-17 at 18.22.41.png" width="300"/>\
An trend in the application looks like the above. As can be seen, the y axis specifies the prices of the stock, and the x axis shows the dates. This graph is for a 5 day period.\
The trend line in the graph changes color based on the current value of the stock in NYSE.


##Detailed Page
After successful login, a user's file is created in the computer. All the information about their portfolio is then stored into the file.\
The user can now search for different stocks in the application and see the trends for the stock price for a defined time period. By clicking the Detailed Button, a user can access important information about the stocks, like:\
1. Market Cap
2. PE Ratio
3. Ask
4. Ex-dividend rate

The following is the detailed window for apple stock:

<img height="200" src="../../../../../../../var/folders/0c/fgrnvq111ws10lt92j11hlfh0000gn/T/TemporaryItems/NSIRD_screencaptureui_0GjhAo/Screenshot 2021-12-17 at 17.41.36.png" width="150" title="Detailed Window"/>\

##Invest Page
The invest window in the application gives the user the ability to store a company's share. At the bottom of the page, the user also has the option to sell/dump a company's share.

<img height="150" src="../../../../../../../var/folders/0c/fgrnvq111ws10lt92j11hlfh0000gn/T/TemporaryItems/NSIRD_screencaptureui_WdiQ54/Screenshot 2021-12-17 at 18.30.47.png" width="200"/>\

##Portfolio Summary
The portfolio summary is the window which gives a user the summary of their entire portfolio. The window lists all the shares the user is holding at any moment.\
The window looks like the following:

<img height="150" src="../../../../../../../var/folders/0c/fgrnvq111ws10lt92j11hlfh0000gn/T/TemporaryItems/NSIRD_screencaptureui_RvY2mL/Screenshot 2021-12-17 at 18.48.42.png" width="250"/>

The user can see the total portfolio value, the stocks they own and the value they invested in the current stock. The color of the stock shows whether the user is either in profit or loss.
