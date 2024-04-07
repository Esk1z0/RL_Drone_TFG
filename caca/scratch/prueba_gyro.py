from controller import Robot
def prueba():
    robot = Robot()

    imu = robot.getInertialUnit("inertial unit")
    imu.enable(10)

    while robot.step(10) != -1:
        imu_values = imu.getQuaternion()
        print("Gyro values: ", imu_values, type(imu_values), imu_values[0], type(imu_values[0]))

