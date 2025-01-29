from queue import Queue
from threading import Event, Thread
import pickle

import psutil

from config import *
from SharedMemoryCommunication import Comm
from executor import CommandExecutor

import os

import uuid

from manager import register_uid, _read_manager, delete_uid
class Drone:
    """
        It works as an interface with the simulation in 4 simple functions. It starts the simulation, sends the motor
        actions, receive the data_collected from the sensors and shutdown the simulation
    """
    def __init__(self, webots_dir, **kwargs):
        """
            Initialize the drone interface, the channel and the simulation
        """

        process_pid = os.getpid()
        print("drone_sim: ", psutil.Process(os.getpid()).children())#TODO:borrar
        #self.request_memory = f"request_memory_{process_pid}"
        #self.response_memory = f"response_memory_{process_pid}"

        self.uid = 0 #TODO: borrar

        self.request_memory = f"request_memory_"
        self.response_memory = f"response_memory_"
        self.webots_dir = webots_dir
        self.kwargs = kwargs

        self.sim_out = None
        self.queue = None
        self.queue_thread = None
        self.channel = None
        self.command_executor = None

    def send(self, action):
        self.channel.send(pickle.dumps(action))

    def receive(self):
        return self.queue.get()

    def queue_func(self):
        while not self.sim_out.is_set():
            try:
                item = self.channel.receive()
                if self.queue.full():
                    self.queue.get()  # Remove oldest item if queue is full
                self.queue.put(item)
            except Exception as e:
                pass

    def start_simulation(self) -> None:
        """
            It starts the thread that calls the simulation command.
        """
        self.sim_out = Event()
        self.queue = Queue(maxsize=1)

        self.queue_thread = Thread(target=self.queue_func)

        self.command_executor = CommandExecutor(self.sim_out, self.webots_dir, **self.kwargs)
        pid = self.command_executor.execute()

        print("drone_simulation: ",self.request_memory, pid)#TODO: borrar
        print("drone_simulation2: ", psutil.Process(os.getpid()).cmdline())#TODO:borrar

        #TODO:borrar
        self.uid = str(uuid.uuid4())
        register_uid(pid, self.uid)
        print("drone_simulation uid: ", self.uid)
        print("drone_simulation manager: ", _read_manager())
        #borrar

        self.channel = Comm(buffer_size=SHM_SIZE, emitter_name=self.request_memory + self.uid,#str(pid),
                            receiver_name=self.response_memory + self.uid,#str(pid),
                            close_event=self.sim_out)
        self.queue_thread.start()
        print("channel ok and thread started")

    def is_sim_out(self):
        return self.sim_out.is_set()

    def end_simulation(self) -> None:
        """
            Sends the signal to the simulation to end Webots simulation and the communication channel
        """
        delete_uid(self.uid)
        self.channel.send(pickle.dumps({"ACTION": "CLOSE_CONNECTION", "PARAMS": ""}))
        self.channel.close_connection()
