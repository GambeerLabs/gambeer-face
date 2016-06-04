import time
import serial

from gamidle import Gambidleware

gambi = Gambidleware('/dev/ttyACM0', 115200)

time.sleep(2)

print("turn on engine")
gambi.on_engine()

time.sleep(2)

print("turn off engine")
gambi.off_engine()

print("reading temperature")

for i in xrange(50):
    print("Temperature = %0.2f" % gambi.read_temperature())

gambi.close()
