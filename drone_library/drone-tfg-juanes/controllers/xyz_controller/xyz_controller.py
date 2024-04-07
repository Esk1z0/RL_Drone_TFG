import sys
import json
import socket
import threading
import time
from controller import Robot, Supervisor
from drone_library import ACTIONS, PORT, HOST, TIME_OUT
from drone_library.functions import FUNCTIONS, Connection_End, Connection_Timeout


class DroneServer:
    def __init__(self):
        self.robot = Supervisor()
        self.server_socket = None
        self.reception_running = False
        self.start_time = time.monotonic()
        self.close_sim = False
        self.ACTIONS_CONVERT = dict(zip(ACTIONS, FUNCTIONS))


    def start(self):
        self.server_socket = self.initialize_API()
        self.main_cycle()


    def main_cycle(self):
        try:
            conn = self.receive_conn()
            while self.robot.step(10) != -1:
                connection_action = threading.Thread(target=self.attend_message, args=[conn])
                if not self.reception_running:
                    print("webo")
                    self.reception_running = True
                    connection_action.start()
                if ((time.monotonic() - self.start_time) > TIME_OUT) or self.close_sim:
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
                response = func(self.robot, message['PARAMS'])  # ejecución de la acción y respuesta
                conn.sendall(response.encode())
                if response == "closing_connection;":
                    self.close_sim = True
            else:
                print(f'Error: Función no encontrada para la acción {message["ACTION"]}')
        self.reception_running = False

    def initialize_API(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((HOST, PORT))
        server_socket.listen(1)
        server_socket.settimeout(TIME_OUT)
        print("Servidor socket iniciado en {}:{}".format(HOST, PORT))
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
        server.start()
        server.end_simulation()
    except Exception as e:
        print(e)
        server.end_simulation()
