import mmap


class BinarySemaphore:
    """This class works as a Binary Semaphore using memory shared library called mmap"""
    def __init__(self, initial_value=True, name="shared_memory"):
        """This constructor create the temporal file for the semaphore and set the initial value

        Args:
            initial_value (bool): Is the default value of the semaphore: False for 0, True for 1
            name (str): Is the name of the file for the shared memory information interchange
            """
        self._map_memory(name)
        self._initialize(initial_value)

    def _map_memory(self, name):
        """Creates the shared memory file with mmap"""
        self.mem = mmap.mmap(-1, 1, name)

    def _initialize(self, initial_value):
        """Creates the internal value and writes the value in the file in case it is not written yet"""
        self.value = initial_value
        self.mem.seek(0)
        val = self.mem.read()
        if not (val == b'0' or val == b'1'):
            self.mem.seek(0)
            self.mem.write(b'1' if initial_value else b'0')
            self.mem.flush()

    def read_open(self):
        """Set the semaphore to 0, allowing the other part to read the file associated with this semaphore"""
        self.mem.seek(0)
        self.mem.write(b'0')
        self.mem.flush()

    def write_open(self):
        """Set the semaphore to 1 allowing the other part to write in the file associated with this semaphore"""
        self.mem.seek(0)
        self.mem.write(b'1')
        self.mem.flush()

    def is_read_open(self):
        """Tells if it can read from the file associated with this semaphore"""
        self.mem.seek(0)
        return self.mem.read(1) == b'0'

    def is_write_open(self):
        """Tells if it can write on the file associated with this semaphore"""
        self.mem.seek(0)
        return self.mem.read(1) == b'1'

    def __del__(self):
        self.mem.close()
