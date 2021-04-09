from gpiozero import DistanceSensor
import time

distance_sensor = DistanceSensor(echo=3, trigger=2)

while True:
    print("Distance: {}".format(distance_sensor.distance))
    time.sleep(1)
