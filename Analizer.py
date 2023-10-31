import DirectoryInfo
import os, shutil
from progress.bar import IncrementalBar


class Analizer:
    def __init__(self):
        pass


    @staticmethod
    def analyze_directory(path:str, bar=None):
        try:
            directory_info = DirectoryInfo.DirectoryInfo(path, os.stat(path))
            files = os.scandir(path)
            os.chdir(path)
        except:
            return None
        for f in files:
            file_name = f.name
            if f.is_file():
                try:
                    directory_info.add_file(file_name, os.stat(f.name))
                    if bar!=None:
                        bar.next()
                finally:
                    continue
            directory_info.add_directory(Analizer.analyze_directory(f'{path}/{file_name}'))
            if bar!=None:
                bar.next()
            os.chdir(path)
        return directory_info


if __name__ == '__main__':
    pass