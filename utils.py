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
