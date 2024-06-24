from queue import Queue
from threading import Event, Thread
import pickle

from .config import *

from .SharedMemoryCommunication import Comm
from .executor import CommandExecutor


class Drone:
    """
        It is the interface with the drone controller.
        It is made in order to be able to run the simulation from code.

        Attributes:
            sim_out : Event
                It is the Event that is used by the communication module in order to signal the interface that the simulation crashed or by the interface.
            channel : Comm
                It is the communication channel with the controller using shared memory.
            thread : Thread
                It is the thread that runs the command line that starts the simulation, when it ends sets the sim_out Event to finish the communication channel too.
    """

    def __init__(self, webots_dir, **kwargs):
        """
            Initialize the drone interface, the channel and the simulation
        """
        self.webots_dir = webots_dir
        self.sim_out = Event()
        self.channel = Comm(buffer_size=SHM_SIZE, emitter_name=REQUEST_M, receiver_name=RESPONSE_M,
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

    def get_actions(self) -> list[str]:
        """
            Get the list of actions that the simulator can perform.
            Returns:
                list[str]: It is the collection of the names of all the functions
        """
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
