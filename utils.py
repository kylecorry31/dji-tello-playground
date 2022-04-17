import math


def delta_angle(angle1: float, angle2: float) -> float:
    delta = angle2 - angle1
    delta += 180
    delta -= math.floor(delta / 360) * 360
    delta -= 180
    if abs(abs(delta) - 180) <= 0.0001:
        delta = 180
    return delta


def clamp(value: float, minimum: float, maximum: float) -> float:
    return min(maximum, max(minimum, value))


def rotate(vector, angle):
    cos_angle = math.cos(math.radians(angle))
    sin_angle = math.sin(math.radians(angle))
    x = vector[0] * cos_angle - vector[1] * sin_angle
    y = vector[0] * sin_angle + vector[1] * cos_angle
    return x, y
