from controller import Robot
import pandas as pd

def prueba():
    robot = Robot()

    imu = robot.getDevice("inertial unit")
    imu.enable(10)

    df = pd.DataFrame({"first":[], "second":[], "third":[], "fourth":[]})
    lista = []
    while robot.step(10) != -1:
        imu_values = imu.getQuaternion()
        print("Gyro values: ", imu_values, type(imu_values))
        df.loc[len(df)] = imu_values
    df.to_csv("../imu_data_sample.csv")