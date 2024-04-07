from sensors.data_handler import DataHandler
from utils.EDevices import EDevices

class SensorCore():

    def __init__(self, data_handler: DataHandler):
        self.__data_handler = data_handler

    def move_data(self):
        data = self.__data_handler.get_data()
        #sender.send_data(data)
        #flightMemory.set_position(data.get(EDevices.IMU))