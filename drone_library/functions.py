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



def close_connection(robot, devices, message: str):
    time.sleep(0.5)
    return "closing_connection;"

FUNCTIONS = [
    take_off,
    land,
    get_time,
    close_connection
]

