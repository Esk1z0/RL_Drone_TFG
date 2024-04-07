class Comander():

    def __init__(self):
        self.__command = []

    def set_command(self, command = []):
        self.__command = command

    def get_order(self):
        if(len(self.__command) == 0):
            return -1
        else:
            return self.__command.pop(0)

    def theresOrder(self):
        return len(self.__command) != 0