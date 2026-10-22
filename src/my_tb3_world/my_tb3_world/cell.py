from my_tb3_world.local_measurement import Local_measurement

# describes a single cell, with a certain pressure
class Cell():

    def __init__(self, x, y, pressure, time_last_measurement):
        self.pressure = pressure
        self.time_last_measurement = time_last_measurement
        self.x = x
        self.y = y


    