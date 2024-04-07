
class MemoryDecoder:

    def __init__(self, commands: dict):
        self.__commands = commands

    def decode(self, data):
        #esto no está hecho ni nada
        if data in self.__commands.keys():
            return self.__commands[data]
        else:
            return None