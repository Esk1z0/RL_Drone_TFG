from sensors.data_gathering.idata_gather import IDataGather
from utils.EDevices import EDevices
from controller import InertialUnit
from time import sleep


class IMUGather(IDataGather):

    def __init__(self, device: InertialUnit):
        self.__imu = device

    def get_data(self):
        data = self.__get_data()
        return {EDevices.IMU : data}

    def __get_gyro(self):
        return self.__imu.getRollPitchYaw()

