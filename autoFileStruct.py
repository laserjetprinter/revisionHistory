import gi
from datetime import datetime
import os

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class ListBoxRowWithData(Gtk.ListBoxRow):
    def __init__(self, data):
        super().__init__()
        self.data = data
        self.add(Gtk.Label(label=data))

    def get_data(self):
        return self.data

class MyWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Revision History")

        # Setting up the Task_ID
        self.outer_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(self.outer_box)

        self.userentry_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.outer_box.add(self.userentry_box)

        self.taskid_label = Gtk.Label()
        self.taskid_label.set_text("What is the Task_ID?: Please use the following format <######>")
        self.taskid_label.set_justify(Gtk.Justification.LEFT) 
        self.userentry_box.pack_start(self.taskid_label, True, True, 0)               

        self.taskid_entry = Gtk.Entry()
        self.userentry_box.pack_start(self.taskid_entry, True, True, 0)

        # Setting up the Date
        self.date_label = Gtk.Label()
        self.date_label.set_text("What is the Date? Please use the following format <MM-DD-YYYY>, example: 01-01-2022:")
        self.date_label.set_justify(Gtk.Justification.LEFT) 
        self.userentry_box.pack_start(self.date_label, True, True, 0)               

        self.date_entry = Gtk.Entry()
        self.date_entry.set_text(f"{datetime.today().strftime('%m-%d-%Y')}")
        self.userentry_box.pack_start(self.date_entry, True, True, 0)

        # Setting up the Author
        self.author_label = Gtk.Label()
        self.author_label.set_text("What is the author name? Please use the following format <FirstName LastName>, example: Jane Doe")
        self.author_label.set_justify(Gtk.Justification.LEFT) 
        self.userentry_box.pack_start(self.author_label, True, True, 0)               

        self.author_entry = Gtk.Entry()
        self.userentry_box.pack_start(self.author_entry, True, True, 0)

        # Setting up the Comment
        self.comment_label = Gtk.Label()
        self.comment_label.set_text("What is the comment?:")
        self.comment_label.set_justify(Gtk.Justification.LEFT) 
        self.userentry_box.pack_start(self.comment_label, True, True, 0)               

        self.comment_entry = Gtk.Entry()
        self.userentry_box.pack_start(self.comment_entry, True, True, 0)

        # Setting up the File Path
        self.filepath_label = Gtk.Label()
        self.filepath_label.set_text("What is the file directory after ..\source\gc\ you would like to update? Example: elementManager\display\include")
        self.filepath_label.set_justify(Gtk.Justification.LEFT) 
        self.userentry_box.pack_start(self.filepath_label, True, True, 0)               

        self.filepath_entry = Gtk.Entry()
        self.userentry_box.pack_start(self.filepath_entry, True, True, 0)

        # Setting up File Directory List  
        self.file_label = Gtk.Label()
        self.file_label.set_text("Select the files to add revision history to below:")
        self.file_label.set_justify(Gtk.Justification.LEFT) 
        self.userentry_box.pack_start(self.file_label, True, True, 0) #Need to figure out how to hide this label until okay is selected

        self.file_listbox = Gtk.ListBox()
        self.file_listbox.set_selection_mode(Gtk.SelectionMode.MULTIPLE)

        # Setting up the Okay and Cancel buttons
        button_box = Gtk.Box(spacing=6)
        self.outer_box.pack_start(button_box, True, True, 0)

        self.okay_button = Gtk.Button(label="Okay")
        self.okay_button.connect("clicked", self.okay_clicked)
        button_box.pack_start(self.okay_button, True, True, 0)

        self.click_tracker = 0

        self.cancel_button = Gtk.Button(label="Cancel")
        self.cancel_button.connect("clicked", self.cancel_clicked)
        button_box.pack_start(self.cancel_button, True, True, 0)

    def okay_clicked(self, widget):
        # Verify all entries have been filled out
        if len(self.taskid_entry.get_text()) == 0 or len(self.date_entry.get_text()) == 0 or len(self.author_entry.get_text()) == 0 or len(self.comment_entry.get_text()) == 0 or len(self.filepath_entry.get_text()) == 0:
            print('Please fill out all text fields before selecting "Okay"')
        elif self.click_tracker == 0:
            # Increment the click tracker so that the selection list is not regenerated if clicking
            # "Okay" more than once
            self.click_tracker = 1

            # Code added by Rena to have the system work on the GC system. Commenting out to work on local system.
            # current_path = os.get_cwd()
            # source_path = current_path.index('\gc')
            # dir_path = f'{current_path[0:(source_path + 3)]}\{self.filepath_entry.get_text()}'

            dir_path = self.filepath_entry.get_text()

            tempfile_list = []

            # Iterate through directory and fill up tempFileList with current files
            for path in os.listdir(dir_path):
                # Check if current path is a file
                if os.path.isfile(os.path.join(dir_path, path)):
                    if path[0] == ".": # Skips adding the .DS_Store file that is auto added and any hidden files
                        pass
                    else:
                        self.file_listbox.add(ListBoxRowWithData(path)) #Adds file to scroll bar list
            
            self.userentry_box.pack_start(self.file_listbox, True, True, 0)

            self.file_listbox.show_all()
        else:
            #Close the window and update the files
            # Set the user entry fields equal to variables
            author = self.author_entry.get_text()
            taskID = self.taskid_entry.get_text()
            date = self.date_entry.get_text()
            comment = self.comment_entry.get_text()

            #Format the author name to be maximum 15 characters, otherwise clip to FirstInitial.LastName
            auth = self.author_entry.get_text() #Python throws error for local variable referenced before assignment with below logic
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
            revString = taskID.ljust(12, ' ') + date.ljust(18, ' ') + auth.ljust(25, " ") + comment + "\n"

            # Loop through the selected files and add revision history entries
            selected_files = self.file_listbox.get_selected_rows()
            for entry in selected_files:
                # Open each file and add history
                print(f'Adding revision history to {entry.get_data()}')
                filePath = self.filepath_entry.get_text() + "/" + entry.get_data()
                openedFile = open(filePath, 'r+')
                fileLines = openedFile.readlines()

                # Tracks index to insert new line at
                lineNum = 0

                # Cycles through the file lines to identify the *</pre> line
                for line in fileLines:
                    lineList = line.split()

                    if '/pre' in lineList[0]:
                        # Checks for the characters that start the comment lines by taking the characters before the 
                        # </pre> statement at the end of the comment blocks.
                        clipIndex = lineList[0].index('</pre')
                        commentLine = lineList[0][0:clipIndex] + " " + revString

                        # Sets the cursor to the beginning of the file, so the whole file is overwritten
                        openedFile.seek(0)
                        fileLines.insert(lineNum, commentLine)
                        openedFile.writelines(fileLines)
                        openedFile.truncate()
                        openedFile.close()
                        break

                    lineNum+=1
            
            # Program completed
            quit()
                
    def cancel_clicked(self, widget):
        quit()

win = MyWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()