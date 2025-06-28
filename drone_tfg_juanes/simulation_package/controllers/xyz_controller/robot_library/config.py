# Constantes xyz_controller
TIME_OUT = 3000
TIME_STEP = 1
SHM_SIZE = 2048

SENSORS = ["back_left_1_sensor",
           "back_left_2_sensor",
           "back_left_3_sensor",
           "back_right_1_sensor",
           "back_right_2_sensor",
           "back_right_3_sensor",
           "front_left_1_sensor",
           "front_left_2_sensor",
           "front_left_3_sensor",
           "front_right_1_sensor",
           "front_right_2_sensor",
           "front_right_3_sensor",
           "head_sensor",
           "neck_1_sensor",
           "neck_2_sensor",
           "pelvis_sensor",
           "inertial unit",
           "gps",
           "compass"]

ACTUATORS = ["back_left_1",
             "back_left_2",
             "back_left_3",
             "back_right_1",
             "back_right_2",
             "back_right_3",
             "front_left_1",
             "front_left_2",
             "front_left_3",
             "front_right_1",
             "front_right_2",
             "front_right_3",
             "head",
             "neck_1",
             "neck_2",
             "pelvis"]

# Command constants
WIN_BASE_COMMAND = "webots"
LINUX_BASE_COMMAND = "xvfb-run -a -s \"-screen 0 1024x768x24\" webots" #"xvfb-run webots"
FLAGS = {
    "batch": " --batch",
    "realtime": " --mode=realtime",
    "fast": " --mode=fast",
    "no_rendering": " --no-rendering",
    "minimize": " --minimize",
    "stdout": " --stdout",
    "stderr": " --stderr"
}