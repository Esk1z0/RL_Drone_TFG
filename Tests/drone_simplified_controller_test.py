import unittest
import time
from drone_tfg_juanes.simulation_package.controllers.xyz_controller.drone_library import drone_simulation

world_dir = "/Users/jeste/Desktop/Clase/TFG/drone_tfg_juanes/simulation_package/worlds/my_frst_webots_world.wbt"

class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, True)  # add assertion here

    def test_inicio(self):
        drone = drone_simulation.Drone(world_dir, batch=True, realtime=True)
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
        drone = drone_simulation.Drone(world_dir, batch=True, realtime=True)
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
        drone = drone_simulation.Drone(world_dir, batch=True, realtime=True)
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
        drone = drone_simulation.Drone(world_dir, batch=True, realtime=True)
        drone.start_simulation()
        time.sleep(6)
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

    def test_two_samples(self):
        drone = drone_simulation.Drone(world_dir, batch=True, realtime=True)
        drone.start_simulation()
        time.sleep(6)
        try:
            x = []
            y = 1.5
            #drone.send({"ACTION": "SET_ALL_MOTORS", "PARAMS": [300, 300, 300, 300]})
            x.append(drone.receive()["accelerometer"])
            time.sleep(y)
            x.append(drone.receive()["accelerometer"])
            #drone.send({"ACTION": "SET_ALL_MOTORS", "PARAMS": [0, 0, 0, 0]})
            time.sleep(y)
            x.append(drone.receive()["accelerometer"])
            time.sleep(y)
            x.append(drone.receive()["accelerometer"])

            x.append(drone.receive()["altimeter"])
            print(x)

        except Exception as e:
            print(e)
            assert False
        time.sleep(1)
        assert True

    def test_multiple_simulations(self):
        drone1 = drone_simulation.Drone(world_dir, batch=True, realtime=True)
        drone2 = drone_simulation.Drone(world_dir, batch=True, realtime=True)
        drone1.start_simulation()
        drone2.start_simulation()
        time.sleep(6)
        try:
            start = time.monotonic()
            drone1.send({"ACTION": "SET_ALL_MOTORS", "PARAMS": [100, 100, 100, 100]})
            drone2.send({"ACTION": "SET_ALL_MOTORS", "PARAMS": [100, 100, 100, 100]})
            x = drone1.receive()
            y = drone2.receive()
            end = time.monotonic()
            print(end - start)
            print(x)
            print(y)
        except Exception as e:
            print(e)
            assert False
        time.sleep(5)
        assert True





if __name__ == '__main__':
    unittest.main()
