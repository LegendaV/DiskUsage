import sys
import Analizer
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from datetime import datetime
from PIL import ImageTk, Image


class DiskUsage:
    def __init__(self):
        self.directory_icon = Image.open(f'Images{os.path.sep}directory_icon.png').resize((15, 15), Image.ANTIALIAS)


    def insert_directories(self, directory_info, table, parentID="", space_count=0):
        directories = directory_info.directories
        directories.sort(reverse=True, key=lambda d:d.size)
        for d in directories:
            info = ('-' * space_count + os.path.basename(d.path), round(d.size / 2**20, 5), round(d.size/self.main_directory.size, 2) * 100, datetime.fromtimestamp(max(d.ctime,0)))
            directoryID = table.insert(parentID, 'end', values=info, tags=("custom_color",), image=self.directory_icon)
            self.insert_directories(d, table, directoryID, space_count+1)

        files_data = []
        for f in directory_info.files_info:
            info = directory_info.files_info[f]
            files_data.append(('-' * space_count + f, round(info.st_size / 2**20, 5), round(info.st_size/self.main_directory.size, 2) * 100, datetime.fromtimestamp(max(info.st_ctime,0))))
        files_data.sort(reverse=True, key=lambda x:x[1])

        for i in files_data:
            table.insert(parentID, 'end', values=i)


    def run(self):
        path = filedialog.askdirectory()
        if path == "":
            sys.exit()
        window = tk.Tk()
        window.geometry("750x500")
        window.title("DiskUsage")

        self.directory_icon = ImageTk.PhotoImage(self.directory_icon)

        columns = ("File", "Size", "Visual", "Date")
        table = ttk.Treeview(columns=columns)
        style = ttk.Style()
        style.configure("Treeview", indent=0)

        table.heading("File", text="File", anchor='w')
        table.heading("Size", text="Size MB", anchor='w')
        table.heading("Date", text="Date", anchor='w')
        table.heading("Visual", text="%", anchor='w')

        table.column("#0", width=40, minwidth=40, stretch=False)
        table.column("File", width=400)
        table.column("Size", width=100)
        table.column("Date", width=160)
        table.column("Visual", width=50)

        table.pack(fill='both', expand=1)
        table.tag_configure("custom_color", background="yellow")
        self.main_directory = Analizer.Analizer.analyze_directory(path)
        self.insert_directories(self.main_directory, table)

        window.mainloop()

DiskUsage().run()