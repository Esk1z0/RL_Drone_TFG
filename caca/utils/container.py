from utils.EDevices import EDevices

class Container():
    def __init__(self, dict = {}):
        if (len(dict) == 0):
            dict = {EDevices.IMU: [0, 0, 0]}
        self.__dict = dict

    def put(self, key, value):
        aux = {key, value}
        self.__dict.update(aux)

    def insert(self, data: dict):
        self.__dict.update(data)

    def pop(self):
        return self.__dict.pop()

    def get(self, key):
        return self.__dict.get(key)


    def putImu(self, imu):
        self.__dict[EDevices.IMU] = imu

    def getImu(self):
        return self.__dict[EDevices.IMU]