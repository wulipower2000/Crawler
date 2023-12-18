import os
import threading
import datetime

from application_monitor.ConfigParser import JsonConfigParser as ConfigParser
#from application_monitor.Sink import TextSink as Sink
from application_monitor.Sink import PrometheusSink as Sink
from application_monitor.Monitor import SystemUsage as Exporter
from application_monitor.CustomException import FieldNotFoundError

from loguru import logger
from pprint import pprint
from typing import Callable

import pdb

class ProcessExporter:
    def __init__(self, pid: int, config_path: str, func_name: str) -> None:
        logger.info("Start monitor process info")
        logger.info("Parser configuration")
        config_parser = ConfigParser(config_path)
        config_parser.check()
        self.config = config_parser.load()

        self._stop_loop: bool = False
        self.pid: int = pid
        self.func_name:str = func_name

        self.registered_exporter = list()
        self.exporter = Exporter(pid, self.config.get("interval"))
        self.exporters = {
            "cpu_percent": self.exporter.get_cpu_percent,
            "memory_info":self.exporter.get_memory_info,
            "folder_size":self.get_folder_size_modify
        }

        self.register("cpu_percent")
        self.register("memory_info")
        monitors = self.config.get("monitors")
        
        for monitor in monitors:
            self.register(monitor)

        self.sink = Sink(self.config)
        self.sink.check()

    @logger.catch
    def register(self, target: str) -> None:
        logger.info(f"Register exporter of {target}")
        func = self.exporters.get(target)
        if func == None:
            raise KeyError(f"Can not found input monitor target: {target} in all exporters")
        else:
            self.registered_exporter.append(func)

    @logger.catch
    def get_folder_size_modify(self):
        folder_path = self.config.get("folder_path")
        if folder_path == None: 
            raise FieldNotFoundError(f"Can not folder_path in config, please set folder_path before monitor folder size")

        if os.path.exists(folder_path):
            return self.exporter.get_folder_size(folder_path)
        else:
            raise FileNotFoundError(f"folder_path: {folder_path} not found.")
    
    def stop(self) -> None:
        self._stop_loop = True

    @logger.catch
    def start(self) -> None:
        logger.info("Start get process information")
        while True:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            result = {"pid": self.pid, "function_name": self.func_name, "timestamp":timestamp}
            for func in self.registered_exporter:
                result = {**result, **func()}
            self.sink.output(result)
            if self._stop_loop: break

@logger.catch
def test_daemon():

    pid = os.getpid()
    pe = ProcessExporter(pid=pid, config_path="./config.json", func_name=test_daemon.__name__)

    daemon = threading.Thread(
        target=pe.start, daemon=True
    )

    daemon.start()
    total: int = 0
    for x in range(100_000_000_000):
        total += x

    pe.stop()
    daemon.join()

@logger.catch
def test():

    pid = os.getpid()
    pe = ProcessExporter(pid=pid, conf_path="./config.json")
    pe.start()
    pe.stop()

def doctor(config_path: str) -> Callable:
    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            pid = os.getpid()
            process_exporter = ProcessExporter(
                pid = pid,
                config_path = config_path,
                func_name = func.__name__
            )
            daemon = threading.Thread(
                target = process_exporter.start, daemon=True
            )
            daemon.start()

            result = func(*args, **kwargs)

            process_exporter.stop()
            daemon.join()
            return result
        return wrapper
    return decorator

@logger.catch
@doctor("./application_monitor/monitor_prometheus.json")
def test_decortor():

    total: int = 0
    for x in range(100_000_000_000_000): total += x

if __name__ == "__main__":
    
    test_decortor()
