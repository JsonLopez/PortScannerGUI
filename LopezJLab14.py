#LopezJLab14.py
"""
Name: Jason Lopez
Date: December 2nd, 2022
Purpose: Create a GUI and integrate a port scanner.

Psuedo Code:
            Add GUI Port Scanner by Jason Lopez as the title of the program.
            Build a basic graphical user interface with Mainwin.
            Add three buttons for: Clear, Read Ports, and Scan IP Number.
            Add two labels and text boxes for IP Number + Connection Timeout.
            Create a textbox where our output gets dumped.
            Create a function that scans for open ports by the user input of an IP Number.
            Create a function that reads our popular ports from our csv file and dumps into text box. 

"""

import socket
import tkinter as tk
from tkinter import scrolledtext
 
Mainwin = None                                      # This is the main window on which all my elements will reside.
entryText = None                                    # Global widget for IP text entry.
entryText2 = None                                   # Global widget for timeout entry.
stMessageBox = None                                 # Global widget for scrolled text.

# This function reads the "ListOfPortNumbers.csv" file and returns contents in a list.
def ReadListOfPortNums():

    Infile = open("ListOfPortNumbers.csv", "r")     # Example: 195.78.67.42
    AllLLines = Infile.read().split("\n")
    AllWordsList = []
    for Aline in AllLLines:
        AllWordsList.append(Aline.lower())
    return AllWordsList

# This function removes all contents from any text box of the program.
def ClearEntry():
    global entryText
    global entryText2
    global stMessageBox
    entryText.delete("0", "end")                    # This will delete all the contents of the entry box from position 0 to the end.
    entryText2.delete("0", "end")                   # This will delete all the contents of the entry box 2 from position 0 to the end.
    stMessageBox.delete("1.0","end")                # The first position in the message box is 1.0 (float).

# This function reads the "ListOfPortNumbers.csv" file and returns its contents in dictionary form.
def PNDict():

    global stMessageBox 
    global PNDictionary
    PNDictionary = {}                              # Blank dictionary for the port numbers.
    Ifile = open("ListOfPortNumbers.csv", "r")     # 195.78.67.42
    next(Ifile)                                    # Skip to the next line - that is - skip the first line which is the header.
    for Aline in Ifile:
        AlineParts = Aline.strip().split(",")      # Break each line into a list of 3 strings.
        ValueList = []                             # This is the view list.
        ValueList.append(AlineParts[1])
        ValueList.append(AlineParts[2])
        PNDictionary[int(AlineParts[0])] = ValueList
    return PNDictionary

# This module displays the "ListOfPortNumbers.csv" file.
def ReadDict():

    global stMessageBox
    WordsList = ReadListOfPortNums()
    MsgBoxStr=""
    for Aword in WordsList:
        MsgBoxStr += Aword + "\n"
    stMessageBox.insert(tk.INSERT, MsgBoxStr)

# This module creates the Main Window and "paints" the various widgets on the window.
def CreateMainWindow():

    global Mainwin
    global entryText
    global entryText2
    global stMessageBox
    Mainwin.geometry("1240x555")
    Mainwin.title("GUI Port Scanner by Jason Lopez")                                # The size of the window is 875 pixels wide by 475 pixels height.
 
    # Create a label (text on window) and place it on the window using the grid layout mechanism.
    lblWelcome = tk.Label(Mainwin, text="IP Number to Scan:")                       # Labeling my first text box as IP Number to Scan.
    lblWelcome.grid(row=0, column=3)
    lblWelcome2 = tk.Label(Mainwin, text="Connection Timeout:")                     # Labeling my second text box as Connection Timeout.
    lblWelcome2.grid(row=1, column=3)
 
    # EntryText is a widget that allows you to enter the text in a text box.
    entryText = tk.Entry(Mainwin, width = 15)
    entryText.grid(row=0, column=4)
    entryText2 = tk.Entry(Mainwin, width = 15)
    entryText2.grid(row=1, column=4)
 
    # Button widget allows you to create a button and associate some action with the button.
    btnClear = tk.Button(Mainwin, text="Clear", command=ClearEntry)                # ClearEntry is the function that will be executed when the button is pressed.
    btnClear.grid(row=1, column=0, sticky="NW")                                    # Placing this button in second row, in NE (North East) NW (North West) SE or SW.
 
    # Scrolled text widget allows you to create a text box with multiple lines and a scroll bar.
    stMessageBox = tk.scrolledtext.ScrolledText(Mainwin, width=125, height=30)
    stMessageBox.grid (row=2, column=0, columnspan=2, rowspan=2)
    btnRead = tk.Button(Mainwin, text="Read Ports", command=ReadDict)              # ClearEntry is the function that will be executed when the button is pressed
    btnRead.grid(row=4, column=0, sticky="NW")                                     # Placing this button in second row, in NE (North East) NW (North West) SE or SW.
    btnCopyText = tk.Button(Mainwin, text="Scan IP Num", command = scanOneIPNum)
    btnCopyText.grid(row=4, column=1, sticky="NW")

# This module scans the IP number typed in window box, with connction timeout, and scans for open ports.
def scanOneIPNum():

    global entryText
    global entryText2
    global stMessageBox
    PNDictionary = PNDict()
    EntryTextboxStr = entryText.get()            # Get IP from box.
    TargetIP = socket.gethostbyname(EntryTextboxStr)
    EntryTextboxStr2 = float(entryText2.get())   # Get timeout from box.
    for APN in PNDictionary.keys():
        Mysock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        Mysock.settimeout(EntryTextboxStr2)
        if (Mysock.connect_ex((TargetIP, APN))) == 0:
            MsgBoxStr= (f"{APN:<12} {PNDictionary[APN][0]:<12} {PNDictionary[APN][1]:<12} \n")
            stMessageBox.insert(tk.INSERT, MsgBoxStr)
    Mainwin.update_idletasks()                   # Force the screen to show updated results.
    pass

# This function is the starting point of execution of the program.
def main():
    global Mainwin
    Mainwin = tk.Tk()                           # I am creating a main window which is a class of tk library.
    CreateMainWindow()
    Mainwin.mainloop()                          # This is the class that keeps painting the main window on the screen forever - until user kills the program.
    pass
if __name__ == "__main__":
    main()