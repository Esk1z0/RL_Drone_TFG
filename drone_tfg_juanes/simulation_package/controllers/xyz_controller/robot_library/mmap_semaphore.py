import mmap
import os
import platform


class BinarySemaphore:
    """This class works as a Binary Semaphore using the memory shared library called mmap"""

    def __init__(self, initial_value=True, name="shared_memory"):
        """
        This constructor creates the memory for the semaphore and sets the initial value.

        Args:
            initial_value (bool): Default value of the semaphore: False for 0, True for 1.
            name (str): Name of the memory for the shared memory information interchange.
        """
        self.name = name
        self._map_memory(name)
        self._initialize(initial_value)

    def _map_memory(self, name):
        """
        Creates the shared memory. In Windows, uses the memory name directly, while in Linux,
        it creates a file in /dev/shm and maps it using mmap.
        """
        if platform.system() == "Windows":
            # En Windows, usar mmap con nombre directamente
            self.mem = mmap.mmap(-1, 1, name)
        else:
            # En Linux, usar archivo en /dev/shm para memoria compartida
            shm_file_path = f'/dev/shm/{name}'
            if not os.path.exists(shm_file_path):
                with open(shm_file_path, "wb") as f:
                    f.write(b'\x00')  # Inicializa con un valor de 0
            self.mem_fd = open(shm_file_path, "r+b")
            self.mem = mmap.mmap(self.mem_fd.fileno(), 1)

    def _initialize(self, initial_value):
        """Initializes the internal value and writes it to the file if it is not yet set."""
        self.value = initial_value
        self.mem.seek(0)
        val = self.mem.read(1)
        if not (val == b'0' or val == b'1'):
            # Si el valor no es '0' o '1', inicializarlo
            self.mem.seek(0)
            self.mem.write(b'1' if initial_value else b'0')
            self.mem.flush()

    def read_open(self):
        """Sets the semaphore to 0, allowing the other part to read the file associated with this semaphore."""
        self.mem.seek(0)
        self.mem.write(b'0')
        self.mem.flush()

    def write_open(self):
        """Sets the semaphore to 1, allowing the other part to write in the file associated with this semaphore."""
        self.mem.seek(0)
        self.mem.write(b'1')
        self.mem.flush()

    def is_read_open(self):
        """Checks if it can read from the file associated with this semaphore."""
        self.mem.seek(0)
        return self.mem.read(1) == b'0'

    def is_write_open(self):
        """Checks if it can write to the file associated with this semaphore."""
        self.mem.seek(0)
        return self.mem.read(1) == b'1'

    def __del__(self):
        """Closes the memory map when the object is destroyed."""
        self.mem.close()
        if hasattr(self, 'mem_fd'):
            self.mem_fd.close()
