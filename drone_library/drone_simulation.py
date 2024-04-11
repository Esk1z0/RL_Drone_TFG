import threading
import subprocess
import socket
import warnings
import mmap
import pickle

from . import *
from Mmap_Semaphore import BinarySemaphore


def initialize_instance() -> None:
    """
        Activates the Webots World in mode realtime and activating the flags no-rendering and batch
    """
    proceso = subprocess.run(COMMAND, shell=True, capture_output=True, text=True)
    print('Salida Simulador: ' + str(proceso.returncode))


class Drone:
    def __init__(self):
        self.sim_up = False
        self.receptor = mmap.mmap(-1, SHM_SIZE, RESPONSE_M)
        self.emitter = mmap.mmap(-1, SHM_SIZE, REQUEST_M)
        self.sem_receptor = BinarySemaphore(name=SEM_RESPONSE_M)
        self.sem_emitter = BinarySemaphore(name=SEM_REQUEST_M)
        thread = threading.Thread(target=initialize_instance)
        thread.start()

    def send_receive(self, message: object):
        """
            Sends the message to the simulator through the socket and returns what was
            returned by the simulator
            Args:
                message (object): A json transformable string with a ';' at the end
            Returns:
                str: The Response from the simulator socket
        """
        self.send(pickle.dumps(message))
        print('hola')
        return self.receive()

    def send(self, data) -> None:
        """
            Sends the message to the simulator through the socket
            Args:
            essage (str): A json transformable string with a ';' at the end
        """
        for i in range(0, len(data), SHM_SIZE):
            print('gol')
            chunk = data[i:i + SHM_SIZE]
            print(chunk)
            while not self.sem_emitter.is_write_open():
                pass
            print('golgol')
            self.emitter.seek(0)  # Asegurarse de que estamos al principio de la memoria compartida
            self.emitter.write(chunk)
            self.emitter.flush()

            self.sem_emitter.read_open()

    def receive(self):
        data_received = b''
        while True:
            self.sem_receptor.acquire()
            chunk = self.receptor.read()
            data_received += chunk
            if not chunk:
                break
            self.sem_receptor.release()
        if data_received:
            return pickle.loads(data_received)
        else:
            return None

    def get_actions(self) -> list[str]:
        """
            Get the list of actions that the simulator can perform
        """
        return ACTIONS

    def end_simulation(self) -> None:
        """
            Sends the signal to the simulation to end Webots
        """
        self.send(pickle.dumps({"ACTIONS": "closing_connection", "PARAMS": ""}))
        self.emitter.close()
        self.receptor.close()
