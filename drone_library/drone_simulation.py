from queue import Queue
from threading import Event, Thread
import subprocess
import pickle

from . import *
from SharedMemoryCommunication import Comm

def initialize_instance(event) -> None:
    """
        Activates the Webots World in mode realtime and activating the flags batch and realtime
    """
    proceso = subprocess.run(COMMAND, shell=True, capture_output=True, text=True)
    print('Salida Simulador: ' + str(proceso.returncode))
    event.set()


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
    def __init__(self):
        """
            Initialize the drone interface, the channel and the simulation
        """
        self.sim_out = Event()
        self.channel = Comm(buffer_size=SHM_SIZE, emitter_name=REQUEST_M, receiver_name=RESPONSE_M, close_event=self.sim_out)
        self.thread = Thread(target=initialize_instance, args=[self.sim_out])
        self.queue_thread = Thread(target=self.queue_func)
        self.queue = Queue(maxsize=1)



    def send_receive(self, message: object) -> object:
        """
            Sends the message to the simulator through the shared memory and returns what was
            sent back by the simulation controller
            Args:
                message (object): a dict with the form {\"ACTION\":\"FUNC_NAME\", \"PARAMS\": function_parameters}.
            Returns:
                object: The Response from the simulator controller, it can be any object
        """
        self.channel.send(pickle.dumps(message))
        return self.channel.receive()

    def send(self, action):
        self.channel.send(pickle.dumps(action))

    def receive(self):
        return self.queue.get()

    def queue_func(self):
        while not self.sim_out.is_set():
            item = self.channel.receive()
            if self.queue.full():
                self.queue.get()  # Remove oldest item if queue is full
            self.queue.put(item)

    def get_actions(self) -> list[str]:
        """
            Get the list of actions that the simulator can perform.
            Returns:
                list[str]: It is the collection of the names of all the functions
        """
        return ACTIONS

    def start_simulation(self) -> None:
        """
            It starts the thread that calls the simulation command.
        """
        self.thread.start()
        self.queue_thread.start()


    def end_simulation(self) -> None:
        """
            Sends the signal to the simulation to end Webots simulation and the communication channel
        """
        self.channel.send(pickle.dumps({"ACTION": "CLOSE_CONNECTION", "PARAMS": ""}))
        self.channel.close_connection()


