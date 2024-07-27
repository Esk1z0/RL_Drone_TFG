import math

class Quaternion:
    def __init__(self, w, x, y, z):
        self.w = w
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return f"Quaternion({self.w}, {self.x}, {self.y}, {self.z})"

    def __mul__(self, other):
        if isinstance(other, Quaternion):
            w = self.w * other.w - self.x * other.x - self.y * other.y - self.z * other.z
            x = self.w * other.x + self.x * other.w + self.y * other.z - self.z * other.y
            y = self.w * other.y - self.x * other.z + self.y * other.w + self.z * other.x
            z = self.w * other.z + self.x * other.y - self.y * other.x + self.z * other.w
            return Quaternion(w, x, y, z)
        else:
            raise ValueError("Multiplication is only supported between two quaternions")

    def conjugate(self):
        return Quaternion(self.w, -self.x, -self.y, -self.z)

    def norm(self):
        return math.sqrt(self.w ** 2 + self.x ** 2 + self.y ** 2 + self.z ** 2)

    def normalize(self):
        norm = self.norm()
        if norm == 0:
            raise ZeroDivisionError("Cannot normalize a quaternion with zero norm")
        return Quaternion(self.w / norm, self.x / norm, self.y / norm, self.z / norm)

    def inverse(self):
        norm_sq = self.norm() ** 2
        if norm_sq == 0:
            raise ZeroDivisionError("Cannot invert a quaternion with zero norm")
        conjugate = self.conjugate()
        return Quaternion(conjugate.w / norm_sq, conjugate.x / norm_sq, conjugate.y / norm_sq, conjugate.z / norm_sq)

    def angle_with(self, other):
        dot_product = (self.w * other.w + self.x * other.x + self.y * other.y + self.z * other.z)
        norms = self.norm() * other.norm()
        if norms == 0:
            raise ZeroDivisionError("Cannot calculate angle with a quaternion with zero norm")
        cos_theta = dot_product / norms
        # Clamping value to avoid domain errors in acos
        cos_theta = max(-1.0, min(1.0, cos_theta))
        return math.degrees(math.acos(cos_theta))

    def rotate_vector(self, vector):
        vector_quat = Quaternion(0, vector[0], vector[1], vector[2])
        rotated_vector = self * vector_quat * self.inverse()
        return [rotated_vector.x, rotated_vector.y, rotated_vector.z]

def from_axis_angle(axis, angle_degrees):
    angle_radians = math.radians(angle_degrees)
    half_angle = angle_radians / 2
    sin_half_angle = math.sin(half_angle)
    w = math.cos(half_angle)
    x = axis[0] * sin_half_angle
    y = axis[1] * sin_half_angle
    z = axis[2] * sin_half_angle
    return Quaternion(w, x, y, z)
