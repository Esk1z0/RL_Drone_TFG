#Funciones que ejecuta el socket sobre Robot
import time
from controller.camera import Camera


class Connection_End(Exception):
    """Clase para un error personalizado"""

    def __init__(self, mensaje="Se Cerró la Conexión"):
        self.mensaje = mensaje
        super().__init__(self.mensaje)

class Connection_Timeout(Exception):
    """Clase para un error personalizado"""

    def __init__(self, mensaje="Mucho tiempo sin peticiones"):
        self.mensaje = mensaje
        super().__init__(self.mensaje)



def take_off(robot, devices, message: str):
    return "taking off;"

def land(robot, devices, message: str):
    return "landing;"

def get_time(robot, devices, message: str):
    return str(robot.getTime())+";"

def get_image(robot, devices, message: str):
    cam = devices.get("camera")
    arr = cam.getImageArray()
    return [[sum(pixel) // 3 for pixel in row] for row in arr]

def close_connection(robot, devices, message: str):
    robot.simulationQuit(0)
    return "CLOSE_CONNECTION"

FUNCTIONS = [
    take_off,
    land,
    get_time,
    get_image,
    close_connection
]

