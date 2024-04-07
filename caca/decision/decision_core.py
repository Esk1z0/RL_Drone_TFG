from .Comander import Comander
from .memory.memory import Memory
from .Conexion.receiver import Receiver
from utils.container import Container
from threading import Thread


class DecisionCore():

    def __init__(self, memory: Memory, comander: Comander, receiver: Receiver, actuatorCore, signaling, security):
        self.__mem = memory
        self.__comander = comander#falta
        self.__receiver = receiver
        self.__actuatorCore = actuatorCore#falta
        self.__secureSignaling = signaling#falta
        self.__security = security#falta

        self.__thread = Thread(target=self.run())
        self.__thread.start()



    def run(self):
        while(True):#not signaling.EndProgram
            command = self.get_data()
            command = self.__mem.decode_command(command)
            self.__comander.set_command(command)
            while (self.__comander.theresOrder() or False):#not signaling.endWhile
                order = self.__comander.get_order()
                self.__actuatorCore.order(order)


    def get_data(self):
        if (True):  # not signaling.ProblemExists
            return self.__receiver.receive()
        else:
            return self.__security.receive()


