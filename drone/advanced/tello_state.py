class State:
    def __init__(self, pitch: float, roll: float, yaw: float, vgx: float, vgy: float, vgz: float, templ: float,
                 temph: float, tof: float, h: float, bat: float, baro: float, time: float, agx: float, agy: float,
                 agz: float):
        self.agz = agz
        self.agy = agy
        self.agx = agx
        self.time = time
        self.baro = baro
        self.bat = bat
        self.h = h
        self.tof = tof
        self.temph = temph
        self.templ = templ
        self.vgz = vgz
        self.vgy = vgy
        self.vgx = vgx
        self.yaw = yaw
        self.roll = roll
        self.pitch = pitch


def empty_state() -> State:
    return State(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)


def parse_state(state: bytes) -> State:
    state_str = state.decode('ascii').strip()[:-1]
    parsed = list(map(lambda s: parse_value(s), state_str.split(';')))
    values = {}
    for value in parsed:
        values[value[0]] = value[1]
    return State(values['pitch'], values['roll'], values['yaw'], values['vgx'], values['vgy'], values['vgz'],
                 values['templ'], values['temph'], values['tof'], values['h'], values['bat'], values['baro'],
                 values['time'], values['agx'], values['agy'], values['agz'])


def parse_value(value: str) -> [str, float]:
    split = value.split(":")
    return [split[0], float(split[1])]
