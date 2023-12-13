from typing import Union
import os
from abc import ABC, abstractmethod
from loguru import logger
import datetime
import pandas as pd
from sqlalchemy import create_engine

class Sink(ABC):
    @abstractmethod
    def sink(self):
        pass

    @abstractmethod
    def dest_exist(self):
        pass

class psql(Sink):
    def __init__(self,
           host: str, port: int, user: str,
           password: str, database: str):
        """
        :param host:
            - desc: postgresql hosanme or ip address.
        :param port:
            - desc: postgresql port number.
        :param user:
            - desc: user name.
        :param password:
            - desc: password for user.
        :param database:
            - desc: database in postgresql.
        """

        self.engine = self._connect_psql(
            host, port, user, password, database)

    @logger.catch()
    def _connect_psql(self,
            host: str, port: int, user: str,
            password: str, database: str):
        """
        Function to create postgresql engine.
        :param host:
            - desc: postgresql hosanme or ip address.
        :param port:
            - desc: postgresql port number.
        :param user:
            - desc: user name.
        :param password:
            - desc: password for user.
        :param database:
            - desc: database in postgresql.
        """
        
        connect_string = \
            f"postgresql://{user}:{password}@" + \
            f"{host}:{port}/{database}"

        logger.info(f"Connect postgresql.")
        return create_engine(connect_string)

    def _is_connect(self):
        """
        Function to check postgresql connection.
        """
        return self.engine.connect()

    def dest_exist(self):
        logger.info("Check if is connect psql.")
        return self._is_connect()

    def close(self):
        """
        Function to close psql connection.
        """
        logger.info("Close psql connection.")
        self.engine.dispose()

    @logger.catch()
    def sink(self, data: pd.DataFrame, table: str, if_exists='replace') -> None:
        """
        :param data:
            - desc: Input data.
        :param table:
            - desc: Table name.
        :patam if_exists:
            - desc: Action for if table exist.
        """
        if self.dest_exist():
            logger.info("Connect psql success.")
            logger.info(f"Try to write data into table: {table}.")
            data.to_sql(
                table, self.engine, 
                if_exists=if_exists,
                index=True
            )
            self.close()
        else:
            logger.error("Connect sql failed")

class csv(Sink):

    @logger.catch()
    def sink(self, data: pd.DataFrame, path: str) -> None:
        """
        :param data:
            - desc: Input data.
        :param path:
            - desc: Path to output data.
        """
        self.dest_exist(path)
        logger.info("Start writing data")
        data.to_csv(path)
        logger.info("Data writing completed")

    @logger.catch()
    def dest_exist(self, path: str) -> None:
        """
        Check if the destination directory exists.
        :param path:
            - desc: output data path
        """

        data_dir = os.path.dirname(path) # Get directory path of output

        logger.info("Check data directory exist.")
        logger.info(f"Data directory is: {data_dir}")

        # Check if the directory exists
        if os.path.isdir(data_dir):
            logger.info(f"{data_dir} exist.")
        else:
            # if dir not exist, create dir
            logger.warning(f"{data_dir}: not exist.")
            logger.warning(f"Create data directory")
            os.makedirs(data_dir)
            logger.info(f"Directory is Created!")

