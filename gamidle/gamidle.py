import serial


class Gambidleware(object):

    ENGINE_OFF_CMD    = [1, 0]
    ENGINE_ON_CMD     = [1, 255]
    TEMP_PACKAGE_SIZE = 5

    def __init__(self, serial_addr, bound=115200):
        self.serial = serial.Serial(serial_addr, bound)
        self.temperature_parser = TemperatureParser()

    def close(self):
        self.serial.close()

    def on_engine(self):
        self.serial.write(bytearray(self.ENGINE_ON_CMD))

    def off_engine(self):
        self.serial.write(bytearray(self.ENGINE_OFF_CMD))

    def read_temperature(self):
        raw_temp = self.serial.read(self.TEMP_PACKAGE_SIZE)
        return self.temperature_parser.parse(raw_temp)


class TemperatureParser(object):
    TEMP = [
        0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85,
        90, 95, 100, 105, 110, 115, 120
    ]

    ADC = [
        256, 307, 362, 419, 477, 534, 587, 638, 685, 728, 765, 800, 829, 855,
        878, 896, 913, 927, 939, 949, 960, 968, 974, 980, 984
    ]


    def parse(self, raw_temp):
        value = raw_temp.strip()
        value = int(value)
        return self._interpolate_temperature(value)


    def _interpolate_temperature(self, read_value):
        i = 0;
        while(read_value > self.ADC[i]):
           i += 1

        t0   = self.TEMP[i - 1]
        t1   = self.TEMP[i]
        adc0 = self.ADC[i - 1]
        adc1 = self.ADC[i]
        a = t1 - t0
        b = adc1 - adc0
        c = read_value - adc0

        temperatura = float(a) / float(b)
        temperatura = float(temperatura) * float(c)
        temperatura = float(temperatura) + float(t0)

        return temperatura
