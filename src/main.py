from colors_scrapper import CSSScrapper, HTMLScrapper, Scrapper
from settings import VALID_EXTENSIONS
import os


def change_variable():
    pass

def scrap_file(file: str, colors_group: dict):
    extension = file.split('.')[1]
    file_scrapper = None
    if extension == 'html':
        file_scrapper = HTMLScrapper(scrapper.colors_groups, file)
        file_scrapper.link_css_variables()

    elif extension == 'css':
        file_scrapper = CSSScrapper(scrapper.colors_groups, file)
    
    elif extension == 'jsx':
        print("jsx not implemented yet")
        
    elif extension == 'js':
        print('js not implemented yet')

    if file_scrapper:
        colors_group = file_scrapper.scrap_file()

    return colors_group

if __name__ == '__main__':
    path: str = r'tests\\test_resources\\netflix_website'
    scrapper = Scrapper(source_path=path)
    """ FIRST SCRAP - GROUPING COLOURS INTO VARIABLES AND REPLACING IN THE FILES """
    scrapper.copy_manager.prettier()
    list_of_valid_files: list = []
    for file in scrapper.get_all_files():   
        # init all files that are considered
        if file.split('.')[1] in VALID_EXTENSIONS:
            list_of_valid_files.append(file)
            scrapper.colors_groups = scrap_file(file, scrapper.colors_groups)
    scrapper.create_css_variables_file()

