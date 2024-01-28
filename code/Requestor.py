from abc import ABC, abstractmethod
import requests
from fake_useragent import UserAgent
from loguru import logger


class Request(ABC):
    @abstractmethod
    def get_request(self):
        """
        Implement the method of obtaining http request here.
        """
        pass
    
    @abstractmethod
    def check_status(self):
        """
        This section defines how to check the data
        """
        pass
    
    def set_header_user_agent(self):
        user_agent = UserAgent()
        return user_agent.random

class II_Request(Request):
    """
    institutional investors request（三大法人當日買賣超）
    """
    def __init__(self, yyyymmdd: str):
        self.yyyymmdd = yyyymmdd
    
    def get_request(self):
        url = f'https://www.twse.com.tw/rwd/zh/fund/T86?date={self.yyyymmdd}&selectType=ALL&response=html'
        logger.info(f"Sending a request to the URL: {url}")
        headers = {"user-agent": self.set_header_user_agent()}
        re = requests.post(url, headers = headers)
        self.check_status(re)
        return re

    
    def check_status(self, re_object):
        logger.info(f"Request status code: {re_object.status_code}")
        if re_object.status_code != 200:
            raise Exception(f"Request failed with status code {re_object.status_code}")
        return re_object.status_code
    
        
        
