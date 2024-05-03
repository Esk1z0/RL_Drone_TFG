import threading
from threading import Event, Thread
import subprocess

import mmap
import pickle

from . import *
from Mmap_Semaphore import BinarySemaphore
from SharedMemoryCommunication import Comm

def initialize_instance(event) -> None:
    """
        Activates the Webots World in mode realtime and activating the flags no-rendering and batch
    """
    proceso = subprocess.run(COMMAND, shell=True, capture_output=True, text=True)
    print('Salida Simulador: ' + str(proceso.returncode))
    event.set()


class Drone:
    def __init__(self):
        self.sim_up = False

        self.sim_out = Event()
        self.channel = Comm(buffer_size=SHM_SIZE, emitter_name=REQUEST_M, receiver_name=RESPONSE_M, close_event=self.sim_out)

        self.thread = Thread(target=initialize_instance, args=[self.sim_out])


    def send_receive(self, message: object):
        """
            Sends the message to the simulator through the socket and returns what was
            returned by the simulator
            Args:
                message (object): A json transformable string with a ';' at the end
            Returns:
                str: The Response from the simulator socket
        """
        self.channel.send(pickle.dumps(message))
        return self.channel.receive()





    def get_actions(self) -> list[str]:
        """
            Get the list of actions that the simulator can perform
        """
        return ACTIONS

    def start_simulation(self) -> None:
        self.thread.start()


    def end_simulation(self) -> None:
        """
            Sends the signal to the simulation to end Webots
        """
        self.channel.send(pickle.dumps({"ACTION": "CLOSE_CONNECTION", "PARAMS": ""}))
        self.channel.close_connection()


