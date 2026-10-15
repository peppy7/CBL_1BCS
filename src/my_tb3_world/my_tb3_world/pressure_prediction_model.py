from local_measurement import Local_measurement
from global_measurement import Global_measurement

# describes the entire prediction model, with all cells and taking in all input
class Pressure_prediction_model():

    def __init__(self, x: int, y: int, initial_measurement: Global_measurement):
        self.pressure_matrix = cell_matrix(x, y)
        self.fouling_rate = 0.05 # initial fouling rate, will be changed slowly
        self.global_sensor_trust = 0.5 # how much to use new measurement compared to old, in [0,1]
        self.delta = 1.0 # timestep for updating
        self.time_last_global_measurement = self.get_clock().now().nanoseconds
        self.last_global_measurement = initial_measurement

        self.timer = self.create_timer(delta, self.update)

    # lowers the pressure of every cell by a bit to mimic fouling
    def update(self):
        for collumn in pressure_matrix:
            for cell in collumn:
                cell.pressure = cell.pressure - fouling_rate * delta
                if cell.pressure < 0.0:
                    cell.pressure = 0.0

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
        self.fouling_rate =
            global_sensor_trust * (d_pressure/d_time)
            + (1 - global_sensor_trust) * fouling_rate

        # update parameters
        self.last_global_measurement = global_measurement
        self.time_last_global_measurement = self.get_clock().now().nanoseconds

    # returns a matrix filled with cells at a certain pressure
    def cell_matrix(x: int, y: int, pressure: float):
        matrix = [[]]

        for i in range(x):
            matrix[i] = []

            for j in range(y):
                matrix[i][j] = Cell(pressure)

        return matrix