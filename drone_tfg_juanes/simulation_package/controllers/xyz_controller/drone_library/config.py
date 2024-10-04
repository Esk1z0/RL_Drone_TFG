import os

# Constantes xyz_controller
TIME_OUT = 15
TIME_STEP = 10

SHM_SIZE = 2048


REQUEST_MEMORY = "request_memory_{}"
RESPONSE_MEMORY = "response_memory_{}"

CONFIG_DIR = os.path.join(os.path.dirname(__file__), 'config')
COUNTER_FILE = os.path.join(CONFIG_DIR, "instance_counter.txt")
os.makedirs(CONFIG_DIR, exist_ok=True)

COUNTER_THRESHOLD = 100

if not os.path.exists(COUNTER_FILE):
    with open(COUNTER_FILE, "w") as f:
        f.write("0\n0")  # Dos líneas: una para el cliente y otra para el servidor
    print(f"Archivo de contador creado en {COUNTER_FILE} con valores iniciales 0, 0.")
else:
    print(f"Archivo de contador ya existe en {COUNTER_FILE}.")


def get_next_instance_name(is_client=True):
    with open(COUNTER_FILE, "r") as g:
        lines = g.readlines()
        client_counter = int(lines[0].strip())
        server_counter = int(lines[1].strip())
        #print(f"Valores actuales de los contadores - Cliente: {client_counter}, Servidor: {server_counter}")

    if is_client:
        client_counter += 1
        if client_counter >= COUNTER_THRESHOLD:
            client_counter = 0
        lines[0] = f"{client_counter}\n"
    else:
        server_counter += 1
        if server_counter >= COUNTER_THRESHOLD:
            server_counter = 0
        lines[1] = f"{server_counter}\n"

    with open(COUNTER_FILE, "w") as g:
        g.writelines(lines)
        #print(f"Nuevos valores de los contadores guardados - Cliente: {client_counter}, Servidor: {server_counter}")

    if is_client:
        request_name = REQUEST_MEMORY.format(client_counter)
        response_name = RESPONSE_MEMORY.format(client_counter)
    else:
        request_name = REQUEST_MEMORY.format(server_counter)
        response_name = RESPONSE_MEMORY.format(server_counter)

    print(f"Nombres generados: {request_name}, {response_name}")

    return request_name, response_name


SENSORS = ["camera", "inertial unit", "left distance sensor",
           "right distance sensor", "altimeter", "accelerometer", "GPS"]
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
