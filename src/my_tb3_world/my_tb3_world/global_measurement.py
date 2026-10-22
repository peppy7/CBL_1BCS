# represents a measurement from the pipe pressure sensor, with pressure and time
# represented by cell_x, cell_y = -1,-1
class Global_measurement():

        def __init__(self, pressure: float, time: float):
        self.pressure = pressure
        self.time = time