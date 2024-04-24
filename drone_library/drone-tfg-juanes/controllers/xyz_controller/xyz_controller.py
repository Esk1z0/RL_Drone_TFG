import sys
import json

import threading
import time
from controller import Supervisor, Camera
from drone_library import ACTIONS, PORT, HOST, TIME_OUT, TIME_STEP, ACTUATORS, SENSORS, REQUEST_M, RESPONSE_M, \
    SEM_REQUEST_M, SEM_RESPONSE_M, SHM_SIZE
from drone_library.functions import FUNCTIONS, Connection_End, Connection_Timeout
import mmap
import pickle
from Mmap_Semaphore import BinarySemaphore


class DroneServer:
    def __init__(self, time_out=TIME_OUT, time_step=TIME_STEP):
        self.server_socket = None
        self.reception_running = False

        self.start_time = time.monotonic()
        self.time_step = time_step
        self.time_out = time_out

        self.robot = Supervisor()
        self.devices = {}

        self.emitter = mmap.mmap(-1, SHM_SIZE, RESPONSE_M)
        self.receptor = mmap.mmap(-1, SHM_SIZE, REQUEST_M)
        self.sem_emitter = BinarySemaphore(name=SEM_RESPONSE_M)
        self.sem_receptor = BinarySemaphore(name=SEM_REQUEST_M)

        self.close_sim = threading.Event()
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
            self.close_connection()

    def attend_message(self):
        message = self.receive_data()
        if message:
            self.start_time = time.monotonic()
            print(message.get('ACTION'))
            func = self.ACTIONS_CONVERT.get(message['ACTION'])  # decodificación de la acción
            if func:
                response = func(self.robot, self.devices, message['PARAMS'])  # ejecución de la acción y respuesta
                if response:
                    print('hola')
                    self.send_data(pickle.dumps(response))
                if response == "CLOSE_CONNECTION":
                    print("fin")
                    self.close_sim.set()
            else:
                print(f'Error: Función no encontrada para la acción {message["ACTION"]}')
        self.reception_running = False

    def receive_data(self):
        data_received = b''
        while not self.sem_receptor.is_read_open():
            if self.close_sim.is_set(): raise Exception("crashed")
        length = self.receive_receptor()
        print('len message:' + length.rstrip(b'\x00').decode() + 'yupi')
        self.send_receptor(b'\x00' * SHM_SIZE)
        self.sem_receptor.write_open()

        for _ in range(0, int(length.rstrip(b'\x00').decode()), SHM_SIZE):
            while not self.sem_receptor.is_read_open():
                if self.close_sim.is_set(): raise Exception("crashed")
            chunk = self.receive_receptor()
            data_received += chunk
            self.sem_receptor.write_open()
        if data_received:
            return pickle.loads(data_received)
        else:
            return None

    def send_data(self, data):
        while not self.sem_emitter.is_write_open():
            if self.close_sim.is_set(): raise Exception("crashed")
        self.send_emitter(b'\x00' * SHM_SIZE)
        self.send_emitter(str(len(data)).encode())
        self.sem_emitter.read_open()
        for i in range(0, len(data), SHM_SIZE):
            while not self.sem_emitter.is_write_open():
                if self.close_sim.is_set(): raise Exception("crashed")
            chunk = data[i:i + SHM_SIZE]
            if len(chunk) < SHM_SIZE:
                self.send_emitter(b'\x00' * SHM_SIZE)

            self.send_emitter(chunk)
            self.sem_emitter.read_open()

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

    def send_emitter(self, data: bytes):
        self.emitter.seek(0)
        self.emitter.write(data)
        self.emitter.flush()

    def receive_receptor(self):
        self.receptor.seek(0)
        return self.receptor.read()

    def send_receptor(self, data: bytes):
        self.receptor.seek(0)
        self.receptor.write(data)
        self.receptor.flush()

    def close_connection(self):
        self.receptor.close()
        self.emitter.close()

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
