import sys

sys.path.append('../src')
import unittest
from color_names_creator import ColorNamesCreator
from colors_scrapper import Scrapper, FileScrapper, HTMLScrapper, CSSScrapper
from copy_manager import CopyManager, WindowsCopyManager
import os 
import shutil

class TestDirectoryCopy(unittest.TestCase):    
    # def test_linux_path(self):
    #     linux_path: str = '/home/seth/Pictures/penguin'
    #     copy_manager = CopyManager(linux_path)
    #     assert_val = 'penguin'
    #     ret_val = copy_manager.project_name
    #     self.assertEqual(ret_val, assert_val)

    def test_windows_path(self):
        windows_path: str = r'C:\\Documents\\Newsletters\\Summer\\beach'
        copy_manager = WindowsCopyManager(windows_path)
        assert_val = 'beach'
        ret_val = copy_manager.project_name
        self.assertEqual(ret_val, assert_val)

    def test_wrong_path(self):
        dummy_path: str = 'dummy'
        with self.assertRaises(ValueError) as cm:
            WindowsCopyManager(dummy_path)

        self.assertEqual(str(cm.exception), "Wrong source path.")

    def test_copy_files(self):
        path: str = r"\\test_resources\\dummy_folder"
        scrapper = Scrapper(WindowsCopyManager, path)
        
        ret_val = True
        directoriesCopied = os.listdir(scrapper.copy_manager.destination_path)
        directoriesOriginal = os.listdir(path)
       
        if set(directoriesOriginal) != set(directoriesCopied):
            ret_val = False

        self.assertEqual(ret_val, True)
        
        shutil.rmtree(scrapper.copy_manager.destination_path)

    def test_get_all_files(self):
        
        path: str = r'..\\tests\\test_resources\\dummy_folder'
        assert_val = set(['..\\projects\\dummy_folder\\component1\\component1.jsx', 
                          '..\\projects\\dummy_folder\\index.css', 
                          '..\\projects\\dummy_folder\\index.js'])
        scrapper = Scrapper(WindowsCopyManager, path)

        ret_val: set = set(scrapper.get_all_files())
        self.assertEqual(assert_val, ret_val)

        shutil.rmtree(scrapper.copy_manager.destination_path)


class TestHTMLScrapper(unittest.TestCase):

    def test_scrap_file(self):
        path: str = r'..\\tests\\test_resources\\netflix_website'
        scrapper = Scrapper(source_path=path)
        scrapper.copy_manager.prettier()
        html_scrapper = HTMLScrapper(scrapper.colors_groups, os.path.join(scrapper.copy_manager.destination_path, "index.html"))
        html_scrapper.scrap_file()

        shutil.rmtree(scrapper.copy_manager.destination_path)

class TestCSSScrapper(unittest.TestCase):
    def test_scrap_file(self,):
        path: str = r'..\\tests\\test_resources\\netflix_website'
        scrapper = Scrapper(source_path=path)
        css_scrapper = CSSScrapper(scrapper.colors_groups, os.path.join(scrapper.copy_manager.destination_path, 'netflixstyles.css'))
        scrapper.copy_manager.prettier()
        css_scrapper.scrap_file()
        print(css_scrapper.colors_groups)       

        shutil.rmtree(scrapper.copy_manager.destination_path)

class TestFileScrappers(unittest.TestCase):
    def test_create_css_file(self):
        path: str = r'..\\tests\\test_resources\\netflix_website'
        scrapper = Scrapper(source_path=path)
        css_scrapper = CSSScrapper(scrapper.colors_groups, os.path.join(scrapper.copy_manager.destination_path, 'netflixstyles.css'))
        scrapper.copy_manager.prettier()
        css_scrapper.scrap_file()
        html_scrapper = HTMLScrapper(scrapper.colors_groups, os.path.join(scrapper.copy_manager.destination_path, "index.html"))
        html_scrapper.scrap_file()

        scrapper.create_css_variables_file()
        shutil.rmtree(scrapper.copy_manager.destination_path)

class TestColorNamesCreator(unittest.TestCase):
    def test_hex_validation_is_hex(self):
        color = '0x23E5A1'

        color_names_creator = ColorNamesCreator()

        result = color_names_creator.validate_hex_color(color)
        self.assertTrue(result)
    
    def test_hex_validation_is_not_hex(self):
        color = 'blue'

        color_names_creator = ColorNamesCreator()

        result = color_names_creator.validate_hex_color(color)
        self.assertFalse(result)
    
    def test_hex_validation_is_almost_hex(self):
        color = '0x12345G'

        color_names_creator = ColorNamesCreator()

        result = color_names_creator.validate_hex_color(color)
        self.assertFalse(result)

    def test_truncate_color_name(self):
        color = '0x23E5A1'

        color_names_creator = ColorNamesCreator()
        result = color_names_creator.truncate_hex_name(color)
        self.assertEqual(result, "23E5A1")

    # def test_request_wrong_url(self):
    #     color = ''

    #     color_names_creator = ColorNamesCreator()

    #     with self.assertRaises(ValueError) as cm:
    #         result = color_names_creator.request_color_name(color)

    #     self.assertEqual(str(cm.exception), "Wrong response, status code: 400.")

    def test_request_color_name(self):
        color = '0xABCABC'

        color_names_creator = ColorNamesCreator()
        result = color_names_creator.request_color_name(color)
        self.assertEqual(result, "Opal")

    



if __name__ == "__main__":
    unittest.main()