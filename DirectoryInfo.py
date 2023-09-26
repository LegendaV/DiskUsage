class DirectoryInfo:
    def __init__(self, path:str):
        self.path = path
        self.files_info = []
        self.directories = []
        self.size = 0


    def append_file(self, file_stat):
        self.files_info.append(file_stat)
        self.size+=file_stat.st_size
