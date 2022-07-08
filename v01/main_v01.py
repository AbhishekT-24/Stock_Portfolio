# Tkinter: Used to create and mould the GUI
import tkinter as tk

from Stocks_v01 import Stocks

# Main function that is used to display pages
class Winterfell(tk.Tk):

    def __init__(self):
        # Initializes functions
        tk.Tk.__init__(self)
        # Creates constant container to house navigation buttons
        container = tk.Frame(self)
        container.pack()
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)  # places the container on the bottom

        # Dictionary that will hold all pages (classes)
        self.frames = {}

        # Select page to be displayed
        frame = Stocks(container, self)
        self.frames[Stocks] = frame
        frame.grid(row=0, column=0, sticky="nsew")

# Runs the app, sets main title, logo and keeps window open

app = Winterfell()

app.wm_title('Winterfell')  # sets app window title
app.mainloop()
