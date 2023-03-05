from abc import ABC, abstractmethod
import os 
import logging

from settings import LOGS_PATH 


def make_os_operation(command: str, path_init: str, path_source: str, msg: str = 'Operation went wrong'):
    os.chdir(path_source)
    try:
        os.system(command)
    except:
        msg = "Instalation went wrong."
        logging.warning(msg)
        with open(LOGS_PATH, 'a') as file:
            file.write(f"Message: {msg}")
    finally:
        os.chdir(path_init)

class FolderManager(ABC):
    def __init__(self, folder_path: str, need_install: bool = True) -> None:
        self.folder_path = folder_path
        self.need_install = need_install
        self.cwd = os.getcwd()

    @abstractmethod
    def init_project() -> None:
        pass


class ReactFolderManager(FolderManager):
    def __init__(self, folder_path: str, need_install: bool = True) -> None:
        super().__init__(folder_path, need_install)

    def install_project(self,) -> None:
        make_os_operation("npm install", self.cwd, self.folder_path)

    def init_project(self,) -> None:
        if self.need_install:
            self.install_project()
        
        make_os_operation("npm start", self.cwd, self.folder_path)
       
    def close_project(self, port='3000') -> None:
        make_os_operation(f'npx kill-port {port}', self.cwd, self.folder_path)

class HTMLProjectManager(FolderManager):
    def __init__(self, folder_path: str, need_install: bool = True) -> None:
        super().__init__(folder_path, need_install)
    
    def init_project(self, html_name: str = 'index.html') -> None:
        make_os_operation(f'start {html_name}')