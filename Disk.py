import DirectoryInfo
import os, shutil


class Analizer:
    def __init__(self):
        pass


    @staticmethod
    def analyze_directory(path:str):
        directory_info = DirectoryInfo.DirectoryInfo(path)
        files = os.listdir(path)
        os.chdir(path)
        for f in files:
            if os.path.isfile(f):
                directory_info.append_file(os.stat(f))
                continue
            directory_info.directories.append(Analizer.analyze_directory(f'{path}/{f}'))
            os.chdir(path)
        return directory_info


    @staticmethod
    def analyze_segment(path:str):
        files = Analizer.analyze_directory(path)
        return files
