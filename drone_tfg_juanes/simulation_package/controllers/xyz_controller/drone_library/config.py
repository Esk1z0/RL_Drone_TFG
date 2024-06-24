# Constantes xyz_controller


TIME_OUT = 7
TIME_STEP = 10

REQUEST_M = "request_memory"
RESPONSE_M = "response_memory"
SEM_REQUEST_M = "sem_request_memory"
SEM_RESPONSE_M = "sem_response_memory"
SHM_SIZE = 2048




SENSORS = ["camera", "inertial unit", "distance sensor", "altimeter", "accelerometer"]
ACTUATORS = ["front left propeller", "front right propeller",
             "rear left propeller", "rear right propeller"]

# Command constants
FLAGS = {
    "batch": " --batch",
    "realtime": " --mode=realtime",
    "fast": "--mode=fast",
    "no_rendering": " --no-rendering",
    "minimize": " --minimize"
}

BASE_COMMAND = "webots"

