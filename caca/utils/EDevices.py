from enum import Enum


class EDevices(Enum):
    IMU = "IMU"
    DistanceSensor = "DistanceSensor"
    Camera = "Camera"
    TEXT = "Text"

    TimeSend = "TimeSend"