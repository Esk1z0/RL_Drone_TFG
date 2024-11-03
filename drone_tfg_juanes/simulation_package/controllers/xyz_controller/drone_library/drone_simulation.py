from queue import Queue
from threading import Event, Thread
import pickle

from config import *
from SharedMemoryCommunication import Comm
from executor import CommandExecutor

import os


class Drone:
    """
        It works as an interface with the simulation in 4 simple functions. It starts the simulation, sends the motor
        actions, receive the data from the sensors and shutdown the simulation
    """
    def __init__(self, webots_dir, **kwargs):
        """
            Initialize the drone interface, the channel and the simulation
        """

        process_pid = os.getpid()
        self.request_memory = f"request_memory_{process_pid}"
        self.response_memory = f"response_memory_{process_pid}"
        self.webots_dir = webots_dir
        self.kwargs = kwargs
        self.threads_init()

    def threads_init(self):
        self.sim_out = Event()
        self.queue = Queue(maxsize=1)

        self.queue_thread = Thread(target=self.queue_func)

        self.channel = Comm(buffer_size=SHM_SIZE, emitter_name=self.request_memory, receiver_name=self.response_memory,
                            close_event=self.sim_out)
        self.command_executor = CommandExecutor(self.sim_out, self.webots_dir, **self.kwargs)

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
        self.threads_init()
        self.command_executor.execute()
        self.queue_thread.start()

    def is_sim_out(self):
        return self.sim_out.is_set()

    def end_simulation(self) -> None:
        """
            Sends the signal to the simulation to end Webots simulation and the communication channel
        """
        self.channel.send(pickle.dumps({"ACTION": "CLOSE_CONNECTION", "PARAMS": ""}))
        self.channel.close_connection()
