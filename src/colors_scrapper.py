import re
import shutil
import os
import logging
from settings import CSS_VARIABLES_FILENAME, LOGS_PATH, PROJECT_PATH, VALID_EXTENSIONS, CSS_COLOR_ATTRIBUTES, HTML_COLOR_ATTRIBUTES
from copy_manager import CopyManager, WindowsCopyManager
from pathlib import Path
from abc import ABC, abstractmethod
import fileinput

class Scrapper:
    def __init__(self, copy_manager: CopyManager = WindowsCopyManager, source_path: str = None ):
        self.copy_manager = copy_manager(source_path)
        self.colors_groups = dict()
        self.all_files = self.get_all_files()

    def create_css_variables_file(self) -> None:
        with open(os.path.join(self.copy_manager.destination_path, CSS_VARIABLES_FILENAME), 'w') as file:
            file.write(":root{")
            for key, value in self.colors_groups.items():
                file.write('\t' + key + ': ' + value + ';\n')
            file.write("}")

    def get_all_files(self) -> list:
        p = Path(self.copy_manager.destination_path).glob('**/*')
        all_files = [str(x) for x in p if x.is_file()]
        return filter(self.valid_files, all_files)

    def change_color(self, color_key: str, color_new_value: str) -> None:
        self.colors_groups[color_key] = color_new_value
        self.update_css_variable(color_key, color_new_value)

        # Here we need to reload page!

    def update_css_variable(self, color_key: str, color_new_value: str) -> None:
        search_value: str = color_key + ":"
        for line in fileinput.input(os.path.join(self.copy_manager.destination_path, CSS_VARIABLES_FILENAME), inplace=True):
            if search_value in line:
                line = "\t" + color_key + ": " + color_new_value + ";\n"
            
            print(line, end="")

    @staticmethod
    def valid_files(path):
        if path.split('.')[-1] in VALID_EXTENSIONS:
            return True
        else:
            return False

class FileScrapper(ABC):
    color_counter = 0
    def __init__(self, colors_groups: dict, path: str) -> None:
        self.colors_groups = colors_groups
        self.path = path
        

    def update_colors_variables(self, color: str):
        if color not in self.colors_groups.values():
            self.colors_groups[f'--variable_{FileScrapper.color_counter}'] = color
            FileScrapper.color_counter += 1

    def replace_color_in_line(self, line: str, color: str) -> str:
        for key, value in self.colors_groups.items():
            if value == color:
                return line.replace(color, f"var({key})")

    @abstractmethod
    def scrap_file() -> None:
        pass
    
    @staticmethod
    def convert_color_name(color_name: str) -> str:
        pass

class HTMLScrapper(FileScrapper):
    def __init__(self, colors_groups: dict, path: str) -> None:
        super().__init__(colors_groups, path)

    @staticmethod
    def valid_html_files(path):
        if path.split('.')[-1] == 'html':
            return True
        else:
            return False

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
    
    def link_css_variables(self) -> None:

        head_flag = False
        for line in fileinput.input(os.path.normpath(self.path), inplace=True):
            words = line.split(' ')
            for word in words:
                if word == '<head>' or word == '<head>\n':
                    head_flag = True
            print(line, end="")
            if head_flag:
                print(f'<link rel="stylesheet" type="text/css" href={CSS_VARIABLES_FILENAME}/>\n')
                head_flag = False

class CSSScrapper(FileScrapper):
    def __init__(self, colors_groups: dict, path: str) -> None:
        super().__init__(colors_groups, path)

    def scrap_file(self,) -> None:
        import_flag = True
        for line in fileinput.input(self.path, inplace=True):
            if import_flag:
                print(f'@import "{CSS_VARIABLES_FILENAME}";\n')
                import_flag = False
            words = line.split(' ')
            for css_attribute in CSS_COLOR_ATTRIBUTES:
                for i, word in enumerate(words):
                    if css_attribute == word and i < len(words):
                        color = words[i + 1].split(';')[0]
                        self.update_colors_variables(color)
                        line = self.replace_color_in_line(line, color) 
            print(line, end="")

