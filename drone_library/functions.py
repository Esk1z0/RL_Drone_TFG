#Funciones que ejecuta el socket sobre Robot
import time


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



def take_off(message: str):
    return "taking off;"

def land(message: str):
    return "landing;"

def close_connection(message: str):
    time.sleep(0.5)
    return Connection_End

FUNCTIONS = [
    take_off,
    land,
    close_connection
]

