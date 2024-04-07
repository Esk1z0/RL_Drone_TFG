from processes.iprocess import IProcess
from utils.EInputs import EInput
import numpy as np
from scipy.spatial.transform import Rotation
from utils.EDevices import EDevices

class IMUProcess(IProcess):

    MAX_ROTATION = 7
    MIN_ROTATION = -7


    def process_data(self, data):
        values = data.get(EDevices.IMU, 0)

        if values != 0:
            interval = data.get(EDevices.TimeInterval)
            pos = IMUProcess.rotation_scaler(IMUProcess.get_pos(values, interval))
            ang_vel = IMUProcess.rotation_scaler(IMUProcess.get_ang_vel(values, interval))
            data[EInput.IMUPosition] = pos
            data[EInput.IMUAngularVel] = ang_vel

        return data

    @staticmethod
    def get_pos(values, interval):
        return values[-1]

    @staticmethod
    def get_ang_vel(values, interval):
        q_1 = np.array(values[0])
        q_2 = np.array(values[-1])

        delta_q = q_1 * np.conjugate(q_2)
        delta_q /= np.linalg.norm(delta_q)
        delta_rotation = Rotation.from_quat(delta_q)

        rotation = delta_rotation.as_rotvec() / interval

        return rotation.to_list()


    @staticmethod
    def get_ang_accel(values, interval):
        pass

    @staticmethod
    def min_max_scaler(data, min_value, max_value):
        scaled_data = (data - min_value) / (max_value - min_value)
        if scaled_data > 1:
            scaled_data = 1
        elif scaled_data < 0:
            scaled_data = 0
        return scaled_data

    @staticmethod
    def rotation_scaler(rotation):
        for i in rotation:
            rotation[rotation.index(i)] = IMUProcess.min_max_scaler(i,
                                        IMUProcess.MIN_ROTATION, IMUProcess.MAX_ROTATION)
        return rotation
