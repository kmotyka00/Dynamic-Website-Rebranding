from abc import ABC, abstractmethod
import shutil
import logging
import os
from settings import LOGS_PATH, PROJECT_PATH


class CopyManager(ABC):
    def __init__(self, source_path: str) -> None:
        self.project_name = self.create_project_name(source_path)
        self.destination_path = os.path.join(PROJECT_PATH, self.project_name)
        self.copy_source_code(source_path)

    def prettier(self):
        init_cwd = os.getcwd()
        os.chdir(self.destination_path)
        # TODO: Make try expect work (connection between cmd and our code)
        try:
            os.system("npx prettier --write .")
        except:
            # TODO: Print info for the user in application
            msg = "Wrong Source Code, page will not load."
            logging.warning(msg)
            with open(LOGS_PATH, 'a') as file:
                file.write(f"Message: {msg}")
        finally:
            os.chdir(init_cwd)

    @abstractmethod
    def copy_source_code(self, source_path: str) -> None:
        pass
    
    @abstractmethod
    def create_project_name(self, source_path: str) -> str:
        pass

class WindowsCopyManager(CopyManager):
    def __init__(self, source_path: str) -> None:
        super().__init__(source_path)
        
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

        if len(source_path.split(r"\\")) > 1:

            project_name = source_path.split(r"\\")[-1]
        else:
            raise ValueError("Wrong source path.")
        
        return project_name
    
    