from decision.Conexion.server_comunnication import ServerCommunication
from utils.timelib import TimeLib
from utils.EData import EData

class Receiver:
    def __init__(self, server_udp: ServerCommunication, server_tcp: ServerCommunication):
        self.server_tcp = server_tcp
        self.server_udp = server_udp

    def receive(self):
        return {EData.DATA_RECEIVED : 1}