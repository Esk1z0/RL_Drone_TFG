import unittest
import socket
from drone_library import drone_simulation
import time


class MyTestCase(unittest.TestCase):
    def test_something(self):
        cadena_bytes = b'444\x00\x00\x00\x00\x00\x00\x00'
        cadena_limpia = cadena_bytes.replace(b'\x00', b'')  # Eliminar los bytes nulos
        cadena_texto = cadena_limpia.decode()  # Decodificar los bytes a una cadena de texto
        numero = int(cadena_texto)  # Convertir la cadena de texto a un entero
        print(numero)

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

    def test_cycle_fix(self):
        drone = drone_simulation.Drone()
        while not drone.is_connected():
            drone.try_connection()
            time.sleep(0.1)
        try:
            print(drone.send_receive('{"ACTION":"GET_TIME", "PARAMS": ""};'))
            time.sleep(2)
            print(drone.send_receive('{"ACTION":"GET_TIME", "PARAMS": ""};'))
            time.sleep(2)
        except Exception as e:
            print(e)
            assert False
        drone.end_simulation()
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
        while not drone.is_connected():
            drone.try_connection()
            time.sleep(0.1)
        try:
            start = time.monotonic()
            print(drone.send_receive('{"ACTION":"GET_IMAGE", "PARAMS": ""};'))
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
