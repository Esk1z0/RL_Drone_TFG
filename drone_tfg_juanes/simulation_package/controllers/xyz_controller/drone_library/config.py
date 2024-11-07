# Constantes xyz_controller
TIME_OUT = 90
TIME_STEP = 10
SHM_SIZE = 2048

SENSORS = ["camera",
           "inertial unit",
           "left distance sensor",
           "right distance sensor",
           "altimeter",
           "accelerometer",
           "GPS"]

ACTUATORS = ["front left propeller",
             "front right propeller",
             "rear left propeller",
             "rear right propeller"]

# Command constants
WIN_BASE_COMMAND = "webots"
LINUX_BASE_COMMAND = "xvfb-run webots"
FLAGS = {
    "batch": " --batch",
    "realtime": " --mode=realtime",
    "fast": "--mode=fast",
    "no_rendering": " --no-rendering",
    "minimize": " --minimize",
    "stdout": " --stdout",
    "stderr": " --stderr"
}