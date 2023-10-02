class DirectoryInfo:
    def __init__(self, path:str, ctime:int):
        self.path = path
        self.files_info = {}
        self.directories = []
        self.size = 0
        self.ctime = ctime

    
    def add_file(self, file_name:str, file_stat):
        self.files_info[file_name] = file_stat
        self.size+=file_stat.st_size


    def add_directory(self, directory_info):
        if directory_info != None:
            self.directories.append(directory_info)
            self.size+=directory_info.size


if __name__ == '__main__':
    pass