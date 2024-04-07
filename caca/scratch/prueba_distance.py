from controller import Robot, DistanceSensor

def prueba():
    robot = Robot()
    sensor = robot.getDistanceSensor("distance sensor")
    sensor.enable(10)

    while robot.step(10) != -1:
        distance = sensor.getValue()
        print(distance, type(distance), sensor.getType())
