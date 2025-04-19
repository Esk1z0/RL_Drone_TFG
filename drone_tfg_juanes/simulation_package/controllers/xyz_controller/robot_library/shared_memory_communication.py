import mmap
import os
import platform
import pickle
from threading import Event
from mmap_semaphore import BinarySemaphore


class Comm:
    """
        This class uses mmap as a buffer and a BinarySemaphore to pass information through shared memory.
    """

    def __init__(self, buffer_size: int, emitter_name: str, receiver_name: str, close_event: Event):
        """
        Constructs a communication channel through shared memory. It needs to be instantiated on both ends of the
        channel with the request_name and response_name swapped.

        Args:
            buffer_size (int): Size of the buffer to pass the data_collected.
            emitter_name (str): Name for the emitter semaphore and buffer.
            receiver_name (str): Name for the receiver semaphore and buffer.
            close_event (Event): Event for when the simulation finishes.
        """
        self.buffer_size = buffer_size
        self.close = close_event

        # Detectar si estamos en Windows o Linux
        if platform.system() == "Windows":
            # Windows usa mmap con nombres
            self.emitter = mmap.mmap(-1, buffer_size, tagname=emitter_name)
            self.receptor = mmap.mmap(-1, buffer_size, tagname=receiver_name)
        else:
            # Linux usa archivos en /dev/shm para memoria compartida
            self.emitter, self.emitter_fd = self._create_mmap_file(emitter_name, buffer_size)
            self.receptor, self.receptor_fd = self._create_mmap_file(receiver_name, buffer_size)

        self.sem_emitter = BinarySemaphore(name="sem_" + emitter_name)
        self.sem_receptor = BinarySemaphore(name="sem_" + receiver_name)

    def _create_mmap_file(self, name: str, size: int) -> (mmap.mmap, 'file'):
        """
        Crea un archivo en /dev/shm en Linux y lo mapea en la memoria.

        Args:
            name (str): El nombre que se utilizará para el archivo en /dev/shm.
            size (int): El tamaño del buffer de memoria compartida.

        Returns:
            Tuple[mmap.mmap, file]: El objeto mmap creado y el descriptor de archivo.
        """
        shm_file_path = f'/dev/shm/{name}'
        if not os.path.exists(shm_file_path):
            with open(shm_file_path, "wb") as f:
                f.write(b'\x00' * size)

        shm_fd = open(shm_file_path, "r+b")
        mmap_obj = mmap.mmap(shm_fd.fileno(), size)
        return mmap_obj, shm_fd

    def send(self, data) -> None:
        """
        Sends the message to the simulator through the shared memory of emitter.

        Args:
            data: Any binary data_collected can be passed.
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
           Receives the data_collected sent from the other part and returns it deserialized.

           Returns:
               Any: The deserialized data_collected received. If no data_collected is received, returns None.
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
        if platform.system() != "Windows":
            self.receptor_fd.close()
            self.emitter_fd.close()

    def __del__(self):
        self.close_connection()

    def is_closed(self):
        return self.receptor.closed or self.emitter.closed
