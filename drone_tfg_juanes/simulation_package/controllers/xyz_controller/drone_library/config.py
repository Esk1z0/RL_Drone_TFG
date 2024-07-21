import os

# Constantes xyz_controller
TIME_OUT = 7
TIME_STEP = 10

SHM_SIZE = 2048

REQUEST_MEMORY = "request_memory_{}"
RESPONSE_MEMORY = "response_memory_{}"

# Memory Names for shared memory
COUNTER_FILE = "instance_counter.txt"
COUNTER_THRESHOLD = 100

if not os.path.exists(COUNTER_FILE):
    with open(COUNTER_FILE, "w") as f:
        f.write("0")

def get_next_instance_name():

    with open(COUNTER_FILE, "r") as f:
        counter = int(f.read())

    counter += 1

    if counter >= COUNTER_THRESHOLD:
        counter = 0

    with open(COUNTER_FILE, "w") as f:
        f.write(str(counter))

    # Generar un nombre único para la instancia
    return REQUEST_MEMORY.format(counter), RESPONSE_MEMORY.format(counter)




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

