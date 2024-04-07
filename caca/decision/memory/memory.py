from utils.EData import EData
from .memory_decoding.memory_decoder import MemoryDecoder
from .memory_decoding.security_commands import SecurityCommands
from .memory_decoding.received_commands import ReceivedCommands
from .memory_decoding.other_commands import OtherCommands


class Memory():

    def __init__(self):
        self.__security_decoder = MemoryDecoder(SecurityCommands.COMMANDS)
        self.__command_decoder = MemoryDecoder(ReceivedCommands.COMMANDS)
        self.__other_decoder = MemoryDecoder(OtherCommands.COMMANDS)

    def decode_command(self, command: list):
        key, value = command.pop(0)
        if EData.RECEIVEDED_DATA == key:
            return self.__security_decoder.decode(value)
        elif EData.SECURITY_DATA == key:
            return self.__command_decoder.decode(value)
        elif EData.OTHER == key:
            return self.__other_decoder.decode(value)
        else:
            print('error memory decode')
            return None
