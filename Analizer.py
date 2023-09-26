import DirectoryInfo
import os, shutil


class Analizer:
    def __init__(self):
        pass


    @staticmethod
    def analyze_directory(path:str):
        directory_info = DirectoryInfo.DirectoryInfo(path, os.stat(path).st_ctime)
        files = os.listdir(path)
        os.chdir(path)
        for f in files:
            if os.path.isfile(f):
                directory_info.add_file(f, os.stat(f))
                continue
            directory_info.add_directory(Analizer.analyze_directory(f'{path}/{f}'))
            os.chdir(path)
        return directory_info


if __name__ == '__main__':
    pass