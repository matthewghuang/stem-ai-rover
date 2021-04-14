from gpiozero import DistanceSensor
from time import sleep
from PCA9685 import PCA9685
from ped_classifier import PedestrianClassifier

use_ultrasonic = False
use_camera = True

echo_1, trigger_1 = 21, 20
echo_2, trigger_2 = 19, 18
echo_3, trigger_3 = 17, 16

distance_sensor_1 = DistanceSensor(echo=echo_1, trigger=trigger_1)
distance_sensor_2 = DistanceSensor(echo=echo_2, trigger=trigger_2)
distance_sensor_3 = DistanceSensor(echo=echo_3, trigger=trigger_3)

pwm = PCA9685(0x40, debug=False)
pwm.setPWMFreq(50)

#    d2
# d1----d3
#  /    \
# /      \

threshold = 0.25

class MotorDriver():
    def __init__(self):
        self.PWMA = 0
        self.AIN1 = 1
        self.AIN2 = 2
        self.PWMB = 5
        self.BIN1 = 3
        self.BIN2 = 4

    def run(self, motor, index, speed):
        if speed > 100:
            return

        if motor == 0:
            pwm.setDutycycle(self.PWMA, speed)

            if index == 0:
                pwm.setLevel(self.AIN1, 0)
                pwm.setLevel(self.AIN2, 1)
            else:
                pwm.setLevel(self.AIN1, 1)
                pwm.setLevel(self.AIN2, 0)
        else:
            pwm.setDutycycle(self, PWMB, speed)

            if index == 0:
                pwm.setLevel(self.BIN1, 0)
                pwm.setLevel(self.BIN2, 1)
            else:
                pwm.setLevel(self.BIN1, 1)
                pwm.setLevel(self.BIN2, 0)

    def stop(self, motor):
        if motor == 0:
            pwm.setDutycycle(self.PWMA, 0)
        else:
            pwm.setDutycycle(self.PWMB, 0)

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
