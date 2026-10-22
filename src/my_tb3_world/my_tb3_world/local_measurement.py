# represents a measurement from the pressure sensor, with pressure, time and cell coordinate
class Local_measurement():

        def __init__(self, pressure: float, time: float, cell_x: int, cell_y: int):
                self.pressure = pressure
                self.time = time
                self.cell_x = cell_x
                self.cell_y = cell_y