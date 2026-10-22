from local_measurement import Local_measurement

# describes a single cell, with a certain pressure
class Cell():

    def __init__(self, measurements: list[Local_measurement]):
        self.measurements = measurements
        most_recent_measurement = most_recent(measurements)
        self.pressure = most_recent_measurement.pressure
        self.time_last_measurement = most_recent_measurement.time

    # gives the most recent measurement
    def most_recent(local_measurements: list[Local_measurement]):
        most_recent = Local_measurement(0.0, 0.0)
        for m in measurements:
            if m.time < most_recent.time:
                most_recent = measurement
        return most_recent


    