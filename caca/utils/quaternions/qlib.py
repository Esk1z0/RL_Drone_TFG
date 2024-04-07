import math
import numpy as np

class qlib:
    def __init__(self):
        pass

    def norm(self, quaternion):
        return math.sqrt(sum(componente ** 2 for componente in quaternion))

    def normalize(self, quaternion):
        normal = self.norm(quaternion)
        return [component / normal for component in quaternion]
    def complementary(self, quaternion):
        result = quaternion
        for elemento in range(len(quaternion)):
            if elemento > 0:
                result[elemento] = -quaternion[elemento]

        return result

    def inverse(self, quaternion):
        norm = self.norm(quaternion)**2
        return [comp / norm for comp in self.complementary(quaternion)]

    def product(self, q1, q2):
        array_2 = np.array(q2)
        array_1 = np.array([
            [q1[0], -q1[1], -q1[2], -q1[3]],
            [q1[1], q1[0], -q1[3], q1[2]],
            [q1[2], q1[3], q1[0], -q1[1]],
            [q1[3], -q1[2], q1[1], q1[0]]
        ])

        return list(array_1 @ array_2)



if __name__ == '__main__':
    q1 = [0.0, -0.1, -0.8, 0.1]

    quat = qlib()
    print(q1)
    print(quat.norm(q1))
    print(quat.normalize(q1))
    print(quat.complementary(q1))
    print(quat.inverse(q1))
    print(quat.product(q1, quat.inverse(q1)))
