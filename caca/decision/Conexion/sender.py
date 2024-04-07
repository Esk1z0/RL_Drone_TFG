from decision.Conexion.server_comunnication import ServerCommunication
from utils.timelib import TimeLib
from utils.EDevices import EDevices

class Sender:
    def __init__(self, server_udp: ServerCommunication, server_tcp: ServerCommunication):
        self.server_tcp = server_tcp
        self.server_udp = server_udp

    def send(self, data):
        udp_data, tcp_data = self.__prepare_data(data)
        self.__send_udp(udp_data)
        self.__send_tcp(tcp_data)

    def __prepare_data(self, data):
        udp_data, tcp_data = self.__split_message(data)
        self.__add_time(udp_data)
        self.__add_time(tcp_data)
        return udp_data, tcp_data

    def __split_message(self, data: dict):
        keys_to_extract = [EDevices.IMU]
        imu_data = {key: data[key] for key in keys_to_extract}

        for key in keys_to_extract:
            data.pop(key)

        return imu_data, data

    def __add_time(self, data: dict):
        current_time = TimeLib.getTimeStr()
        data.update(EDevices.TimeSend, current_time)

    def __send_tcp(self, data_tcp):
        try:
            self.server_tcp.send_message(data_tcp)
            print("Message sent successfully tcp")
        except Exception as e:
            print("Error sending message tcp:", e)

    def __send_udp(self, data_udp):
        try:
            self.server_udp.send_message(data_udp)
            print("Message sent successfully udp")
        except Exception as e:
            print("Error sending message udp:", e)

    def __del__(self):
        self.server_tcp.close_connection()
        self.server_udp.close_connection()