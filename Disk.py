from msilib.schema import Directory
import os, shutil


class Analizer:
    def __init__(self):
        pass


    @staticmethod
    def analyze_directory(path:str):
        files = os.listdir(path)
        os.chdir(path)
        files_info = []
        for f in files:
            if os.path.isfile(f):
                files_info.append(os.stat(f))
                continue
            files_info.append(Analizer.analyze_directory(f'{path}/{f}'))
            os.chdir(path)
        return files_info
    

    @staticmethod
    def parse(directory_data:list):
        for directory in directory_data:
            if type(directory) == list:
                continue
            


    @staticmethod
    def analyze_segment(path:str):
        files = Analizer.analyze_directory(path)
        return files

a = Analizer.analyze_segment("C://Projects")
print(a)
while (True):
    pass