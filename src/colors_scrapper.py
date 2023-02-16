import re
import shutil
import os
import logging
# ścieżka do folderu
# lista atrybutów których szukamy: colors, background-color...
# 

PROJECT_PATH = '../projects/'
LOGS_PATH = '../logs/logs.txt'

class Scrapper:
    def __init__(self, source_path: str = None):
        self.project_name = self.create_project_name(source_path)
        self.colors_groups = dict()
        self.destination_path = PROJECT_PATH + self.project_name
        self.copy_source_code(source_path)
        
        
    # TODO: if there is no project_name, then create one from source_path
    def copy_source_code(self, source_path: str) -> None:
        # TODO: implement linux version
       
        try:
            shutil.copytree(source_path, self.destination_path)

        except FileNotFoundError as e:
            logging.warning("Wrong Path, copy operation failed")
            with open(LOGS_PATH, 'a') as file:
                #TODO add time, issue etc. 
                file.write(f"Message: {str(e)} \n")

    def create_project_name(self, source_path: str):

        #TODO make it prettier
        if len(source_path.split("/")) > 1:         
            project_name = source_path.split("/")[-1]
        elif len(source_path.split(r"\\")) > 1:
            project_name = source_path.split(r"\\")[-1]
        else:
            raise ValueError("Wrong source path.")
        
        return project_name


    
