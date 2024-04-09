#Constantes xyz_controller
HOST = 'localhost'
PORT = 12000
TIME_OUT = 3

REQUEST_M = "request_memory"
RESPONSE_M = "response_memory"
SEM_REQUEST_M = "sem_request_memory"
SEM_RESPONSE_M = "sem_response_memory"
SHM_SIZE = 1024

TIME_STEP = 10
SENSORS = ["camera", "inertial unit", "distance sensor"]
ACTUATORS = ["front left propeller", "front right propeller",
                     "rear left propeller", "rear right propeller"]


#Constantes Drone
WORLD_DIR = " ..\drone_library\drone-tfg-juanes\worlds\my_frst_webots_world.wbt"
MODE_FLAGS = " --no-rendering --batch --mode=realtime "#--minimize "
EXECUTE = "webots "

COMMAND = EXECUTE + MODE_FLAGS + WORLD_DIR

#Funciones
ACTIONS = [
    "TAKE_OFF",
    "LAND",
    "GET_TIME",
    "GET_IMAGE",
    "CLOSE_CONNECTION"
]
