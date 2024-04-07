import threading
import subprocess
import socket
import warnings

from . import *


def initialize_instance() -> None:
    """
        Activates the Webots World in mode realtime and activating the flags no-rendering and batch
    """
    proceso = subprocess.run(COMMAND, shell=True, capture_output=True, text=True)
    print('Salida Simulador: ' + str(proceso.returncode))


class Drone:
    def __init__(self):
        warnings.filterwarnings(action="ignore", message="unclosed", category=ResourceWarning)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sim_up = False
        self.connected = False
        thread = threading.Thread(target=initialize_instance)
        thread.start()

    def try_connection(self) -> None:
        """
            Try to connect to the simulator socket through the HOST and PORT selected
        """
        try:
            self.sock.connect((HOST, PORT))
            self.connected = True
        except Exception as e:
            print("Error al conectar " + f'Error: {e}')
            self.connected = False

    def is_connected(self):
        return self.connected

    def send_receive(self, message: str):
        """
            Sends the message to the simulator through the socket and returns what was
            returned by the simulator
            Args:
                message (str): A json transformable string with a ';' at the end
            Returns:
                str: The Response from the simulator socket
        """
        self.send(message)
        return self.receive()



    def send(self, message: str) -> None:
        """
            Sends the message to the simulator through the socket
            Args:
            essage (str): A json transformable string with a ';' at the end
        """
        self.sock.sendall(message.encode())

    def receive(self):
        buffer = b''
        while True:
            datos_recibidos = self.sock.recv(1024)
            buffer += datos_recibidos
            if b';' in buffer:
                break
        value = buffer.decode()
        value = value.replace(';', ' ')
        return value

    def get_actions(self) -> list[str]:
        """
            Get the list of actions that the simulator can perform
        """
        return ACTIONS

    def end_simulation(self) -> None:
        """
            Sends the signal to the simulation to end Webots
        """
        self.sock.sendall('{"ACTION":"CLOSE_CONNECTION", "PARAMS":""};'.encode())
        self.sock.close()
