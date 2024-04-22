import unittest
import socket
from drone_library import drone_simulation
import time
from PIL import Image
import io

class MyTestCase(unittest.TestCase):
    def test_something(self):
        drone = drone_simulation.Drone()
        time.sleep(5)
        try:

            imagen_bytes = drone.send_receive({"ACTION": "GET_IMAGE", "PARAMS": ""})
            bytes_rgba = bytearray(imagen_bytes)
            for i in range(0, len(bytes_rgba), 4):
                bytes_rgba[i], bytes_rgba[i + 2] = bytes_rgba[i + 2], bytes_rgba[i]
            imagen = Image.frombytes('RGBA', (400, 240), bytes(bytes_rgba))
            imagen.show()
            print(imagen_bytes)

            time.sleep(5)
        except Exception as e:
            print(e)
            assert False
        time.sleep(5)
        self.assertEqual(True, True)  # add assertion here

    def test_constructor_initialize_instance(self):
        try:
            drone = drone_simulation.Drone()
            print("Instancia del Drone Creada")
            time.sleep(5)
        except Exception as e:
            print(e)
            assert False
        assert True

    def test_send_basic(self):
        drone = drone_simulation.Drone()
        try:
            print(drone.send_receive({"ACTION": "TAKE_OFF", "PARAMS": ""}))
            print("primer mensaje hecho")
            time.sleep(2)
            print(drone.send_receive({"ACTION": "LAND", "PARAMS": ""}))
            print("segundo mensaje hecho")
            time.sleep(2)
        except Exception as e:
            print(e)
            assert False
        print("ending")
        drone.end_simulation()
        print("ended")
        time.sleep(5)
        assert True

    def test_get_actions(self):
        try:
            drone = drone_simulation.Drone()
            actions = drone.get_actions()
            print(actions)
        except Exception as e:
            print(e)
            assert False
        time.sleep(5)
        assert True

    def test_get_image(self):
        drone = drone_simulation.Drone()
        time.sleep(5)
        try:
            start = time.monotonic()
            print(drone.send_receive({"ACTION":"GET_IMAGE", "PARAMS": ""}))
            end = time.monotonic()
            print("time: " + str(end - start))
            time.sleep(5)
        except Exception as e:
            print(e)
            assert False
        time.sleep(5)
        assert True


if __name__ == '__main__':
    unittest.main()
