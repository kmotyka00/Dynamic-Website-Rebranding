import sys
sys.path.append('../src')
import unittest
from colors_scrapper import Scrapper
import os 
import shutil

class TestDirectoryCopy(unittest.TestCase):    
    def test_linux_path_test(self):
        linux_path: str = '/home/seth/Pictures/penguin'
        scrapper = Scrapper(linux_path)
        assert_val = 'penguin'
        ret_val = scrapper.project_name
        self.assertEqual(ret_val, assert_val)

    def test_windows_path_test(self):
        windows_path: str = r'C:\\Documents\\Newsletters\\Summer\\beach'
        scrapper = Scrapper(windows_path)
        assert_val = 'beach'
        ret_val = scrapper.project_name
        self.assertEqual(ret_val, assert_val)

    def test_wrong_path(self):
        dummy_path: str = 'dummy'
        with self.assertRaises(ValueError) as cm:
            Scrapper(dummy_path)

        self.assertEqual(str(cm.exception), "Wrong source path.")

    def test_copy_files(self):
        path: str = r"..\\tests\\test_resources\\dummy_folder"
        scrapper = Scrapper(path)
        
        ret_val = True
        directoriesCopied = os.listdir(scrapper.destination_path)
        directoriesOriginal = os.listdir(path)
       
        if set(directoriesOriginal) != set(directoriesCopied):
            ret_val = False

        self.assertEqual(ret_val, True)

        shutil.rmtree(scrapper.destination_path)
    # def test_make_directory(self):
    #     windows_path: str = r'C:\\Documents\\Newsletters\\Summer\\coastline'
    #     scrapper = colors_scrapper.Scrapper(windows_path)
    #     assert_val = os.
    #     ret_val = scrapper.project_name

    

if __name__ == "__main__":
    unittest.main()