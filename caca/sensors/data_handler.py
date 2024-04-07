from utils.ibatch import IBatch

from sensors.data_gathering.idata_gather import IDataGather
from utils.EDevices import EDevices
from utils.timelib import TimeLib
from utils.container import Container
from typing import List

class DataHandler():
    def __init__(self, sensors: List[IDataGather]):
        self.__sensors = sensors

    def get_data(self) -> Container:
        data = Container()
        data.put(EDevices.TimeExtraction, TimeLib.getTimeStr())
        for sensor in self.__sensors:
            data.insert(sensor.get_data())
        return data




