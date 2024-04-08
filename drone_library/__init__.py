#Constantes xyz_controller
HOST = 'localhost'
PORT = 12000
TIME_OUT = 3
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
    "CLOSE_CONNECTION"
]
