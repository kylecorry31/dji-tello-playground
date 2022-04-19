def __bytes(cmd: str) -> bytes:
    return cmd.encode("utf-8")


def command() -> bytes:
    return __bytes("command")


def takeoff() -> bytes:
    return __bytes("takeoff")


def land() -> bytes:
    return __bytes("land")


def streamon() -> bytes:
    return __bytes("streamon")


def streamoff() -> bytes:
    return __bytes("streamoff")


def emergency() -> bytes:
    return __bytes("emergency")


def up(x: int) -> bytes:
    return __bytes("up {}".format(x))


def down(x: int) -> bytes:
    return __bytes("down {}".format(x))


def left(x: int) -> bytes:
    return __bytes("left {}".format(x))


def right(x: int) -> bytes:
    return __bytes("right {}".format(x))


def forward(x: int) -> bytes:
    return __bytes("forward {}".format(x))


def back(x: int) -> bytes:
    return __bytes("back {}".format(x))


def cw(x: int) -> bytes:
    return __bytes("cw {}".format(x))


def ccw(x: int) -> bytes:
    return __bytes("ccw {}".format(x))


def flip(x: chr) -> bytes:
    return __bytes("flip {}".format(x))


def go(x: int, y: int, z: int, speed: int) -> bytes:
    return __bytes("go {} {} {} {}".format(x, y, z, speed))


def curve(x1: int, y1: int, z1: int, x2: int, y2: int, z2: int, speed: int) -> bytes:
    return __bytes("curve {} {} {} {}".format(x1, y1, z1, x2, y2, z2, speed))


def speed(x: int) -> bytes:
    return __bytes("speed {}".format(x))


def rc(a: int, b: int, c: int, d: int) -> bytes:
    return __bytes("rc {} {} {} {}".format(a, b, c, d))


def wifi(ssid: str, password: str) -> bytes:
    return __bytes("wifi {} {}".format(ssid, password))


def read_speed() -> bytes:
    return __bytes("speed?")


def read_battery() -> bytes:
    return __bytes("battery?")


def read_time() -> bytes:
    return __bytes("time?")


def read_height() -> bytes:
    return __bytes("height?")


def read_temp() -> bytes:
    return __bytes("temp?")


def read_attitude() -> bytes:
    return __bytes("attitude?")


def read_baro() -> bytes:
    return __bytes("baro?")


def read_acceleration() -> bytes:
    return __bytes("acceleration?")


def read_tof() -> bytes:
    return __bytes("tof?")


def read_wifi() -> bytes:
    return __bytes("wifi?")
