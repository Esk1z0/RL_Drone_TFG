import platform
import threading
import time
import pickle
from controller import Supervisor
import numpy as np

import os
import psutil

from robot_library.config import TIME_OUT, TIME_STEP, ACTUATORS, SENSORS, SHM_SIZE

from robot_library.shared_memory_communication import Comm

from manager import get_uid


class RobotServer:
    def call_uid(self, pid):
        for _ in range(5):
            uid = get_uid(pid)
            if uid is not None:
                return uid
            time.sleep(0.1)
        return None  # si luego de 5 intentos no aparece

    def __init__(self, time_out=TIME_OUT, time_step=TIME_STEP):
        controller_pid = psutil.Process(os.getpid()).parent().parent().parent().parent().pid
        launcher_pid = psutil.Process(os.getpid()).parent().parent().parent().pid
        pid = str(controller_pid)+str(launcher_pid)

        if platform.system() == "Windows":
            self.uid = self.call_uid(launcher_pid)
        else:
            self.uid = self.call_uid(controller_pid)

        request_memory = f"request_memory_{self.uid}"
        response_memory = f"response_memory_{self.uid}"


        self.reception_running = False
        self.sending_running = False

        self.start_time = time.monotonic()
        self.time_step = time_step
        self.time_out = time_out

        self.robot = Supervisor()
        self.devices = {}

        self.close_sim = threading.Event()
        self.channel = Comm(buffer_size=SHM_SIZE, emitter_name=response_memory, receiver_name=request_memory,
                            close_event=self.close_sim)

    def main_cycle(self):
        try:
            while self.simulation_up():
                self.receiving()
                self.sending()
                self.closing_evaluation()
        except Exception as error:
            print(f'Error: {error}')
        finally:
            self.channel.close_connection()

    def simulation_up(self):
        return (self.robot.step(self.time_step) != -1) and (not self.close_sim.is_set())

    def sending(self):
        if not self.sending_running:
            self.sending_running = True
            send_thread = threading.Thread(target=self.send_obs)
            send_thread.start()

    def receiving(self):
        if not self.reception_running:
            self.start_time = time.monotonic()
            self.reception_running = True
            receive_thread = threading.Thread(target=self.receive_action)
            receive_thread.start()

    def closing_evaluation(self):
        if (time.monotonic() - self.start_time) > self.time_out:
            self.close_sim.set()

    def send_obs(self):
        try:
            observations = {}
            dev = self.devices  # Cacheamos la referencia para evitar acceder a self.devices en cada iteración.
            for sensor in SENSORS:
                device = dev[sensor]
                if sensor == "inertial unit":
                    # Se obtiene un cuaternión: [qx, qy, qz, qw].
                    observations[sensor] = np.array(device.getQuaternion(), dtype=np.float32)
                elif sensor == "gps":
                    # Estos sensores retornan un vector de valores.
                    observations[sensor] = np.array(device.getValues(), dtype=np.float32)
                elif sensor == "compass":
                    compass = device.getValues()
                    theta = np.arctan2(compass[1], compass[0])
                    observations[sensor] = np.array([np.cos(theta), np.sin(theta)], dtype=np.float32)
                else:
                    # Para el resto se asume un único valor.
                    observations[sensor] = np.array([device.getValue()], dtype=np.float32)
            self.channel.send(pickle.dumps(observations))
        except:
            pass
        finally:
            self.sending_running = False

    def receive_action(self):
        try:
            action = self.channel.receive()
            tag = action["ACTION"]
            params = action["PARAMS"]
            #print(tag, params)
            self.actions(tag, params)
        except:
            pass
        finally:
            self.reception_running = False

    def actions(self, tag, params:np.float32):
        if tag == "SET_ALL_MOTORS":
            for idx, motor in enumerate(ACTUATORS):
                self.devices[motor].setPosition(params[idx])
        elif tag == "RESET":
            self.robot.simulationReset()
            self.enable_everything()
        elif tag == "CLOSE_CONNECTION":
            self.close_sim.set()
            self.robot.simulationQuit(0)

    def enable_everything(self):
        for i in SENSORS:
            device = self.robot.getDevice(i)
            device.enable(self.time_step)
            self.devices.update({i: device})
        for j in ACTUATORS:
            device = self.robot.getDevice(j)
            device.setPosition(0)
            device.setVelocity(1.70068)
            self.devices.update({j: device})

    def end_simulation(self):
        self.robot.simulationQuit(0)


if __name__ == '__main__':
    server = RobotServer()
    try:
        print("Simulation Starting")
        server.enable_everything()
        server.main_cycle()
    except Exception as e:
        print(e)
    finally:
        time.sleep(10)
        server.end_simulation()
