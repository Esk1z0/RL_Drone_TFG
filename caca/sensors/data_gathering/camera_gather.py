from sensors.data_gathering.idata_gather import IDataGather
from controller import Camera
from utils.EDevices import EDevices

class CameraGather(IDataGather):

    def __init__(self, device: Camera):
        self.__camera = device

    def get_data(self):
        data = self.__get_image()
        return {EDevices.Camera : data}

    def __get_image(self):
        image = self.__camera.getImage()
        return image
