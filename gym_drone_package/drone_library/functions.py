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

def reset_simulation(robot, devices, message: str):
    robot.simulationReset()
    return "restarted"

def get_time(robot, devices, message: str):
    return str(robot.getTime())

def get_imu(robot, devices, message: str):
    imu = devices["inertial unit"]
    return imu.getQuaternion()


def get_distance(robot, devices, message: str):
    distance_sensor = devices["distance sensor"]
    return distance_sensor.getValue()

def get_image(robot, devices, message):
    cam = devices["camera"]
    return cam.getImage()

def get_data(robot, devices, message):
    return {
        "camera": bytearray(get_image(robot, devices, message)),
        "imu": get_imu(robot, devices, message),
        "distance": get_distance(robot, devices, message)
    }

def set_MotorRL(robot, devices, message):
    motor = devices['rear left propeller']
    motor.setVelocity(-message["velocity"])
    return "OK_VEL"

def set_MotorRR(robot, devices, message):
    motor = devices['rear right propeller']
    motor.setVelocity(message["velocity"])
    return "OK_VEL"

def set_MotorFL(robot, devices, message):
    motor = devices['front left propeller']
    motor.setVelocity(message["velocity"])
    return "OK_VEL"

def set_MotorFR(robot, devices, message):
    motor = devices['front right propeller']
    motor.setVelocity(-message["velocity"])
    return "OK_VEL"

def set_vel_motors(robot, devices, message):
    motor_rl = devices['rear left propeller']
    motor_rr = devices['rear right propeller']
    motor_fl = devices['front left propeller']
    motor_fr = devices['front right propeller']

    motor_rl.setVelocity(-message[0])
    motor_rr.setVelocity(message[1])
    motor_fl.setVelocity(message[2])
    motor_fr.setVelocity(-message[3])
    return "OK_VEL"

def close_connection(robot, devices, message):
    robot.simulationQuit(0)
    return "CLOSE_CONNECTION"


def provisional_message(robot, devices, message):
    return b"Lorem ipsum dolor sit amet, " \
           b"consectetur adipiscing elit. Sed vel nisl non orci vehicula posuere. " \
           b"Nullam auctor, leo ut bibendum pellentesque, libero ligula vulputate quam, " \
           b"non bibendum lorem eros ac justo. Quisque sed tellus ullamcorper, " \
           b"fermentum lacus non, consequat sem. Aliquam id arcu sit amet ligula cursus vehicula sit amet non ex." \
           b" Duis scelerisque risus nec est congue, nec ullamcorper turpis volutpat. Nulla in tortor vel velit faucibus vehicula. " \
           b"Maecenas sed bibendum lacus"

FUNCTIONS = [
    take_off,
    land,
    reset_simulation,
    get_time,
    get_imu,
    get_distance,
    get_image,
    get_data,
    set_MotorRL,
    set_MotorRR,
    set_MotorFL,
    set_MotorFR,
    set_vel_motors,
    close_connection,
    provisional_message
]

