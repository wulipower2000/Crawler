import psutil
import sh

from loguru import logger
from typing import Dict
from typing import Union

class SystemUsage:
    """
    System usage monitor.
    """
    def __init__(self, pid: int, interval: int, unit: str="MB") -> None:
        """
        :param pid:
            - desc: process ID
        :param interval:
            - desc monitor time interval
        """
        self.pid = pid
        self.interval = interval
        self.process_info = psutil.Process(pid)
        self.unit = unit

    @logger.catch
    def get_cpu_percent(self) -> Dict[str, str]:
        """
        Function to monitor process cpu percentage.
        """
        
        logger.info("Start monitor cpu percentage.")
        cpu_percent = self.process_info.cpu_percent(interval=self.interval)
        return {"cpu_percent": cpu_percent}

    @logger.catch
    def get_memory_info(self) -> Dict[str, str]:
        """
        Function to monitor memory rss and vms.
        """
        mem_info = self.process_info.memory_info()._asdict()
        mem_rss = self.convert_bytes(
            data = mem_info.get("rss"), unit = self.unit
        )
        mem_vms = self.convert_bytes(
            data = mem_info.get("vms"), unit = self.unit
        )
        return {"memory_rss": mem_rss, "memory_vms": mem_vms}

    @logger.catch
    def get_folder_size(self, path: str) -> Dict[str, float]:
        """
        Function to get folder size.
        """
        logger.info(f"Start get folder size, path: {path}")
        folder_size, folder_path = sh.du("-s", path).splitlines()[0].split('\t')
        folder_size = self.convert_bytes(
            data = folder_size, unit = self.unit
        )
        
        return {"folder_size":folder_size, "folder_path": folder_path}

    @logger.catch
    def convert_bytes(self, data: Union[str, int, float], unit: str) -> float:
        """
        Convert data to input unit.
        """
        custom_format = lambda target: float(f"{target:.2f}")
        
        to_B  = lambda x: float(x)
        to_KB = lambda x: to_B(x)/1024
        to_MB = lambda x: to_KB(x)/1024
        to_GB = lambda x: to_MB(x)/1024
        to_TB = lambda x: to_GB(x)/1024

        converters = {
            "B" : to_B , "KB": to_KB,
            "MB": to_MB, "GB": to_GB,
            "TB": to_TB
        }
        
        converter = converters.get(unit)
        if converter == None:
            logger.warning(f"{unit} conversion not defined, convert data to B")
            return custom_format(to_B(data))
        else:
            return custom_format(converter(data))
