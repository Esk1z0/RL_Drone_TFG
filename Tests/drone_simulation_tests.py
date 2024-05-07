import unittest
import socket
from drone_library import drone_simulation
import time
from PIL import Image
import io

class MyTestCase(unittest.TestCase):
    def test_something(self):
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

    def test_constructor_initialize_instance(self):
        try:
            drone = drone_simulation.Drone()
            drone.start_simulation()
            print("Instancia del Drone Creada")
            time.sleep(5)
        except Exception as e:
            print(e)
            assert False
        assert True

    def test_send_basic(self):
        drone = drone_simulation.Drone()
        drone.start_simulation()
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
            drone.start_simulation()
            actions = drone.get_actions()
            print(actions)
        except Exception as e:
            print(e)
            assert False
        time.sleep(5)
        assert True

    def test_get_image(self):
        drone = drone_simulation.Drone()
        drone.start_simulation()
        time.sleep(10)
        try:
            start = time.monotonic()
            imagen_bytes = drone.send_receive({"ACTION": "GET_IMAGE", "PARAMS": ""})
            imagen = Image.frombytes('RGBA', (400, 240), imagen_bytes)

            r, g, b, a = imagen.split()
            imagen_rgba = Image.merge('RGBA', (b, g, r, a))
            fin = time.monotonic()
            print('tiempo ', str(fin - start))
            imagen_rgba.show()

            time.sleep(5)
        except Exception as e:
            print(e)
            assert False
        time.sleep(5)
        assert True

    def test_get_imu(self):
        drone = drone_simulation.Drone()
        drone.start_simulation()
        time.sleep(5)
        try:
            start = time.monotonic()
            x = drone.send_receive({"ACTION": "GET_IMU", "PARAMS": ""})
            fin = time.monotonic()
            print('tiempo ', str(fin - start))
            print(x)
            time.sleep(5)
        except Exception as e:
            print(e)
            assert False
        time.sleep(5)
        assert True

    def test_get_distance(self):
        drone = drone_simulation.Drone()
        drone.start_simulation()
        time.sleep(9)
        try:
            start = time.monotonic()
            x = drone.send_receive({"ACTION": "GET_DISTANCE", "PARAMS": ""})
            fin = time.monotonic()
            print('tiempo ', str(fin - start))
            print(x)
            time.sleep(5)
        except Exception as e:
            print(e)
            assert False
        time.sleep(5)
        assert True

    def test_set_backmotorvel(self):
        drone = drone_simulation.Drone()
        drone.start_simulation()
        time.sleep(9)
        try:
            start = time.monotonic()
            x = drone.send_receive({"ACTION": "SET_MOTOR_RL", "PARAMS": {"velocity": 100}})
            fin = time.monotonic()
            print('tiempo ', str(fin - start))
            print(x)
            time.sleep(8)
        except Exception as e:
            print(e)
            assert False
        time.sleep(5)
        assert True

    def test_set_fourmotors(self):
        drone = drone_simulation.Drone()
        drone.start_simulation()
        time.sleep(9)
        try:
            start = time.monotonic()
            drone.send_receive({"ACTION": "SET_MOTOR_RL", "PARAMS": {"velocity": 300}})
            drone.send_receive({"ACTION": "SET_MOTOR_RR", "PARAMS": {"velocity": 300}})
            drone.send_receive({"ACTION": "SET_MOTOR_FL", "PARAMS": {"velocity": 300}})
            drone.send_receive({"ACTION": "SET_MOTOR_FR", "PARAMS": {"velocity": 300}})
            fin = time.monotonic()
            print('tiempo ', str(fin - start))
            time.sleep(8)
        except Exception as e:
            print(e)
            assert False
        time.sleep(5)
        assert True

    def test_set_fourmotors_at_once(self):
        drone = drone_simulation.Drone()
        drone.start_simulation()
        time.sleep(9)
        try:
            start = time.monotonic()
            drone.send_receive({"ACTION": "SET_ALL_MOTORS", "PARAMS": [300, 300, 300, 300]})
            fin = time.monotonic()
            print('tiempo ', str(fin - start))
            time.sleep(8)
        except Exception as e:
            print(e)
            assert False
        time.sleep(5)
        assert True


    def test_reset_simulation(self):
        drone = drone_simulation.Drone()
        drone.start_simulation()
        time.sleep(9)
        try:
            start = time.monotonic()
            x = drone.send_receive({"ACTION": "RESET", "PARAMS": ""})
            fin = time.monotonic()
            print('tiempo ', str(fin - start))
            print(x)
            time.sleep(5)
        except Exception as e:
            print(e)
            assert False
        time.sleep(5)
        assert True

    def test_get_data(self):
        drone = drone_simulation.Drone()
        drone.start_simulation()
        time.sleep(9)
        try:
            start = time.monotonic()
            x = drone.send_receive({"ACTION": "GET_DATA", "PARAMS": ""})
            fin = time.monotonic()
            print(type(x))
            print(len(x))
            print('tiempo ', str(fin - start))
            time.sleep(5)
        except Exception as e:
            print(e)
            assert False
        time.sleep(5)
        assert True

if __name__ == '__main__':
    unittest.main()
