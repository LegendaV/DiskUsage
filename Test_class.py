import unittest
import os
import tempfile
import Analizer
import random

class DirectoryMaker:
    def __init__(self):
        self.root_directory = tempfile.TemporaryDirectory()
        self.size = 0
        self.files = []
        for i in range(3):
            f = open(os.path.join(self.root_directory.name, f"test_file{i+1}.txt"), "wb")
            file_size = random.randint(10, 50)
            self.size += file_size
            random_bytes = bytearray(random.getrandbits(8) for _ in range(file_size))
            f.write(random_bytes)

    
    def __del__(self):
        self.root_directory.cleanup()


class AnalizerTest(unittest.TestCase):
    def test_analizer(self):
        test_directory = DirectoryMaker()
        directory_info = Analizer.Analizer.analyze_directory(test_directory.root_directory.name)
        self.assertAlmostEqual(directory_info.size, test_directory.size, 1)


if __name__ == '__main__':
    unittest.main()