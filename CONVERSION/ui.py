import logging
import os
import threading
from tkinter import *
import tkinter as tk
from tkinter import ttk
import random
import time
import datetime

import backend
from tkinter import *
from tkinter import filedialog, messagebox
from datetime import datetime
from backend import Backend

import pymongo
from tkinter import PhotoImage

from config import mongo_host, mongo_port, mongo_database, mongo_collection
from tkinter import Tk, Label
from PIL import ImageTk, Image



from datetime import datetime
from pymongo import MongoClient

import pygame

#======================================================MONGO DB=========================================================
client = pymongo.MongoClient('mongodb://localhost:27017/')
database = client['Announcementapp']
collection = database['ScheduleAnnouncement']




#========================================================================================================================

class AnnouncementScheduler:
    def __init__(self, root):
        self.root = root
        self.root.title("Announcement Scheduler")
        self.root.geometry("1540x800+0+0")



        pygame.init()
        pygame.mixer.init()






        #==================================================Main label=================================================


        # Load the logo image
        self.logo_image = PhotoImage(file="Ct_logo.png")

        # Adjust the size of the logo image
        logo_width = 40  # Specify the desired width
        logo_height = 40  # Specify the desired height
        self.logo_image = self.logo_image.subsample(int(self.logo_image.width() / logo_width),
                                                    int(self.logo_image.height() / logo_height))

        # Create the label with the resized logo image on the left
        lbltitle = Label(self.root, bd=10, relief=RIDGE, text="CT UNIVERSITY ANNOUNCEMENT SYSTEM", fg="blue",
                         bg="white", font=("times new roman", 20, "bold"), compound="left", image=self.logo_image,
                         padx=10)  # Add padding of 10 pixels from the right side

        lbltitle.pack(side=TOP, fill=X)
        #================================ConnectionFunction=============================================================
        def connect_to_mongodb():
            # Connect to MongoDB using the imported connection settings
            client = pymongo.MongoClient(f'mongodb://{mongo_host}:{mongo_port}')
            database = client[mongo_database]
            collection = database[mongo_collection]
            return collection
        #================================Placeholder functionality======================================================
        def on_entry_click(event):
            if announcement_entry.get() == "Announcement":
                announcement_entry.delete(0, "end")  # Remove the placeholder text
                announcement_entry.config(fg="black")  # Change text color to black

        def on_focus_out(event):
            if announcement_entry.get() == "":
                announcement_entry.insert(0, "Announcement")  # Insert the placeholder text
                announcement_entry.config(fg="grey")  # Change text color to grey


        # ================================DATAFRAME=====================================================================
        DataFrame = Frame(self.root, bd=3, padx=20, relief=GROOVE)
        DataFrame.place(x=0, y=90, width=1530, height=480)
#-----------------------------------------------------------------------------------------------------------------------------------------
        DataFrameLeft = LabelFrame(DataFrame, bd=2, padx=20, relief=RIDGE, font=("arial", 12, "bold"),
                                   text="Announcement Scheduler")
        DataFrameLeft.place(x=0, y=5, width=300, height=450)
#-----------------------------------------------------------------------------------------------------------------------------------------


        DataFrameMiddle = LabelFrame(DataFrame, bd=2, padx=20, relief=RIDGE, font=("arial", 12, "bold"),
                                     text="Controls")
        DataFrameMiddle.place(x=320, y=5, width=300, height=450)



#--------------------------------------------------------------------------------------------------------------------------------------

        from datetime import date, datetime

        # ...

        DataFrameRighttop = LabelFrame(DataFrame, bd=2, padx=20, relief=RIDGE, font=("arial", 12, "bold"),
                                       text="Current Day Announcements")
        DataFrameRighttop.place(x=640, y=5, width=850, height=225)

        scroll_x = ttk.Scrollbar(DataFrameRighttop, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(DataFrameRighttop, orient=VERTICAL)
        self.currentdayannouncement_table = ttk.Treeview(DataFrameRighttop,
                                                         columns=(
                                                         "lblName", "lblDate", "lblTime", "lblRepeat", "lblFile"),
                                                         xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)

        scroll_x.config(command=self.currentdayannouncement_table.xview)
        scroll_y.config(command=self.currentdayannouncement_table.yview)

        self.currentdayannouncement_table.heading("lblName", text="Label",anchor="w")
        self.currentdayannouncement_table.heading("lblDate", text="Date",anchor="w")
        self.currentdayannouncement_table.heading("lblTime", text="Time",anchor="w")
        self.currentdayannouncement_table.heading("lblRepeat", text="Repeat",anchor="w")
        self.currentdayannouncement_table.heading("lblFile", text="File",anchor="w")

        # Set the column width to fit the content
        self.currentdayannouncement_table.column("lblName", width=100)
        self.currentdayannouncement_table.column("lblDate", width=100)
        self.currentdayannouncement_table.column("lblTime", width=100)
        self.currentdayannouncement_table.column("lblRepeat", width=100)
        self.currentdayannouncement_table.column("lblFile", width=800)

        # Remove the empty first column
        self.currentdayannouncement_table["show"] = "headings"

        # Pack the table
        self.currentdayannouncement_table.pack(fill=BOTH, expand=1)

        from datetime import date, datetime

        # ...

        def display_currentday_scheduled_announcements():
            # Call the connect_to_mongodb() function to get the MongoDB collection
            collection = connect_to_mongodb()

            # Get the current date
            current_date = date.today().strftime("%Y-%m-%d")

            # Clear the current contents of the table
            self.currentdayannouncement_table.delete(*self.currentdayannouncement_table.get_children())

            # Retrieve and filter the announcements for the current date
            data = collection.find({"date": current_date})

            # Iterate over the retrieved data
            for document in data:
                announcement = [
                    document.get('announcement'),
                    document.get('date'),
                    document.get('schedule_time'),
                    document.get('repeat'),
                    document.get('file_path')
                ]
                self.currentdayannouncement_table.insert("", "end", values=announcement)

        # Call the function to display the announcements for the current day
        display_currentday_scheduled_announcements()



        #-----------------------------------------------------------------------------------------------------------------------------------------


        DataFrameRightbottom = LabelFrame(DataFrame, bd=2, padx=20, relief=RIDGE, font=("arial", 12, "bold"),
                                          text="Scheduled Announcements")
        DataFrameRightbottom.place(x=640, y=230, width=850, height=225)

        # Create the Treeview table
        scheduled_announcement_table = ttk.Treeview(DataFrameRightbottom,
                                                    columns=("lblName", "lblDate", "lblTime", "lblRepeat", "lblFile"),
                                                    xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

        # Set the column headings with centered alignment
        scheduled_announcement_table.heading("lblName", text="Label", anchor="w")
        scheduled_announcement_table.heading("lblDate", text="Date", anchor="w")
        scheduled_announcement_table.heading("lblTime", text="Time", anchor="w")
        scheduled_announcement_table.heading("lblRepeat", text="Repeat", anchor="w")
        scheduled_announcement_table.heading("lblFile", text="File", anchor="w")

        # Set the column width to fit the content
        scheduled_announcement_table.column("lblName", width=100)
        scheduled_announcement_table.column("lblDate", width=100)
        scheduled_announcement_table.column("lblTime", width=100)
        scheduled_announcement_table.column("lblRepeat", width=100)
        scheduled_announcement_table.column("lblFile", width=800)

        # Configure the scrollbars
        scroll_x.config(command=scheduled_announcement_table.xview)
        scroll_y.config(command=scheduled_announcement_table.yview)

        # Remove the empty first column
        scheduled_announcement_table["show"] = "headings"

        # Pack the Treeview table
        scheduled_announcement_table.pack(fill=tk.BOTH, expand=1)

        import datetime
        from datetime import datetime

        def display_scheduled_announcements():
            # Call the connect_to_mongodb() function to get the MongoDB collection
            collection = connect_to_mongodb()

            # Get the current date
            current_date = date.today().strftime("%Y-%m-%d")

            # Query the collection to retrieve schedules with dates greater than or equal to the current date
            query = {'date': {'$gte': current_date}}
            data = collection.find(query)

            print(data)



            # Clear the current contents of the table
            scheduled_announcement_table.delete(*scheduled_announcement_table.get_children())

            # Iterate over the retrieved data
            for document in data:
                announcement = [
                    document.get('announcement'),
                    document.get('date'),
                    document.get('schedule_time'),  # Retrieve the 'schedule_time' field instead of 'time'
                    document.get('repeat'),
                    document.get('file_path')
                ]
                scheduled_announcement_table.insert("", "end", values=announcement)

        # Call the function to display scheduled announcements initially
        display_scheduled_announcements()

        # =============================================Browse Option====================================================

        # ===============================================================================================================
        # =================================================Buttons========================================================
        Buttonframe = Frame(self.root, bd=2, relief=GROOVE)
        Buttonframe.place(x=0, y=550, width=1530, height=50)

        # =================================================Details========================================================

        Detailsframe = Frame(self.root, bd=2, relief=RIDGE)
        Detailsframe.place(x=0, y=600, width=1530, height=190)

        # ====================================DATAFRAMELEFT==============================================================
        def add_schedule():
            """Function to handle add schedule button click event"""
            announcement = announcement_entry.get()
            date = date_entry.get()
            time = time_entry.get()
            repeat = repeat_var.get()
            file_path = self.file_path

            # Schedule the job using the backend
            backend.add_schedule(announcement, date, time, repeat, file_path)

            # Display message boxes
            messagebox.showinfo("Schedule Added", "Announcement scheduled successfully!")


        # UI Components
        lblName = Label(DataFrameLeft, text="Label", font=("times new roman", 10, ""), padx=0, pady=15)
        lblName.grid(row=0, column=0)
        announcement_entry = Entry(DataFrameLeft, font=("times new roman", 12), bd=1, relief=RIDGE, width=20)
        announcement_entry.insert(0, "Announcement")  # Insert the placeholder text initially
        announcement_entry.bind("<FocusIn>", on_entry_click)
        announcement_entry.bind("<FocusOut>", on_focus_out)
        announcement_entry.grid(row=0, column=1, padx=(10, 20), sticky=W)

        lblDate = Label(DataFrameLeft, text="Date", font=("times new roman", 10, ""), padx=0, pady=15)
        lblDate.grid(row=1, column=0)
        date_entry = Entry(DataFrameLeft, font=("times new roman", 12), bd=1, relief=RIDGE, width=20)
        date_entry.grid(row=1, column=1, padx=(10, 20), sticky=W)

        lblTime = Label(DataFrameLeft, text="Time", font=("times new roman", 10, ""), padx=0, pady=15)
        lblTime.grid(row=2, column=0)
        time_entry = Entry(DataFrameLeft, font=("times new roman", 12), bd=1, relief=RIDGE, width=20)
        time_entry.grid(row=2, column=1, padx=(10, 20), sticky=W)

        lblRepeat = Label(DataFrameLeft, text="Repeat", font=("times new roman", 10, ""), padx=0, pady=15, width=10)
        lblRepeat.grid(row=3, column=0)
        repeat_var = StringVar()
        repeat_dropdown = ttk.Combobox(DataFrameLeft, textvariable=repeat_var, font=("times new roman", 12),
                                       state="readonly", width=20)
        repeat_dropdown["values"] = ("Everyday", "Once")
        repeat_dropdown.current(1)  # Set default selection to index 1, which is "Once"
        repeat_dropdown.grid(row=3, column=1, padx=(10, 20), sticky=W)

        import datetime as dt
        # Set current date and time in the respective entry fields
        current_date = dt.datetime.now().strftime("%Y-%m-%d")
        current_time = dt.datetime.now().strftime("%H:%M:%S")

        date_entry.insert(0, current_date)
        time_entry.insert(0, current_time)

        lblFile = Label(DataFrameLeft, text="Upload File", font=("times new roman", 10, ""), padx=0, pady=15)
        lblFile.grid(row=4, column=0, sticky=E)  # Adjust the sticky attribute to align the label to the right

        # Create the schedule button
        schedule_button = Button(DataFrameLeft, text="Add Schedule", command=add_schedule,
                                 font=("times new roman", 12, "bold"), bg="blue", fg="white", width=20)
        schedule_button.grid(row=8, column=0, columnspan=2, padx=40, pady=30)

        # Add browse button

        def browse_files():
            filetypes = (("Audio files", "*.mp3;*.wav"), ("All files", "*.*"))
            selected_files = filedialog.askopenfilenames(filetypes=filetypes)
            self.file_listbox.delete(0, END)  # Clear previous file list

            if selected_files:
                for file_path in selected_files:
                    self.file_listbox.insert(END, file_path)

                # Store the selected file paths in the file_paths attribute as a list
                self.file_paths = list(selected_files)



        browse_button = Button(DataFrameLeft, text="Browse", command=browse_files, font=("times new roman", 12, "bold"))
        browse_button.grid(row=4, column=1, padx=(10, 20), pady=15, sticky=W)  # Adjust the column and sticky attributes



        # Create the backend instance
        backend = Backend()
        # =================================================Actual Buttons===============================================

        def open_update_form():
            # Get the selected item from the Treeview table
            selected_item = scheduled_announcement_table.focus()

            if selected_item:
                # Create a new window for the update form
                update_window = tk.Toplevel(root)
                update_window.title("Update Announcement")
                update_window.geometry("300x300")

                # Get the values of the selected item
                item_values = scheduled_announcement_table.item(selected_item)['values']
                label = item_values[0]  # Assuming the label is in the first column
                date = item_values[1]  # Assuming the date is in the second column
                time = item_values[2]  # Assuming the time is in the third column
                repeat = item_values[3]  # Assuming the repeat is in the fourth column
                file_path = item_values[4]  # Assuming the file_path is in the fifth column

                # Function to handle the update action
                def update_announcement():
                    # Get the updated values from the form fields
                    updated_label = label_entry.get()
                    updated_date = date_entry.get()
                    updated_time = time_entry.get()
                    updated_repeat = repeat_var.get()
                    updated_file_path = selected_file.get()

                    # Update the selected item in the Treeview table
                    scheduled_announcement_table.set(selected_item, "lblName", updated_label)
                    scheduled_announcement_table.set(selected_item, "lblDate", updated_date)
                    scheduled_announcement_table.set(selected_item, "lblTime", updated_time)
                    scheduled_announcement_table.set(selected_item, "lblRepeat", updated_repeat)
                    scheduled_announcement_table.set(selected_item, "lblFile", updated_file_path)

                    # Update the corresponding item in the database
                    collection.update_one(
                        {'announcement': label},
                        {'$set': {
                            'announcement': updated_label,
                            'date': updated_date,
                            'schedule_time': updated_time,
                            'repeat': updated_repeat,
                            'file_path': updated_file_path
                        }}
                    )

                    # Close the update form window
                    update_window.destroy()

                    # Show a message indicating successful update
                    messagebox.showinfo("Update Successful", "Announcement has been updated.")

                # Create labels and entry fields for the update form
                label_label = tk.Label(update_window, text="Label:")
                label_label.pack()
                label_entry = tk.Entry(update_window)
                label_entry.pack()
                label_entry.insert(0, label)

                date_label = tk.Label(update_window, text="Date:")
                date_label.pack()
                date_entry = tk.Entry(update_window)
                date_entry.pack()
                date_entry.insert(0, date)

                time_label = tk.Label(update_window, text="Time:")
                time_label.pack()
                time_entry = tk.Entry(update_window)
                time_entry.pack()
                time_entry.insert(0, time)

                repeat_label = tk.Label(update_window, text="Repeat:")
                repeat_label.pack()
                repeat_var = tk.StringVar(update_window)
                repeat_var.set(repeat)  # Set the default value
                repeat_dropdown = tk.OptionMenu(update_window, repeat_var, "Once", "Everyday")
                repeat_dropdown.pack()

                def browse_file():
                    # Open a file dialog to select the sound file
                    file_path = filedialog.askopenfile(parent=update_window, filetypes=[("Sound Files", "*.wav;*.mp3")])
                    if file_path is not None:
                        selected_file.set(file_path.name)
                        file_name = os.path.basename(file_path.name)  # Extract the file name from the path
                        selected_file_label.config(text=file_name)  # Update the label with the selected file name

                # ...

                file_path_label = tk.Label(update_window, text="File Path:")
                file_path_label.pack()
                selected_file = tk.StringVar()  # Variable to store the selected file path

                browse_button = tk.Button(update_window, text="Browse", command=browse_file)
                browse_button.pack()

                # Label to show the selected file path
                selected_file_label = tk.Label(update_window, text="")
                selected_file_label.pack()

                # Create the update button
                update_button = tk.Button(update_window, text="Update", command=update_announcement)
                update_button.pack()
            else:
                messagebox.showinfo("No item selected", "Please select an item before updating.")

                # Create the update button in the main GUI
        btnUpdate = tk.Button(Buttonframe, text="Update", font=("times new roman", 12, "bold"), bg="green",
                                      fg="white", width=21, height=1, padx=2, pady=6, command=open_update_form)
        btnUpdate.grid(row=0, column=0, padx=(660, 10), sticky='e')

                #-----------------------------------------------------------------------------------------------------------------------------
        def delete_scheduled_announcement():
            # Get the selected item from the Treeview table
            selected_item = scheduled_announcement_table.focus()

            if selected_item:
                # Extract the necessary information from the selected item
                item_values = scheduled_announcement_table.item(selected_item)['values']
                label = item_values[0]  # Assuming the label is in the first column

                # Connect to the MongoDB and retrieve the collection
                collection = connect_to_mongodb()

                # Delete the document from the database using the extracted label
                collection.delete_one({'announcement': label})

                # Remove the selected item from the Treeview table
                scheduled_announcement_table.delete(selected_item)
            else:
                print("No item selected.")

        # Bind the delete_scheduled_announcement function to the "Delete" button
        btnDelete = Button(Buttonframe, text="Delete", font=("times new roman", 12, "bold"), bg="green", fg="white",
                           width=21, height=1, padx=2, pady=6, command=delete_scheduled_announcement)
        btnDelete.grid(row=0, column=1, padx=(0, 10), sticky='e')


#-----------------------------------------------------------------------------------------------------------------------------
        def reset_selection():
            global scheduled_announcements  # Use the global scheduled_announcements variable

            # Get the selected item from the Treeview table
            selected_item = scheduled_announcement_table.focus()

            if selected_item:
                # Set the "File" value of the selected item to "None"
                scheduled_announcement_table.set(selected_item, "lblFile", "None")

                # Disable the announcement from playing by removing the file_path in the scheduled_announcements dictionary
                item_values = scheduled_announcement_table.item(selected_item)['values']
                label = item_values[0]  # Assuming the label is in the first column
                if label in scheduled_announcements:
                    scheduled_announcements[label]['file_path'] = "None"

                    # Update the database with the new "file_path" value
                    collection.update_one(
                        {'announcement': label},
                        {'$set': {'file_path': "None"}}
                    )
            else:
                print("No item selected.")

        # Create the Reset button and bind the reset_selection function to it
        btnReset = Button(Buttonframe, text="Reset", font=("times new roman", 12, "bold"), bg="green", fg="white",
                          width=21, height=1, padx=2, pady=6, command=reset_selection)
        btnReset.grid(row=0, column=2, padx=(0, 10), sticky='e')

        #------------------------------------------------------------------------------------------------------------------------
        def exit_application():
            result = messagebox.askquestion("Exit Application", "Are you sure you want to exit?", icon="warning")
            if result == "yes":
                # Close the application
                root.destroy()

        # Create the Exit button and bind the exit_application function to it
        btnExit = Button(Buttonframe, text="Exit", font=("times new roman", 12, "bold"), bg="green", fg="white",
                         width=21, height=1, padx=2, pady=6, command=exit_application)
        btnExit.grid(row=0, column=3, columnspan=6, sticky='e')

        #==================================================To display dataframe logs====================================
        def show_logs():
            log_file = 'backend.log'  # Path to the log file

            # Create a text widget to display the logs
            logs_text = Text(Detailsframe, font=("times new roman", 10), bd=1, relief=RIDGE, width=150, height=10)
            logs_text.pack(fill=BOTH, expand=1)

            try:
                # Read the entire log file
                with open(log_file, 'r') as file:
                    logs = file.readlines()

                # Filter out the debug log entries
                logs = [log for log in logs if not log.startswith('DEBUG')]

                # Join the filtered logs into a single string
                logs = ''.join(logs)

                # Insert the logs into the text widget at the beginning
                logs_text.insert('1.0', logs)

                # Disable the text widget for editing
                logs_text.config(state='disabled')

                # Get the initial size of the log file
                initial_size = os.path.getsize(log_file)

                def monitor_logs():
                    nonlocal initial_size
                    while True:
                        # Check if the log file has been modified
                        if os.path.getsize(log_file) > initial_size:
                            # Open the log file in read mode
                            with open(log_file, 'r') as file:
                                # Move the file pointer to the end
                                file.seek(initial_size)

                                # Read the new log entries
                                logs = file.readlines()

                            # Filter out the debug log entries
                            logs = [log for log in logs if not log.startswith('DEBUG')]

                            # Join the filtered logs into a single string
                            logs = ''.join(logs)

                            # Insert the new logs into the text widget at the beginning
                            logs_text.config(state='normal')  # Enable the text widget for editing
                            logs_text.insert('1.0', logs)
                            logs_text.config(state='disabled')  # Disable the text widget for editing

                            # Update the initial size of the log file
                            initial_size = os.path.getsize(log_file)

                        # Wait for a short interval before checking for updates again
                        time.sleep(0.5)

                # Create a new thread for monitoring logs
                log_monitor_thread = threading.Thread(target=monitor_logs)
                log_monitor_thread.daemon = True  # Set the thread as a daemon to stop it when the main thread ends
                log_monitor_thread.start()

            except FileNotFoundError:
                logs_text.insert('1.0', "Log file not found.")

        # Call the show_logs function to display the logs on the UI and get real-time updates
        show_logs()

        #===============================================================================================================
        # Add Schedule button


        # ===============================================DATAFRAME MIDDLE================================================
        # Add message box, control buttons, and volume controller



        self.play_button = Button(DataFrameMiddle, text="Play", command=self.play_selected_sound,
                                  font=("times new roman", 12, "bold"))
        self.play_button.grid(row=2, column=0, padx=10, pady=20, sticky=W)

        self.pause_button = Button(DataFrameMiddle, text="Pause", command=self.pause_selected_sound,
                                   font=("times new roman", 12, "bold"))
        self.pause_button.grid(row=2, column=1, padx=10, pady=20, sticky=W)

        self.stop_button = Button(DataFrameMiddle, text="Stop", command=self.stop_selected_sound,
                                  font=("times new roman", 12, "bold"))
        self.stop_button.grid(row=2, column=2, padx=10, pady=20, sticky=W)

        #--------------------------------------------------------------------------------------------------------------------

        self.volume_title_label = Label(DataFrameMiddle, text="Volume:", font=("times new roman", 10, "bold"))
        self.volume_title_label.grid(row=3, column=0, padx=10, pady=(20, 0), sticky=W)

        from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume

        def adjust_system_volume(volume):
            sessions = AudioUtilities.GetAllSessions()
            for session in sessions:
                volume_interface = session._ctl.QueryInterface(ISimpleAudioVolume)
                volume_interface.SetMasterVolume(volume / 100, None)

        # Create the volume scale
        self.volume_scale = Scale(DataFrameMiddle, from_=0, to=100, orient="horizontal",
                                  font=("times new roman", 15, "bold"), length=200, sliderlength=20,
                                  showvalue=True)
        self.volume_scale.set(50)  # Initial volume level
        self.volume_scale.grid(row=4, column=0, columnspan=3, padx=10, pady=10, sticky="w")

        self.volume_scale.bind("<ButtonRelease-1>", lambda event: adjust_system_volume(self.volume_scale.get()))



        #===============================================================================================================

        DataFrameMiddle.columnconfigure(0, weight=1)
        DataFrameMiddle.columnconfigure(1, weight=1)
        DataFrameMiddle.columnconfigure(2, weight=1)

        # Create a frame for the selected file label
        selected_file_frame = Frame(DataFrameLeft)
        selected_file_frame.grid(row=8, column=0, pady=(10, 5), sticky=W)

        # Create a label for the selected file with text wrapping
        selected_file_label = Label(DataFrameLeft, text="Selected File: ", font=("times new roman", 10, ""),
                                    wraplength=200, anchor=W, justify=LEFT)
        selected_file_label.grid(row=6, column=0, pady=(10, 5))

        # Create a label to display the selected file path
        self.selected_file_path_label = Label(DataFrameLeft, text="", font=("times new roman", 10, ""), wraplength=200,
                                              anchor=W, justify=LEFT)
        self.selected_file_path_label.grid(row=6, column=1, pady=(10, 5), sticky=W)

        # Variable to store the selected file path
        self.file_path = ""

        # Function to update the selected file path label
        def update_selected_file_path_label(event):
            selected_file = self.file_listbox.get(self.file_listbox.curselection())
            file_name = os.path.basename(selected_file)  # Extract the filename from the path
            self.selected_file_path_label.config(text=file_name)  # Display only the filename

            self.file_path = selected_file  # Update the file_path attribute with the selected file path

        # Add the scrollbar to the file_listbox
        self.file_listbox = Listbox(DataFrameMiddle, font=("times new roman", 12), bd=1, relief=RIDGE, width=30,
                                    height=9)
        self.file_listbox.grid(row=0, column=0, padx=20, pady=(10, 0), columnspan=3, sticky=N)

        # Configure the file_listbox width to fill available space in DataFrameMiddle
        DataFrameMiddle.columnconfigure(0, weight=1)
        self.file_listbox.grid_configure(sticky="nsew")


        # Bind the update_selected_file_path_label function to selection changes in the file_listbox
        self.file_listbox.bind('<<ListboxSelect>>', update_selected_file_path_label)



        # Prevent disturbance in DataFrameLeft alignment
        DataFrameLeft.grid_propagate(False)

        # Function to get the selected file path
    def get_selected_file_path(self, callback):
            file_path = callback()
            return file_path





    def play_selected_sound(self):
        selected_file = self.file_listbox.get(self.file_listbox.curselection())
        pygame.mixer.music.load(selected_file)
        pygame.mixer.music.play()


    def pause_selected_sound(self):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()



    def stop_selected_sound(self):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()


    def pause_audio(self):
        if self.audio_state == "playing":
            pygame.mixer.music.pause()
            self.audio_state = "paused"

    def stop_audio(self):
        if self.audio_state == "playing" or self.audio_state == "paused":
            pygame.mixer.music.stop()
            self.audio_state = "stopped"

            self.play_button.config(command=self.play_audio)
            self.pause_button.config(command=self.pause_audio)
            self.stop_button.config(command=self.stop_audio)

    def run(self):
            self.root.mainloop()







if __name__ == "__main__":
        root = Tk()
        app = AnnouncementScheduler(root)
        app.run()