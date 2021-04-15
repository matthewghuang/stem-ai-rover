from gpiozero import DistanceSensor
from time import sleep
from PCA9685 import PCA9685
from ped_classifier import PedestrianClassifier
from motor_driver import MotorDriver

use_ultrasonic = False
use_camera = True

echo_1, trigger_1 = 21, 20
echo_2, trigger_2 = 19, 18
echo_3, trigger_3 = 17, 16

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

    motor.stop()

def move_routine():
    distance_1 = distance_sensor_1.distance
    distance_2 = distance_sensor_2.distance
    distance_3 = distance_sensor_3.distance

    if distance_1 >= threshold and distance_2 >= threshold and distance_3 >= threshold:
        print("moving forward")
        move("up", 1)
    elif distance_1 < threshold:
        print("Moving right")
        move("right", 1)
    elif distance_2 < threshold:
        print("Moving back")
        move("back", 1)
    elif distance_3 < threshold:
        print("Moving left")
        move("left", 1)

def pedestrian_routine():
    classifier.on_loop()
    n_peds = classifier.detect()
    print("pedestrian detection: ", n_peds)

def main():
    while True:
        if use_ultrasonic:
            move_routine()

        if use_camera:
            pedestrian_routine()
                    
        sleep(0.5)

if __name__ == "__main__":
    main()
