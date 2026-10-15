# represents a measurement from the pipe pressure sensor, with pressure and time
class Global_measurement():

        def __init__(self, pressure: float, time: float):
        self.pressure = pressure
        self.time = time