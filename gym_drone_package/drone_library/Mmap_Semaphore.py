import mmap


class BinarySemaphore:
    def __init__(self, initial_value=True, name="shared_memory"):
        self._map_memory(name)
        self._initialize(initial_value)

    def _map_memory(self, name):
        self.mem = mmap.mmap(-1, 1, name)

    def _initialize(self, initial_value):
        self.value = initial_value
        self.mem.seek(0)
        val = self.mem.read()
        if not (val == b'0' or val == b'1'):
            self.mem.seek(0)
            self.mem.write(b'1' if initial_value else b'0')
            self.mem.flush()

    def read_open(self):
        self.mem.seek(0)
        self.mem.write(b'0')
        self.mem.flush()

    def write_open(self):
        self.mem.seek(0)
        self.mem.write(b'1')
        self.mem.flush()

    def is_read_open(self):
        self.mem.seek(0)
        return self.mem.read(1) == b'0'

    def is_write_open(self):
        self.mem.seek(0)
        return (self.mem.read(1) == b'1')

    def __del__(self):
        self.mem.close()
