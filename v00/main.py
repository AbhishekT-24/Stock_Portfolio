# Tkinter: Used to create the main User Interface
import tkinter as tk

#Importing Stocks function from file Stocks_V00.py

from Stocks_v00 import Stocks


# Main function that is used to run the application

class Winterfell(tk.Tk):
    '''main function that controls all windows'''
    def __init__(self):
        # Initializes functions
        tk.Tk.__init__(self)
        # We create constant container to house navigation buttons
        container = tk.Frame(self)
        container.pack()
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)  # places the container on the bottom

        # Dictionary that will hold all pages (classes) - this shall be useful when we have more windows
        self.frames = {}
        frame = Stocks(container, self)
        self.frames[Stocks] = frame
        frame.grid(row=0, column=0, sticky="nsew")


#Runs the app, sets main title, logo and keeps window open

app = Winterfell()

app.wm_title('Winterfell')  # sets app window title
app.mainloop()

