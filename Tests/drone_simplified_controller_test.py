import unittest
from drone_library import drone_simulation
import time

class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, False)  # add assertion here

    def test_inicio(self):
        drone = drone_simulation.Drone()
        drone.start_simulation()
        time.sleep(10)
        try:
            time.sleep(5)
        except Exception as e:
            print(e)
            assert False
        time.sleep(5)
        assert True

    def test_get_data_basic(self):
        drone = drone_simulation.Drone()
        drone.start_simulation()
        time.sleep(10)
        try:
            print(drone.receive())
        except Exception as e:
            print(e)
            assert False
        time.sleep(5)
        assert True

    def test_set_motors(self):
        drone = drone_simulation.Drone()
        drone.start_simulation()
        time.sleep(10)
        try:
            drone.send({"ACTION": "SET_ALL_MOTORS", "PARAMS": [100, 100, 100, 100]})
        except Exception as e:
            print(e)
            assert False
        time.sleep(5)
        assert True

    def test_send_receive(self):
        drone = drone_simulation.Drone()
        drone.start_simulation()
        time.sleep(10)
        try:
            start = time.monotonic()
            drone.send({"ACTION": "SET_ALL_MOTORS", "PARAMS": [100, 100, 100, 100]})
            drone.receive()
            end = time.monotonic()
            print(end - start)
        except Exception as e:
            print(e)
            assert False
        time.sleep(5)
        assert True






if __name__ == '__main__':
    unittest.main()
