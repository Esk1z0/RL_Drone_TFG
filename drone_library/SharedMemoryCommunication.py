from threading import Event
import mmap
import pickle
from Mmap_Semaphore import BinarySemaphore

class Comm:

    def __init__(self, buffer_size: int, emitter_name: str, receiver_name: str, close_event: Event):
        """
           It constructs a communication channel through shared memory,
           it needs to be instantiated in the two channel ends with the request_name and response_name
           swapped
        """
        self.buffer_size = buffer_size
        self.emitter = mmap.mmap(-1, buffer_size, emitter_name)  # igual
        self.receptor = mmap.mmap(-1, buffer_size, receiver_name)  # igual
        self.sem_emitter = BinarySemaphore(name="sem_" + emitter_name)  # igual
        self.sem_receptor = BinarySemaphore(name="sem_" + receiver_name)  # igual
        self.close = close_event

    def send(self, data) -> None:  # igual
        """
            Sends the message to the simulator through the shared memory of emitter
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

    def receive_data(self):
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
        self.send_emitter(b'\x00' * self.buffer_size)
        self.send_emitter(str(len(data)).encode())
        self.sem_emitter.read_open()

    def receive_start_receiver(self):
        length = self.receive_receptor()
        self.send_receptor(b'\x00' * self.buffer_size)
        self.sem_receptor.write_open()
        return length

    def wait_emitter(self):
        while not self.sem_emitter.is_write_open():
            if self.close.is_set():
                raise Exception("crashed")

    def wait_receiver(self):
        while not self.sem_receptor.is_read_open():
            if self.close.is_set():
                raise Exception("crashed")

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

    def close_connection(self):
        self.receptor.close()
        self.emitter.close()
