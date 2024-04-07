from controller import Robot, Motor

def prueba():
    robot = Robot()

    vel = 200

    motor1 = robot.getDevice("front left propeller") #rear left propeller
    motor1.setPosition(float('inf'))
    motor1.setVelocity(vel)

    motor2 = robot.getDevice("rear left propeller")  # rear left propeller
    motor2.setPosition(float('inf'))
    motor2.setVelocity(vel)

    motor3 = robot.getDevice("front right propeller")  # rear left propeller
    motor3.setPosition(float('inf'))
    motor3.setVelocity(vel)

    motor4 = robot.getDevice("rear right propeller")  # rear left propeller
    motor4.setPosition(float('inf'))
    motor4.setVelocity(vel)

    while robot.step(10) != -1:
        pass