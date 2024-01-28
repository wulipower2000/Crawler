from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
from io import StringIO

import pandas as pd

from loguru import logger
from typing import Union

import bs4

class GetNoDataException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class Parser(ABC):
    @abstractmethod
    def parse_html_to_dataframe(self):
        pass
    
    @abstractmethod
    def check_data(self, data):
        """
        父類別中的檢查資料邏輯，對所有子類別通用
        """
        if not isinstance(data, pd.DataFrame):
            raise ValueError("Data must be a pandas DataFrame")
        if data.empty:
            logger.warning("Empty DataFrame")
        

class II_Parser(Parser):
    """
    Institutional investor parser
    """
    def __init__(self, re):
        self.re = re
    
    def parse_html_to_dataframe(self):
        logger.info("Parsing HTML to DataFrame")
        self.re.encoding = 'utf-8'

        parser_html_to_soup = lambda data: BeautifulSoup(data, 'html.parser').find('table')
        parser_soup_to_string = lambda data: StringIO(str(data))

        table_soup = parser_html_to_soup(self.re.text)
        self._check_soup(table_soup)

        df_total = pd.read_html(parser_soup_to_string(table_soup))[0]
        df = df_total.set_index(df_total.columns[0])
        
        return df

    def _check_soup(self, soup: bs4.element.Tag) -> None:
        if soup == None:
            raise GetNoDataException("Can not parser data from API by bs4.")
    
    def check_data(self, data):
        logger.info(f'data shape: {data.shape}')
        super().check_data(data)
