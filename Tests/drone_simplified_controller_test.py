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

    def test_image_trasformation(self):
        import numpy as np
        import matplotlib.pyplot as plt
        def bytearray_to_grayscale_numpy(image_bytes, width, height):
            # Convertir bytearray a un array de numpy
            arr = np.frombuffer(image_bytes, dtype=np.uint8).reshape((height, width, 4))
            #arr = image_bytes
            # Extraer canales R, G, B
            B, G, R = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]

            # Calcular la luminancia según la percepción humana
            # Esta fórmula pondera más el canal verde y menos el azul.
            gray = 0.299 * R + 0.587 * G + 0.114 * B

            # Convertir a uint8 si es necesario
            gray = gray.astype(np.uint8)

            return gray

        def visualize(grayscale_image_numpy):
            plt.figure(figsize=(8, 5))  # Tamaño de la figura en pulgadas
            plt.imshow(grayscale_image_numpy, cmap='gray')  # Mostrar la imagen en escala de grises
            plt.axis('off')  # Desactivar los ejes para una mejor visualización
            plt.show()



        drone = drone_simulation.Drone(world_dir, batch=True, realtime=True)
        drone.start_simulation()
        time.sleep(7)
        width, height = 400, 240
        try:
            start = time.monotonic()
            x = drone.receive()

            grayscale_image_numpy = bytearray_to_grayscale_numpy(x["camera"], width, height)
            end = time.monotonic()
            drone.end_simulation()
            print(end - start)
            visualize(grayscale_image_numpy)
            print(grayscale_image_numpy)
        except Exception as e:
            print(e)
            assert False

        time.sleep(3)
        assert True


if __name__ == '__main__':
    unittest.main()
