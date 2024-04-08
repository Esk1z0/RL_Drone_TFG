import sys
import json
import socket
import threading
import time
from controller import Supervisor, Camera
from drone_library import ACTIONS, PORT, HOST, TIME_OUT, TIME_STEP, ACTUATORS, SENSORS
from drone_library.functions import FUNCTIONS, Connection_End, Connection_Timeout


class DroneServer:
    def __init__(self, port=PORT, host=HOST, time_out=TIME_OUT, time_step=TIME_STEP):
        self.server_socket = None
        self.reception_running = False

        self.start_time = time.monotonic()
        self.time_step = time_step
        self.time_out = time_out

        self.host = host
        self.port = port

        self.robot = Supervisor()
        self.devices = {}



        self.close_sim = False
        self.ACTIONS_CONVERT = dict(zip(ACTIONS, FUNCTIONS))


    def start(self):
        self.server_socket = self.initialize_API()
        self.main_cycle()


    def main_cycle(self):
        try:
            conn = self.receive_conn()
            while self.robot.step(self.time_step) != -1:
                connection_action = threading.Thread(target=self.attend_message, args=[conn])
                if not self.reception_running:
                    self.reception_running = True
                    connection_action.start()
                if (((not self.time_out == 0) and (time.monotonic() - self.start_time) > self.time_out)) or self.close_sim:
                    break
        except Exception as e:
            print(f'Error: {e}')
        finally:
            if self.server_socket:
                self.close_connection()

    def attend_message(self, conn):
        aux = self.receive_until_semicolon(conn)
        if aux is not None:
            self.start_time = time.monotonic()
            message = json.loads(aux)
            print(message.get('ACTION'))
            func = self.ACTIONS_CONVERT.get(message['ACTION'])  # decodificación de la acción
            if func:
                response = func(self.robot, self.devices, message['PARAMS'])  # ejecución de la acción y respuesta
                conn.sendall(response.encode())
                if response == "closing_connection;":
                    self.close_sim = True
            else:
                print(f'Error: Función no encontrada para la acción {message["ACTION"]}')
        self.reception_running = False

    def initialize_API(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.host, self.port))
        server_socket.listen(1)
        if(not self.time_out == 0):
            server_socket.settimeout(self.time_out)
        print("Servidor socket iniciado en {}:{}".format(self.host, self.port))
        return server_socket

    def receive_conn(self) -> (socket.socket, float):
        conn, addr = self.server_socket.accept()
        print("Nueva conexión entrante desde:", addr)
        self.start_time = time.monotonic()
        return conn

    def receive_until_semicolon(self, conn):
        try:
            data_received = b''  # Inicializamos una variable para almacenar los datos recibidos
            while True:
                chunk = conn.recv(1024)  # Recibimos datos del socket en bloques de 1024 bytes
                if not chunk:
                    break  # Si no hay más datos para recibir, salimos del bucle
                data_received += chunk
                if b';' in chunk:
                    break  # Si encontramos un punto y coma en los datos recibidos, salimos del bucle

            value = data_received.decode()
            value = value.replace(';', ' ')
            return value
        except socket.timeout:
            raise Exception("Se ha producido un tiempo de espera durante la recepción de datos.")

    def enable_everything(self):
        for i in SENSORS:
            device = self.robot.getDevice(i)
            device.enable(self.time_step)
            self.devices.update({i: device})
        for j in ACTUATORS:
            device = self.robot.getDevice(j)
            self.devices.update({j: device})

    def close_connection(self):
        if self.server_socket:
            self.server_socket.close()
            print("Cerrando Simulación")

    def end_simulation(self):
        self.robot.simulationQuit(0)


if __name__ == '__main__':
    try:
        print(sys.version)
        server = DroneServer()
        server.enable_everything()
        server.start()
        server.end_simulation()
    except Exception as e:
        print(e)
        server.end_simulation()
