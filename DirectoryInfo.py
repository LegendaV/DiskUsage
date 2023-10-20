class DirectoryInfo:
    def __init__(self, path:str, ctime:int):
        self.path = path
        self.files_info = {}
        self.directories = []
        self.size = 0
        self.ctime = ctime
        self.child_dir = 0

    
    def add_file(self, file_name:str, file_stat):
        self.files_info[file_name] = file_stat
        self.size+=file_stat.st_size


    def add_directory(self, directory_info):
        if directory_info != None:
            self.directories.append(directory_info)
            self.size+=directory_info.size
            self.child_dir+=directory_info.child_dir+1


if __name__ == '__main__':
    pass