from my_tb3_world.local_measurement import Local_measurement
from my_tb3_world.global_measurement import Global_measurement
from my_tb3_world.cell import Cell

# describes the entire prediction model, with all cells and taking in all input
class Pressure_prediction_model():

    def __init__(self, x: int, y: int, initial_measurement: Global_measurement, logger):
        self.pressure_matrix = self.cell_matrix(x, y, float(1), initial_measurement.time)
        self.fouling_rate = 0.05 # initial fouling rate, will be changed slowly
        self.global_sensor_trust = 0.5 # how much to use new measurement compared to old, in [0,1]
        self.delta = 1.0 # timestep for updating
        self.time_last_global_measurement = initial_measurement.time
        self.last_global_measurement = initial_measurement
        self.cleanThreshhold = 0.3 # below what level is a cell considered dirty
        self.cleanQueue = []
        self.logger = logger

    # lowers the pressure of every cell by a bit to mimic fouling
    def update(self):

        # update cells
        for collumn in self.pressure_matrix:
            for cell in collumn:
                cell.pressure = cell.pressure - self.fouling_rate * self.delta
                if cell.pressure <= 0.0:
                    cell.pressure = 0.0

        # check if cells need to be cleaned
        for collumn in self.pressure_matrix:
            for cell in collumn:
                cell.pressure = cell.pressure - self.fouling_rate * self.delta
                if cell.pressure < self.cleanThreshhold and not (cell in self.cleanQueue):
                    self.cleanQueue.append(cell)

        # log all pressures
        logMatrix = [
            [cell.pressure for cell in row]
            for row in self.pressure_matrix
        ]

        self.logger.info(f'logging matrix')
        for i in range(len(self.pressure_matrix[0])):
            printStr = ""
            for j in range(len(self.pressure_matrix)):
                printStr = printStr + " " + str(self.pressure_matrix[j][i].pressure)
            self.logger.info(f'matrix log: {printStr}')

    # takes a local measurement and sets the cell accordingly
    def handle_local_measurement(self, local_measurement: Local_measurement):
        m = measurement
        self.pressure_matrix[m.x][m.y].pressure = m.pressure
        self.pressure_matrix[m.x][m.y].time_last_measurement = 0.0

    # takes a global measurement and adapts the fouling rate accordingly
    def handle_global_measurement(self, global_measurement: Global_measurement):
        g_last = self.last_global_measurement

        # difference in pressure
        d_pressure = global_measurement.pressure - g_last.pressure

        # difference in time
        d_time = global_measurement.time - g_last.time

        # new pressure is weighted average of predicted and previous
        self.fouling_rate = global_sensor_trust * (d_pressure/d_time) + (1 - global_sensor_trust) * fouling_rate

        # update parameters
        self.last_global_measurement = global_measurement
        self.time_last_global_measurement = global_measurement.time

    def get_cleaning_goal(self):
        return self.cleanQueue.pop(0)

    # returns a matrix filled with cells at a certain pressure
    def cell_matrix(self, x: int, y: int, pressure: float, time_last_measurement: float):
        return [
            [Cell(x, y, pressure, time_last_measurement) for j in range(y)]
            for i in range(x)
        ]