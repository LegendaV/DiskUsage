from audioop import reverse
import Analizer
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from datetime import datetime


class DiskUsage:
    def __init__(self):
        pass


    def insert_directories(self, directory_info, table, parentID="", space_count=0):
        directories = directory_info.directories
        directories.sort(reverse=True, key=lambda d:d.size)
        for d in directories:
            info = ('-' * space_count + os.path.basename(d.path), round(d.size / 2**20, 5), datetime.fromtimestamp(d.ctime))
            directoryID = table.insert(parentID, 'end', values=info)
            self.insert_directories(d, table, directoryID, space_count+1)

        files_data = []
        for f in directory_info.files_info:
            info = directory_info.files_info[f]
            files_data.append(('-' * space_count + f, round(info.st_size / 2**20, 5), datetime.fromtimestamp(info.st_ctime)))
        files_data.sort(reverse=True, key=lambda x:x[1])

        for i in files_data:
            table.insert(parentID, 'end', values=i)


    def run(self):
        path = filedialog.askdirectory()
        window = tk.Tk()
        window.geometry("700x500")
        window.title("DiskUsage")

        columns = ("File", "Size", "Date")
        table = ttk.Treeview(columns=columns, show='headings')

        table.heading("File", text="File", anchor='w')
        table.heading("Size", text="Size MB", anchor='w')
        table.heading("Date", text="Date", anchor='w')

        table.column("File", width=400)
        table.column("Size", width=100)
        table.column("Date", width=200)

        table.pack(fill='both', expand=1)
        main_directory = Analizer.Analizer.analyze_directory(path)
        self.insert_directories(main_directory, table)

        window.mainloop()


DiskUsage().run()