import unittest
import time
from drone_tfg_juanes.controllers.xyz_controller.drone_library import drone_simulation

world_dir = "/Users/jeste/Desktop/Clase/TFG/drone_tfg_juanes/worlds/my_frst_webots_world.wbt"

class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, False)  # add assertion here

    def test_inicio(self):
        drone = drone_simulation.Drone(world_dir)
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
        drone = drone_simulation.Drone(world_dir)
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
        drone = drone_simulation.Drone(world_dir)
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
        drone = drone_simulation.Drone(world_dir)
        drone.start_simulation()
        time.sleep(10)
        try:
            start = time.monotonic()
            drone.send({"ACTION": "SET_ALL_MOTORS", "PARAMS": [100, 100, 100, 100]})
            x = drone.receive()
            end = time.monotonic()
            print(end - start)
            print(x)
        except Exception as e:
            print(e)
            assert False
        time.sleep(5)
        assert True






if __name__ == '__main__':
    unittest.main()
