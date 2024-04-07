import json
import socket

class ServerCommunication:
    def __init__(self, server_ip, server_port):
        self.server_ip = server_ip
        self.server_port = server_port
        self.sock = None

    def connect_tcp(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.server_ip, self.server_port))

    def connect_udp(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send_message(self, message):
        if not self.sock:
            raise Exception("Socket not connected")

        if isinstance(message, dict):
            message = json.dumps(message)
        self.sock.sendto(message.encode(), (self.server_ip, self.server_port))

    def receive_message(self):
        if not self.sock:
            raise Exception("Socket not connected")

        if self.sock.type == socket.SOCK_STREAM:
            return self.sock.recv(1024).decode()
        elif self.sock.type == socket.SOCK_DGRAM:
            data, _ = self.sock.recvfrom(1024)
            return data.decode()

    def close_connection(self):
        if self.sock:
            self.sock.close()
            self.sock = None

def main():
    # Ejemplo de uso
    server_ip = '127.0.0.1'
    server_port = 10000

    communication = ServerCommunication(server_ip, server_port)
    communication.connect_udp()

    message  = {'IMU': [0.99999, 0.99999, 0.99999],  'Accel': [0.99999, 0.99999, 0.99999]}
    message = json.dumps(message)
    for i in range(10):
        communication.send_message(message)

    #received_message = communication.receive_message()
    #print("Received message:", received_message)

    communication.close_connection()

if __name__ == '__main__':
    main()