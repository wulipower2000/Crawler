import os

from abc import abstractmethod
from loguru import logger


class Sink:
    
    @abstractmethod
    def check(self):
        """
        Method to check output folder exist
        """
        pass

    @abstractmethod
    def output(self):
        """
        Method to output data 
        """
        pass


class TextSink(Sink):

    def __init__(self, path: str) -> None:
        self.path = path

    @logger.catch
    def check(self) -> None:
         
        if os.path.isdir(self.path):
            logger.info(f"Input folder {self.path} is exist")
        else:
            logger.warning(f"Input folder {self.path} is not exist")
            logger.warning(f"Create folder: {self.path}")
            os.makedirs(self.path)
    
    def output(self, file_name: str, data: str) -> None:
        with open(f"{self.path}/{file_name}", 'a') as file_obj:
            file_obj.write(data)



