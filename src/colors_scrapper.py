import re
import shutil
import os
import logging
from settings import LOGS_PATH, PROJECT_PATH, VALID_EXTENSIONS, CSS_COLOR_ATRIBUTES
from copy_manager import CopyManager, WindowsCopyManager
from pathlib import Path
from abc import ABC, abstractmethod
# ścieżka do folderu
# lista atrybutów których szukamy: colors, background-color...
# 


class Scrapper:
    def __init__(self, copy_manager: CopyManager = WindowsCopyManager, source_path: str = None ):
        self.copy_manager = copy_manager(source_path)
        self.colors_groups = dict()
        self.all_files = self.get_all_files()

    def create_css_variables_file(self, ):
        #TODO
        return None

    def get_all_files(self) -> list:
        p = Path(self.copy_manager.destination_path).glob('**/*')
        all_files = [str(x) for x in p if x.is_file()]
        return filter(self.valid_files, all_files)

    @staticmethod
    def valid_files(path):
        if path.split('.')[-1] in VALID_EXTENSIONS:
            return True
        else:
            return False

class FileScrapper(ABC):
    def __init__(self, colors_groups: dict, path: str) -> None:
        self.colors_groups = colors_groups
        self.path = path
    
    @abstractmethod
    def scrap_file() -> None:
        pass
    
    @staticmethod
    def convert_color_name(color_name: str) -> str:
        pass

class HTMLScrapper(FileScrapper):
    def __init__(self, colors_groups: dict, path: str) -> None:
        super().__init__(colors_groups, path)

    def scrap_file(self):
        with open(self.path, 'r+') as f:
            style_reg = re.compile("style=")
            color_reg = re.compile("color:")
            end_reg = re.compile("")
            while True:
                line = f.readline()
                
                if not line:
                    break
                
                style_pos = style_reg.search(line)
                if style_pos:
                    style_pos = style_pos.span()[0]

                    color_pos = color_reg.search(line[style_pos:])
                    if color_pos:
                        color_beg = color_pos.span()[1]
                        print(color_pos.string[color_beg:])

                
class CSSScrapper(FileScrapper):
    def __init__(self, colors_groups: dict, path: str) -> None:
        super().__init__(colors_groups, path)

    def scrap_file(self,) -> None:
        with open(self.path, 'r+') as file:
            while True:
                line = file.readline()
                if not line:
                    break
                words = line.split(' ')
                # print(words)
                for css_atribute in CSS_COLOR_ATRIBUTES:
                    for i, word in enumerate(words):
                        if css_atribute in word:
                            print("IM IN")
                            print(words)

                            if self.colors_groups.get(words[i+1]):
                                #replace with css variable
                                words[i+1] = self.colors_groups[words[i+1]]
                            else:
                                #create CSS Variable
                                # self.co
                                self.colors_groups[words[i+1]] = f'variable_{words[i+1]}'
        print(self.colors_groups)