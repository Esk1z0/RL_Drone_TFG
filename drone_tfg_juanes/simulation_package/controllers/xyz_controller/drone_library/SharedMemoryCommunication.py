from threading import Event
import mmap
import pickle

from .Mmap_Semaphore import BinarySemaphore


class Comm:

    def __init__(self, buffer_size: int, emitter_name: str, receiver_name: str, close_event: Event):
        """
        It constructs a communication channel through shared memory,it needs to be instantiated in the two channel ends
        with the request_name and response_name swapped

        Args:
            buffer_size (int): Is the size of the buffer to pass the data
            emitter_name (str): Is the name for the emitter semaphore and buffer
            receiver_name (str): Is the name for the receiver semaphore and buffer
            close_event (Event): Is the event for when the simulation finishes
        """
        self.buffer_size = buffer_size
        self.emitter = mmap.mmap(-1, buffer_size, emitter_name)
        self.receptor = mmap.mmap(-1, buffer_size, receiver_name)
        self.sem_emitter = BinarySemaphore(name="sem_" + emitter_name)
        self.sem_receptor = BinarySemaphore(name="sem_" + receiver_name)
        self.close = close_event

    def send(self, data) -> None:
        """
        Sends the message to the simulator through the shared memory of emitter

        Args:
            data: any binarize data can be passed
        """
        self.wait_emitter()
        self.send_start_emitter(data)
        for i in range(0, len(data), self.buffer_size):
            self.wait_emitter()
            chunk = data[i:i + self.buffer_size]
            if len(chunk) < self.buffer_size:
                self.send_emitter(b'\x00' * self.buffer_size)
            self.send_emitter(chunk)
            self.sem_emitter.read_open()

    def receive(self):
        """
           Receives the data sent from the other part and returns it deserialized.

           Returns:
               Any: The deserialized data received. If no data is received, returns None.
           """
        data_received = b''
        self.wait_receiver()
        length = self.receive_start_receiver()
        for _ in range(0, int(length.rstrip(b'\x00').decode()), self.buffer_size):
            self.wait_receiver()
            chunk = self.receive_receptor()
            data_received += chunk
            self.sem_receptor.write_open()
        return pickle.loads(data_received) if data_received else None

    def send_start_emitter(self, data):
        """
            Sends the start signal to the emitter with the length of the data.

            Args:
                data (bytes): The data to be sent.
        """
        self.send_emitter(b'\x00' * self.buffer_size)
        self.send_emitter(str(len(data)).encode())
        self.sem_emitter.read_open()

    def receive_start_receiver(self):
        """
            Receives the start signal from the receiver which includes the length of the data.

            Returns:
                bytes: The length of the data as bytes.
        """
        length = self.receive_receptor()
        self.send_receptor(b'\x00' * self.buffer_size)
        self.sem_receptor.write_open()
        return length

    def wait_emitter(self):
        """
            Waits until the emitter is ready to write. Raises an exception if the connection is closed.
        """
        while not self.sem_emitter.is_write_open():
            if self.close.is_set():
                raise Exception("crashed")

    def wait_receiver(self):
        """
            Waits until the receiver is ready to read. Raises an exception if the connection is closed.
        """
        while not self.sem_receptor.is_read_open():
            if self.close.is_set():
                raise Exception("crashed")

    def send_emitter(self, data: bytes):
        """
            Sends data to the emitter.

            Args:
                data (bytes): The data to be sent.
        """
        self.emitter.seek(0)
        self.emitter.write(data)
        self.emitter.flush()

    def receive_receptor(self):
        """
            Receives data from the receptor.

            Returns:
                bytes: The data received.
        """
        self.receptor.seek(0)
        return self.receptor.read()

    def send_receptor(self, data: bytes):
        """
            Sends data to the receptor.

            Args:
                data (bytes): The data to be sent.
        """
        self.receptor.seek(0)
        self.receptor.write(data)
        self.receptor.flush()

    def close_connection(self):
        """
            Closes the connection by closing the receptor and emitter.
        """
        self.receptor.close()
        self.emitter.close()

    def is_closed(self):
        """
            Checks if the connection is closed.

            Returns:
                bool: True if the receptor or emitter is closed, False otherwise.
        """
        return self.receptor.closed or self.emitter.closed
