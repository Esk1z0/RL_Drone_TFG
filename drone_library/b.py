
import socket

HOST = "localhost"  # The server's hostname or IP address
PORT = 12000  # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b'{"ACTION" : "TAKE_OFF" , "PARAMS" : "a"};')
    data = s.recv(1024)
    print(f"Received {data!r}")


