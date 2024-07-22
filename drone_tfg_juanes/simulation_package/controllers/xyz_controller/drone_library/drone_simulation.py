from queue import Queue
from threading import Event, Thread
import pickle

from .config import *
from .SharedMemoryCommunication import Comm
from .executor import CommandExecutor


class Drone:
    """
        It works as an interface with the simulation in 4 simple functions. It starts the simulation, sends the motor
        actions, receive the data from the sensors and shutdown the simulation
    """
    def __init__(self, webots_dir, **kwargs):
        """
            Initialize the drone interface, the channel and the simulation
        """
        REQUEST_MEMORY, RESPONSE_MEMORY = get_next_instance_name(is_client=True)

        self.webots_dir = webots_dir
        self.sim_out = Event()
        self.channel = Comm(buffer_size=SHM_SIZE, emitter_name=REQUEST_MEMORY, receiver_name=RESPONSE_MEMORY,
                            close_event=self.sim_out)
        self.command_executor = CommandExecutor(self.sim_out, webots_dir, **kwargs)
        self.queue_thread = Thread(target=self.queue_func)
        self.queue = Queue(maxsize=1)

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
