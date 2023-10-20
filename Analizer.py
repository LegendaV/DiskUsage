import DirectoryInfo
import os, shutil


class Analizer:
    def __init__(self):
        pass


    @staticmethod
    def analyze_directory(path:str):
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
                finally:
                    continue
            directory_info.add_directory(Analizer.analyze_directory(f'{path}/{file_name}'))
            os.chdir(path)
        return directory_info


if __name__ == '__main__':
    pass