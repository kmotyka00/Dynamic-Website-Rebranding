import re
import shutil
import os
import logging
from settings import LOGS_PATH, PROJECT_PATH, VALID_EXTENSIONS, CSS_COLOR_ATTRIBUTES, HTML_COLOR_ATTRIBUTES
from copy_manager import CopyManager, WindowsCopyManager
from pathlib import Path
from abc import ABC, abstractmethod
import fileinput
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

        style_reg = re.compile("style=")
        end_reg = re.compile(r'[\";]')
        
        for line in fileinput.input(self.path, inplace=True):

            style_match = style_reg.search(line)
            if style_match:

                for html_attribute in HTML_COLOR_ATTRIBUTES:
                    color_reg = re.compile(html_attribute + ":")
                    color_match = color_reg.search(line)
                    if color_match:
                        color_beg = color_match.span()[1] + 1
                        end_pos = end_reg.search(line[color_beg:]).span()[1] - 1

                        color = line[color_beg: color_beg + end_pos]

                        self.update_colors_variables(color)
                        line = self.replace_color_in_line(line, color)
                        
            print(line, end="")
                
    def update_colors_variables(self, color: str):
        if color not in self.colors_groups:
            self.colors_groups[color] = f'variable_{color}'
    
    def replace_color_in_line(self, line: str, color: str) -> str:

        return line.replace(color, self.colors_groups[color])

                
class CSSScrapper(FileScrapper):
    def __init__(self, colors_groups: dict, path: str) -> None:
        super().__init__(colors_groups, path)

    def scrap_file(self,) -> None:
        with open(self.path, 'r') as file:
            lines = file.readlines()
            line_number = 0
            while line_number < len(lines):
                words = lines[line_number].split(' ')
                for css_attribute in CSS_COLOR_ATTRIBUTES:
                    for i, word in enumerate(words):
                        if css_attribute in word and i < len(words):
                            lines[line_number] = self.find_var_return_line(words, i)           
                            print(lines[line_number])
                line_number +=1
        os.remove(self.path)
        with open(self.path, 'w') as file:
            file.writelines(lines)

        print(self.colors_groups)

    def find_var_return_line(self, words: list, index: int):
        #TODO convert to abstract method format 
        current_color = words[index + 1].split(';')[0]
        if not self.colors_groups.get(current_color):
            self.colors_groups[current_color] = f'variable_{current_color}'

        words[index+1] = self.colors_groups[current_color]
        return ' '.join(words) + ';\n'
