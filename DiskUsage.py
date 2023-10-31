import sys
import Analizer
import os
import platform
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from datetime import datetime
from PIL import ImageTk, Image
from progress.bar import IncrementalBar

sids = {}
def get_owner_name(file_path, st_uid):
    global sids

    if platform.system() == 'Windows':
        import win32security
        sid = win32security.GetFileSecurity(file_path, win32security.OWNER_SECURITY_INFORMATION).GetSecurityDescriptorOwner()
        str_sid = str(sid)
        if not(str_sid in sids):
            sids[str_sid] = win32security.LookupAccountSid(None, sid)[0]
        return sids[str_sid]
    else:
        import pwd
        return pwd.getpwuid(st_uid).pw_name


class DiskUsage:
    def __init__(self):
        self.directory_icon = Image.open(f'Images{os.path.sep}directory_icon.png').resize((15, 15), Image.ANTIALIAS)


    def sort_column(treeview:ttk.Treeview, col:int, reverse:bool):
            l = [(treeview.set(k, col), k) for k in treeview.get_children("")]
            l.sort(reverse=reverse)
            for index,  (_, k) in enumerate(l):
                treeview.move(k, "", index)
            treeview.heading(col, command=lambda: DiskUsage.sort_column(treeview, col, not reverse))


    def insert_directories(self, directory_info, table, parentID="", space_count=0):
        directories = directory_info.directories
        directories.sort(reverse=True, key=lambda d:d.size)
        for d in directories:
            info = ('-' * space_count + os.path.basename(d.path),#Filename
                    get_owner_name(d.path, d.file_stat),#Owner
                    round(d.size / 2**20, 5),#Size
                    round(d.size/self.main_directory.size, 2) * 100,#%
                    datetime.fromtimestamp(max(d.ctime,0)),#Date
                    d.child_dir)#Child_dir
            directoryID = table.insert(parentID, 'end', values=info, tags=("custom_color",), image=self.directory_icon)
            self.insert_directories(d, table, directoryID, space_count+1)

        files_data = []
        for f in directory_info.files_info:
            info = directory_info.files_info[f]
            files_data.append(('-' * space_count + f,
                               get_owner_name(os.path.join(directory_info.path, f), info.st_uid),
                               round(info.st_size / 2**20, 5), 
                               round(info.st_size/self.main_directory.size, 2) * 100,
                               datetime.fromtimestamp(max(info.st_ctime,0)),
                              ''))
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

        columns = ("File", "Owner", "Size", "Visual", "Date", "Child_dir")
        table = ttk.Treeview(columns=columns)
        style = ttk.Style()
        style.configure("Treeview", indent=0)

        table.heading("File", text="File", anchor='w', command=lambda: DiskUsage.sort_column(table, columns.index("File"), False))
        table.heading("Owner", text="Owner", anchor='w', command=lambda: DiskUsage.sort_column(table, columns.index("Owner"), False))
        table.heading("Size", text="Size MB", anchor='w', command=lambda: DiskUsage.sort_column(table, columns.index("Size"), False))
        table.heading("Date", text="Date", anchor='w', command=lambda: DiskUsage.sort_column(table, columns.index("Date"), False))
        table.heading("Visual", text="%", anchor='w', command=lambda: DiskUsage.sort_column(table, columns.index("Visual"), False))
        table.heading("Child_dir", text="Dir", anchor='w', command=lambda: DiskUsage.sort_column(table, columns.index("Child_dir"), False))

        table.column("#0", width=40, minwidth=40, stretch=False)
        table.column("File", width=200)
        table.column("Owner", width=100)
        table.column("Size", width=100)
        table.column("Date", width=160)
        table.column("Visual", width=50)
        table.column("Child_dir", width=50)

        table.pack(fill='both', expand=1)
        table.tag_configure("custom_color", background="yellow")

        bar = IncrementalBar('Countdown', max = len(os.listdir(path)))
        self.main_directory = Analizer.Analizer.analyze_directory(path, bar=bar)
        bar.finish()
        self.insert_directories(self.main_directory, table)

        window.mainloop()

DiskUsage().run()