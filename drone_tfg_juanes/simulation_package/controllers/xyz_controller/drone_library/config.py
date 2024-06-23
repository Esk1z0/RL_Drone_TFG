#Constantes xyz_controller
HOST = 'localhost'
PORT = 12000
TIME_OUT = 7

REQUEST_M = "request_memory"
RESPONSE_M = "response_memory"
SEM_REQUEST_M = "sem_request_memory"
SEM_RESPONSE_M = "sem_response_memory"
SHM_SIZE = 2048

TIME_STEP = 10
SENSORS = ["camera", "inertial unit", "distance sensor", "altimeter", "accelerometer"]
ACTUATORS = ["front left propeller", "front right propeller",
                     "rear left propeller", "rear right propeller"]


#Constantes Drone
MODE_FLAGS = " --batch --mode=realtime "# --no-rendering --minimize "
EXECUTE = "webots "

COMMAND = EXECUTE + MODE_FLAGS

#Funciones
ACTIONS = [
    "TAKE_OFF",
    "LAND",
    "RESET",
    "GET_TIME",
    "GET_IMU",
    "GET_DISTANCE",
    "GET_IMAGE",
    "GET_DATA",
    "SET_MOTOR_RL",
    "SET_MOTOR_RR",
    "SET_MOTOR_FL",
    "SET_MOTOR_FR",
    "SET_ALL_MOTORS",
    "CLOSE_CONNECTION",
    "GET_PRM"
]
