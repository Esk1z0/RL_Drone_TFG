import threading
import subprocess

import mmap
import pickle

from . import *
from Mmap_Semaphore import BinarySemaphore


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
        self.receptor = mmap.mmap(-1, SHM_SIZE, RESPONSE_M)
        self.emitter = mmap.mmap(-1, SHM_SIZE, REQUEST_M)
        self.sem_receptor = BinarySemaphore(name=SEM_RESPONSE_M)
        self.sem_emitter = BinarySemaphore(name=SEM_REQUEST_M)
        self.sim_out = threading.Event()
        thread = threading.Thread(target=initialize_instance, args=[self.sim_out])
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
        print(pickle.dumps(message))
        print('hola')
        return self.receive()

    def send(self, data) -> None:
        """
            Sends the message to the simulator through the socket
            Args:
            essage (str): A json transformable string with a ';' at the end
        """
        while not self.sem_emitter.is_write_open():
            if self.sim_out.is_set(): raise Exception("crashed")
        self.send_emitter(b'\x00' * SHM_SIZE)
        self.send_emitter(str(len(data)).encode())
        self.sem_emitter.read_open()
        for i in range(0, len(data), SHM_SIZE):
            while not self.sem_emitter.is_write_open():
                if self.sim_out.is_set(): raise Exception("crashed")
            chunk = data[i:i + SHM_SIZE]
            if len(chunk) < SHM_SIZE:
                self.send_emitter(b'\x00' * SHM_SIZE)
            self.send_emitter(chunk)
            self.sem_emitter.read_open()

    def receive(self):
        data_received = b''
        while not self.sem_receptor.is_read_open():
            if self.sim_out.is_set(): raise Exception("crashed")
        self.receptor.seek(0)
        length = self.receptor.read()
        self.receptor.seek(0)
        self.receptor.write(b'\x00' * SHM_SIZE)
        self.sem_receptor.write_open()
        for _ in range(0, int(length.replace(b'\x00', b'').decode()), SHM_SIZE):
            while not self.sem_receptor.is_read_open():
                if self.sim_out.is_set(): raise Exception("crashed")
            self.receptor.seek(0)
            chunk = self.receptor.read()
            data_received += chunk
            self.sem_receptor.write_open()
            # if chunk == b'\x00' * SHM_SIZE:
            #    break
        if data_received:
            # data_received.replace(b'\x00', b'')
            #print(data_received)
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
        self.send(pickle.dumps({"ACTION": "CLOSE_CONNECTION", "PARAMS": ""}))
        self.emitter.close()
        self.receptor.close()

    def send_emitter(self, data: bytes):
        self.emitter.seek(0)
        self.emitter.write(data)
        self.emitter.flush()

    def receive_receptor(self):
        self.receptor.seek(0)
        return self.receptor.read()

    def send_receptor(self, data: bytes):
        self.receptor.seek(0)
        self.receptor.write(data)
        self.receptor.flush()
