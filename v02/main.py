# Tkinter: Used to create and mould app GUI
import tkinter as tk
import matplotlib
import Invest_Page, Login_page

"""Create app default variables"""
# Creates default font used for majority of app
MAIN_FONT = "palatino"
NAV_COL = 'white'
FRA_BG = '#AF7366'
FRA_FG = 'black'

# Tracks colour change
colC = False

# Creates file that will store login credentials upon
# signup to be referenced in login
creds = 'tempfile.temp'

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


class Winterfell(tk.Tk):
    global creds
    def __init__(self):
        # Initializes functions
        tk.Tk.__init__(self)
        # Creates constant container to house navigation buttons
        container = tk.Frame(self)
        container.pack()
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1) # places the container on the bottom

        # Dictionary that will hold all pages (classes)
        self.frames = {}

        # For loop that will select pages to be displayed
        # upon button click event
        for F in (Login_page.LoginPage, Invest_Page.Stocks):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(Login_page.LoginPage)

    # Selected frame is raised above other frames (serves as navigation
    # between pages)
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


app = Winterfell()
app.wm_title('WinterFell')  # sets app window title
app.mainloop()
