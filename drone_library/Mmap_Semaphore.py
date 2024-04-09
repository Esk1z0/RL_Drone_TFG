import mmap


class BinarySemaphore:
    def __init__(self, initial_value=False, name="shared_memory"):
        self._map_memory(name)
        self._initialize(initial_value)

    def _map_memory(self, name):
        self.mem = mmap.mmap(-1, 1, name)

    def _initialize(self, initial_value):
        self.value = initial_value
        self.mem.seek(0)
        self.mem.write(b'\x01' if initial_value else b'\x00')

    def acquire(self):
        while True:
            self.mem.seek(0)
            value = self.mem.read_byte()
            if value == b'\x01':
                self.mem.seek(0)
                self.mem.write(b'\x00')
                return True

    def release(self):
        self.mem.seek(0)
        self.mem.write(b'\x01')

    def __del__(self):
        self.mem.close()
