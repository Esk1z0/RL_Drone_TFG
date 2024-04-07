#Constantes xyz_controller
HOST = 'localhost'
PORT = 12000
TIME_OUT = 2


#Constantes Drone
WORLD_DIR = " ..\drone_library\drone-tfg-juanes\worlds\my_frst_webots_world.wbt"
MODE_FLAGS = " --no-rendering --batch --mode=realtime --minimize "
EXECUTE = "webots "

COMMAND = EXECUTE + MODE_FLAGS + WORLD_DIR

#Funciones
ACTIONS = [
    "TAKE_OFF",
    "LAND",
    "GET_TIME",
    "CLOSE_CONNECTION"
]
