import unittest
from drone_tfg_juanes.simulation_package.controllers.xyz_controller.robot_library.mmap_semaphore import BinarySemaphore
from drone_tfg_juanes.simulation_package.controllers.xyz_controller.robot_library.shared_memory_communication import Comm
import threading
import pickle
import time

class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, False)  # add assertion here

    def test_pass_mesage(self):
        close_sim = threading.Event()
        channel1 = Comm(buffer_size=2048, emitter_name="a", receiver_name="b", close_event=close_sim)
        channel2 = Comm(buffer_size=2048, emitter_name="b", receiver_name="a", close_event=close_sim)

        def send():
            channel1.send(pickle.dumps("hola"))

        def recive():
            x = channel2.receive()
            print("\n"+x)

        threading.Thread(target=send).start()
        threading.Thread(target=recive).start()

if __name__ == '__main__':
    unittest.main()
