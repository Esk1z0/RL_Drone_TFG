import threading
import time
import pickle
from controller import Supervisor
import numpy as np

from drone_library.config import TIME_OUT, TIME_STEP, ACTUATORS, SENSORS, SHM_SIZE, get_next_instance_name

from drone_library.SharedMemoryCommunication import Comm


class DroneServer:
    def __init__(self, time_out=TIME_OUT, time_step=TIME_STEP):
        REQUEST_MEMORY, RESPONSE_MEMORY = get_next_instance_name(is_client=False)
        print(REQUEST_MEMORY, RESPONSE_MEMORY)
        self.reception_running = False
        self.sending_running = False

        self.start_time = time.monotonic()
        self.time_step = time_step
        self.time_out = time_out

        self.robot = Supervisor()
        self.devices = {}

        self.close_sim = threading.Event()
        self.channel = Comm(buffer_size=SHM_SIZE, emitter_name=RESPONSE_MEMORY, receiver_name=REQUEST_MEMORY,
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
            self.channel.send(pickle.dumps({
                "camera": bytearray(self.devices["camera"].getImage()),
                "inertial unit": self.devices["inertial unit"].getQuaternion(),
                "left distance sensor": self.devices["left distance sensor"].getValue(),
                "right distance sensor": self.devices["right distance sensor"].getValue(),
                "altimeter": self.devices["altimeter"].getValue(),
                "accelerometer": self.devices["accelerometer"].getValues()
            }))
        except:
            pass
        finally:
            self.sending_running = False

    def receive_action(self):
        try:
            action = self.channel.receive()
            print(action)#TODO borrar
            tag = action["ACTION"]
            params = action["PARAMS"]
            self.actions(tag, params)
        except:
            pass
        finally:
            self.reception_running = False

    def actions(self, tag, params:np.float32):
        if tag == "SET_ALL_MOTORS":
            motor_rl = self.devices['rear left propeller']
            motor_rr = self.devices['rear right propeller']
            motor_fl = self.devices['front left propeller']
            motor_fr = self.devices['front right propeller']

            motor_rl.setVelocity(-params[0])
            motor_rr.setVelocity(params[1])
            motor_fl.setVelocity(params[2])
            motor_fr.setVelocity(-params[3])
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
            device.setPosition(float('inf'))
            device.setVelocity(1)
            self.devices.update({j: device})

    def end_simulation(self):
        self.robot.simulationQuit(0)


if __name__ == '__main__':
    server = DroneServer()
    try:
        print("Simulation Starting")
        server.enable_everything()
        server.main_cycle()
    except Exception as e:
        print(e)
    finally:
        time.sleep(10)
        server.end_simulation()
