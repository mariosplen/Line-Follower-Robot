import analogio


class Sensor:
    def __init__(self, pin):
        self.min = 0  # Minimum detected value
        self.max = 3.3  # Maximum detected value
        self.threshold = 1.65  # (0 + 3.3) / 2
        self.pin = analogio.AnalogIn(pin)

    def set_min(self, new_min):
        self.min = new_min

    def set_max(self, new_max):
        self.max = new_max

    def set_threshold(self, threshold):
        self.threshold = threshold

    # value returns a value between 0 and 3.3, if it is 3.3 it is detecting complete black, if it is 0 it is white
    def value(self):
        return (self.pin.value * 3.3) / 65536

    # If the value is > than the threshold that means that the line is detected
    def is_above_line(self):
        return self.value() > self.threshold
