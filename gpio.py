from gpiozero import DistanceSensor
from time import sleep
from PCA9685 import PCA9685
from ped_classifier import PedestrianClassifier
from motor_driver import MotorDriver

use_ultrasonic = True
use_camera = True

echo_1, trigger_1 = 19, 13
echo_2, trigger_2 = 21, 20
echo_3, trigger_3 = 16, 12

distance_sensor_1 = DistanceSensor(echo=echo_1, trigger=trigger_1)
distance_sensor_2 = DistanceSensor(echo=echo_2, trigger=trigger_2)
distance_sensor_3 = DistanceSensor(echo=echo_3, trigger=trigger_3)

#    d2
# d1----d3
#  /    \
# /      \

threshold = 0.25

motor = MotorDriver()
classifier = PedestrianClassifier()

def move(direction, sleep_time):
    if direction == "forward":
        motor.run(0, 0, 50)
        motor.run(1, 0, 50)
    elif direction == "backward":
        motor.run(0, 1, 50)
        motor.run(1, 1, 50)
    elif direction == "left":
        motor.run(0, 0, 50)
        motor.run(1, 1, 50)
    elif direction == "right":
        motor.run(0, 1, 50)
        motor.run(1, 0, 50)

    sleep(sleep_time)

    motor.stop(0)
    motor.stop(1)

def move_routine():
    distance_1 = distance_sensor_1.distance
    distance_2 = distance_sensor_2.distance
    distance_3 = distance_sensor_3.distance

    print("distance_1: {}\tdistance_2: {}\tdistance_3: {}".format(distance_1, distance_2, distance_3))

    if distance_1 >= threshold and distance_2 >= threshold and distance_3 >= threshold:
        print("moving forward")
        move("forward", 1)
    elif distance_1 < threshold:
        print("Moving right")
        move("right", 1)
    elif distance_2 < threshold:
        print("Moving back")
        move("backward", 1)
    elif distance_3 < threshold:
        print("Moving left")
        move("left", 1)

def pedestrian_routine():
    classifier.on_loop()
    n_peds = classifier.detect()
    if n_peds > 0:
        print("pedestrian detected")

def main():
    while True:
        if use_ultrasonic:
            move_routine()

        if use_camera:
            pedestrian_routine()
                    
        sleep(0.5)

if __name__ == "__main__":
    main()
