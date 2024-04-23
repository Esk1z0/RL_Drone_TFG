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
    return "taking off"

def land(robot, devices, message: str):
    return "landing"

def get_time(robot, devices, message: str):
    return str(robot.getTime())

def provisional_message(robot, devices, message: str):
    return b"Lorem ipsum dolor sit amet, " \
           b"consectetur adipiscing elit. Sed vel nisl non orci vehicula posuere. " \
           b"Nullam auctor, leo ut bibendum pellentesque, libero ligula vulputate quam, " \
           b"non bibendum lorem eros ac justo. Quisque sed tellus ullamcorper, " \
           b"fermentum lacus non, consequat sem. Aliquam id arcu sit amet ligula cursus vehicula sit amet non ex." \
           b" Duis scelerisque risus nec est congue, nec ullamcorper turpis volutpat. Nulla in tortor vel velit faucibus vehicula. " \
           b"Maecenas sed bibendum lacus"

def get_image(robot, devices, message: str):
    cam = devices["camera"]
    return cam.getImage()

    #return [[sum(pixel) // 3 for pixel in row] for row in arr]

def close_connection(robot, devices, message: str):
    robot.simulationQuit(0)
    return "CLOSE_CONNECTION"

FUNCTIONS = [
    take_off,
    land,
    get_time,
    provisional_message,
    get_image,
    close_connection
]

