from sensors.data_gathering.idata_gather import IDataGather
from controller import DistanceSensor
from time import sleep
from utils.EDevices import EDevices


class DistanceGather(IDataGather):


    def __init__(self, device: DistanceSensor):
        self.__device = device

    def get_data(self):
        data = self.__get_data()
        return {EDevices.DistanceSenso: data}

    def __get_data(self):
        return self.__device.getValue()