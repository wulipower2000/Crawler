from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
import pandas as pd
from loguru import logger

class Parser(ABC):
    @abstractmethod
    def parse_html_to_dataframe(self):
        pass
    
    @logger.catch
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
    
    @logger.catch
    def parse_html_to_dataframe(self):
        logger.info("Parsing HTML to DataFrame")
        self.re.encoding = 'utf-8'
        df_total = pd.read_html(str(BeautifulSoup(self.re.text, 'html.parser')))[0]
        df = df_total.set_index(df_total.columns[0])
        self.check_data(df)
        return df
    
    @logger.catch
    def check_data(self, data):
        logger.info(f'data shape: {data.shape}')
        super().check_data(data)
