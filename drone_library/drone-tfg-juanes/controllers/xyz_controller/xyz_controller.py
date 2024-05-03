import sys
from threading import Event
import threading
import time
from controller import Supervisor
from drone_library import ACTIONS, TIME_OUT, TIME_STEP, ACTUATORS, SENSORS, REQUEST_M, RESPONSE_M, SHM_SIZE
from drone_library.functions import FUNCTIONS
import pickle
from SharedMemoryCommunication import Comm

class DroneServer:
    def __init__(self, time_out=TIME_OUT, time_step=TIME_STEP):
        self.server_socket = None
        self.reception_running = False

        self.start_time = time.monotonic()
        self.time_step = time_step
        self.time_out = time_out

        self.robot = Supervisor()
        self.devices = {}

        self.close_sim = Event()
        self.channel = Comm(buffer_size=SHM_SIZE, emitter_name=RESPONSE_M, receiver_name=REQUEST_M, close_event=self.close_sim)


        self.ACTIONS_CONVERT = dict(zip(ACTIONS, FUNCTIONS))

    def main_cycle(self):
        try:
            while self.robot.step(self.time_step) != -1:
                connection_action = threading.Thread(target=self.attend_message)
                if (not self.close_sim.is_set()) and (not self.reception_running):
                    self.reception_running = True
                    connection_action.start()
                if ((not self.time_out == 0) and (time.monotonic() - self.start_time) > self.time_out) or self.close_sim.is_set():
                    break
        except Exception as e:
            print(f'Error: {e}')
        finally:
            self.channel.close_connection()

    def attend_message(self):
        message = self.channel.receive()
        if message:
            self.start_time = time.monotonic()
            print(message.get('ACTION'))
            func = self.ACTIONS_CONVERT.get(message['ACTION'])  # decodificación de la acción
            if func:
                response = func(self.robot, self.devices, message['PARAMS'])  # ejecución de la acción y respuesta
                if response:
                    print('hola')
                    self.channel.send(pickle.dumps(response))
                if response == "CLOSE_CONNECTION":
                    print("fin")
                    self.close_sim.set()
            else:
                print(f'Error: Función no encontrada para la acción {message["ACTION"]}')
        self.reception_running = False



    def enable_everything(self):
        for i in SENSORS:
            device = self.robot.getDevice(i)
            device.enable(self.time_step)
            self.devices.update({i: device})
        for j in ACTUATORS:
            device = self.robot.getDevice(j)
            device.setPosition(float('inf'))
            device.setVelocity(1)
            self.devices.update({j: device})

    def end_simulation(self):
        self.robot.simulationQuit(0)


if __name__ == '__main__':
    server = DroneServer()
    try:
        print(sys.version)
        server.enable_everything()
        server.main_cycle()
    except Exception as e:
        print(e)
    finally:
        time.sleep(5)
        server.end_simulation()
