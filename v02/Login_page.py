
"""Import necessary modules"""
# Tkinter: Used to create and mould app GUI
import tkinter as tk
from tkinter import ttk

# OS: Used to create and access files (for login information)
import os
import Invest_Page

import matplotlib

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
uname = ""
pword = ""

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


class LoginPage(tk.Frame):
    global uname, pword

    def __init__(self, master, controller):
        # Intiates the navigational frame (just placeholder until login complete)
        tk.Frame.__init__(self, master, bg=NAV_COL)
        style = ttk.Style() # Allows further styling of widgets using ttk
        self.controller=controller

        # Signup definition upon start up - creates signup pages that
        # allows user to create an account
        def Signup():
            # Creates and places main background frame to place everything on
            self.homeFrame = tk.Frame(self, width=600, height=600, bg=FRA_BG)
            self.homeFrame.pack()

            # Creates Finenhance title on homeframe
            labelTitleFIN = tk.Label(self.homeFrame, text="WINTERFELL", font=(MAIN_FONT, 35), bg=FRA_BG, fg='#121f1f')
            labelTitleFIN.place(relx=0.5, rely=0.2, anchor='n')  # Used to places objects on the frame

            # Puts an instruction label in the window telling users to sign up
            instruction = tk.Label(self.homeFrame, text="Please Enter new Credentials\n", bg=FRA_BG,
                                   font=(MAIN_FONT, 12))
            instruction.place(relx=0.5, rely=0.45, anchor="n")

            # Labels to tell users where to place username and password for sign up
            self.nameL = tk.Label(self.homeFrame, text="New Username", font=(MAIN_FONT, 15), bg=FRA_BG, fg='white')
            self.pwordL = tk.Label(self.homeFrame, text="New Password", font=(MAIN_FONT, 15), bg=FRA_BG, fg='white')
            self.nameL.place(relx=0.5, rely=0.55, anchor="n")
            self.pwordL.place(relx=0.5, rely=0.7, anchor="n")

            # Places two text boxes under the according labels to accept credentials
            # as an input (Show="*" shows the password characters as *s)
            self.nameE = tk.Entry(self.homeFrame)
            self.pwordE = tk.Entry(self.homeFrame, show="*")
            self.nameE.place(relx=0.5, rely=0.6, anchor="n")
            self.pwordE.place(relx=0.5, rely=0.75, anchor="n")

            # Creates a signup button to call the next definition FSSignup
            signupButton = ttk.Button(self.homeFrame, text="Signup", command=FSSignup)
            signupButton.place(relx=0.5, rely=0.83, anchor="n")

            # Stores the users credentials entered in entry box of signup

        def FSSignup():
            # Creates document (creds - called 'tempfile')
            with open(creds, 'w') as f:
                f.write(self.nameE.get())  # Stores username string from entry on first line
                f.write('\n')  # Splits to next line
                f.write(self.pwordE.get())  # Stores password string from entry on second line
                f.close()  # Closes file
                self.homeFrame.destroy()  # Destroys the signup page
            Login()  # Calls login definition to open login page

        # Creates login window to allow users to login using signup credentials
        def Login():
            global rmuser  # more globals - used to delete login and signup return once logged in
            global loginB

            # Creates the new login window
            self.homeLFrame = tk.Frame(self, width=600, height=600, bg=FRA_BG)
            self.homeLFrame.pack()

            # Creates Winterfell title on new login frame
            labelTitleFIN = tk.Label(self.homeLFrame, text="WINTERFELL", font=(MAIN_FONT, 35), bg=FRA_BG, fg='#121f1f')
            labelTitleFIN.place(relx=0.5, rely=0.2, anchor='n')


            # Puts new instruction label in the window telling users to login
            instruction = tk.Label(self.homeLFrame, text="Please Login\n", bg=FRA_BG, font=(MAIN_FONT, 12))
            instruction.place(relx=0.5, rely=0.45, anchor="n")

            # More labels to indicate where to enter certain credentials
            self.nameL = tk.Label(self.homeLFrame, text="Username", bg=FRA_BG, font=(MAIN_FONT, 15), fg='white')
            self.pwordL = tk.Label(self.homeLFrame, text="Password", bg=FRA_BG, font=(MAIN_FONT, 15), fg='white')
            self.nameL.place(relx=0.5, rely=0.55, anchor="n")
            self.pwordL.place(relx=0.5, rely=0.7, anchor="n")

            # Two more entry boxes to enter username and password to login
            self.nameEL = tk.Entry(self.homeLFrame)
            self.pwordEL = tk.Entry(self.homeLFrame, show="*")
            self.nameEL.place(relx=0.5, rely=0.6, anchor="n")
            self.pwordEL.place(relx=0.5, rely=0.75, anchor="n")

            # Creates login button, clicked when users have finished entering credentials
            # call checklogin to check input
            loginB = ttk.Button(self.homeLFrame, text="Login", command=CheckLogin)
            loginB.place(relx=0.5, rely=0.8, anchor="n")

            # Creates remove user button to act as back button to return to signup page
            # to create new credentials if need be
            style.configure("Del.TButton", foreground='red', font=(MAIN_FONT, 9))  # styles the button to be red
            rmuser = ttk.Button(self.homeLFrame, text="Delete User", style='Del.TButton', command=DelUser)
            rmuser.place(relx=0.5, rely=0.85, anchor="n")

        # Checks input in entry of login window and compares to the tempfile document
        # to validate if the login matches
        def CheckLogin():
            # Makes username and password global to load and
            # save data in NavAccess() and save() - in stocks
            global uname, pword
            with open(creds) as f:
                data = f.readlines()  # Takes entire creds document and puts its info into a variable
                uname = data[0].rstrip()  # makes the first line (username in signup) a variable
                pword = data[1].rstrip()  # makes the second line (password in signup) a variable

            # Checks if login data matches signup data
            if self.nameEL.get() == uname and self.pwordEL.get() == pword:  # if so..

                f1 = open("tempfile.txt","w+") #creates a tempfile to store username and password
                f1.write(uname+pword)
                f1.close()

                # Opens new window to notify user that they have been logged in
                self.r = tk.Tk()
                self.r.title(":D")
                self.r.iconbitmap('favicon.ico')  # sets app icon
                self.r.geometry("150x50")

                # Prints welcome message to user using their inputed username
                rlbl = tk.Label(self.r, text='\n[+] Logged In \n Welcome back ' + self.nameEL.get() + '!')
                rlbl.pack()

                # Deletes the remove user and login buttons since no longer needed
                rmuser.destroy()
                loginB.destroy()

                self.show_frame(Invest_Page.Stocks) #opens the invest page

            # If input data do not match, creates new window notifying user that
            # this is an invalid login and to try again.
            else:
                self.r = tk.Tk()
                self.r.title("D:")
                self.r.wm_iconbitmap('favicon.ico')  # sets app icon
                self.r.geometry("150x50")
                rlbl = tk.Label(self.r, text="\n[!] Invalid Login")
                rlbl.pack()
                self.r.mainloop()
                Signup()
                # Calls signup to initiate the app

        # If need be, allows user to delete signup credentials, to return to signup page and restart
        def DelUser():
            os.remove(creds)  # deletes the creds file
            self.homeLFrame.destroy()  # destroys the login page
            Signup()  # calls signup to return to signup page


        Signup()
        # Calls signup to initiate the app
    def show_frame(self, cont):
        frame = self.controller.frames[cont]
        frame.tkraise()




