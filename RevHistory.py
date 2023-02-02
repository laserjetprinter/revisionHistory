# RevHistory.py
# Task_ID        Date              Author                     Description
# N/A            01/11/2023        N.Davis                    Initial Revision
# N/A            02/02/2023        R.Yang                     Fixed final button prompting, added defaults and input options


from tkinter import *
import tkinter as tk
from tkinter import simpledialog
from tkinter import Scrollbar
from tkinter import Listbox
from datetime import datetime
import os

#Set up tk windows
root = tk.Tk()
root.withdraw()

# User input for revision history comment. If cancel is pressed, the program quits.
taskID = simpledialog.askstring(title="Revision History Input",
    prompt="What is the Task_ID?: Please use the following format <XX######>, example: DR123456")
if not taskID:
    quit()

author = simpledialog.askstring(title="Revision History Input",
    prompt="What is the author name? Please use the following format <FirstName LastName>, example: Jane Doe")
if not author:
    quit()

date = simpledialog.askstring(title="Revision History Input",
    prompt="What is the Date? Please use the following format <MM-DD-YYYY>, example: 01-01-2022", 
    initialvalue=f"{datetime.today().strftime('%m-%d-%Y')}") # default with today's date
if not date:
    quit()

comment = simpledialog.askstring(title="Revision History Input",
    prompt="What is the comment?:")
if not comment:
    quit()

dirPath = simpledialog.askstring(title="Revision History Input",
    prompt="What is the file directory after ..\source\gc\ you would like to update? Example: elementManager\display\include",
    initialvalue= "elementManager\display\src")
# Add the inputted file path to the sourcepath directory so it will have the username and repo folder
if dirPath:
    currentPath = os.getcwd()
    sourcePath = currentPath.index('\gc')  
    dirPath = f'{currentPath[0:(sourcePath + 3)]}\{dirPath}'
if not dirPath:
    quit()

# User selection for files to update
filesWindow = Tk()
filesWindow.title('Files to Update')
  
# Setting up scrolling vertically
yscrollbar = Scrollbar(filesWindow)
yscrollbar.pack(side = RIGHT, fill = Y)
  
label = Label(filesWindow,
              text = "Select the files to update revision history:  ",
              font = ("Times New Roman", 15), 
              padx = 10, pady = 10)
label.pack()
list = Listbox(filesWindow, selectmode = "multiple") 
  
# Widget expands horizontally and 
# vertically by assigning both to
# fill option
list.pack(padx = 10, pady = 10,
          expand = YES, fill = "both")

#Path to files to update revision history from input
x =[os.listdir(dirPath)]
  
# tempFileList used to form the file scroll bar window
# selectedFiles used to store user selected files for adding rev history
tempFileList = []
selectedFiles = []

# Iterate through directory and fill up tempFileList with current files
for path in os.listdir(dirPath):
    # check if current path is a file
    if os.path.isfile(os.path.join(dirPath, path)):
        tempFileList.append(path)

for each_item in range(len(tempFileList)):
      
    list.insert(END, tempFileList[each_item])
    list.itemconfig(each_item, bg = "white")

# Called when an item is selected, updates selection list and stores files selected in list
def onselect(evt):
    w = evt.widget
    try:
        idx = w.curselection()
        if selectedFiles:
            selectedFiles.clear()
        for i in idx:
            value = w.get(i)
            selectedFiles.append(value)
    except IndexError:
        return

# Attach listbox to vertical scrollbar and monitors for files that are selected by user
yscrollbar.config(command = list.yview)
yscrollbar.pack(side=BOTTOM)
selectedFiles = []
list.bind('<<ListboxSelect>>', onselect)

# Closes the file scroll bar window if the cancel button has been selected
def closeWindow():
    filesWindow.destroy()
    quit()
  
# Processes the selections with the file scroll bar window if the okay button has been selected
def addHistory():
    # Closes the window
    filesWindow.destroy()

    #Format the author name to be maximum 15 characters, otherwise clip to FirstInitial.LastName
    auth = author #Python throws error for local variable referenced before assignment with below logic
    if len(author) > 15:
        print('Author name length longer than 15 characters, updating to form <J.Doe>')
        authorList = author.split()
        
        #If lastname is longer than 13 characters
        if len(authorList[1]) > 13:
            print('Author last name length longer than 13 characters, clipping to first 13 characters.')
            auth = authorList[0][0] + "." + authorList[1][0:13]
            print(auth)
        else:
            auth = authorList[0][0] + "." + authorList[1]
            print(auth)

    # Format the string to put into revision history. It should be in the following format:
    # <comment character(s)> <1 space> <Task_ID> <6 spaces> <Date> <8 spaces> <Author> <10 spaces> <Description>
    # Note that the Task_ID defaults to 6 characters, the Date defaults to 10 characters, and the author takes into
    # account the maximum length of 15 characters
    revString = taskID.ljust(13, ' ') + date.ljust(12, ' ') + auth.ljust(16, " ") + comment + "\n"

    # Open each file and add history
    for curFile in selectedFiles:
        print(f'Adding revision history to {curFile}')
        filePath = dirPath + "/" + curFile
        openedFile = open(filePath, 'r+')
        fileLines = openedFile.readlines()

        # Tracks index to insert new line at
        lineNum = 0

        # Cycles through the file lines to identify the *</pre> line
        for line in fileLines:
            lineList = line.split()

            if '/pre' in lineList[1]:
                # Checks for the characters that start the comment lines by taking the characters before the 
                # </pre> statement at the end of the comment blocks.
                clipSplit = line.split("</pre>")[0]
                commentLine = clipSplit + revString

                # Sets the cursor to the beginning of the file, so the whole file is overwritten
                openedFile.seek(0)
                fileLines.insert(lineNum, commentLine)
                openedFile.writelines(fileLines)
                openedFile.truncate()
                openedFile.close()
                break

            lineNum+=1
    
    # Exits program when complete
    quit()

# Buttons for accepting or closing file scroll bar window
exitButton = Button(yscrollbar, text="Cancel", command=closeWindow)
exitButton.pack(side=RIGHT)
okayButton = Button(yscrollbar, text="Okay", command=addHistory)
okayButton.pack(side=LEFT)

filesWindow.mainloop()