from motor_driver import MotorDriver
from time import sleep

motor = MotorDriver()

motor.run(0, 0, 75)
sleep(1)
motor.run(0, 1, 75)
sleep(1)
motor.stop(0)

motor.run(1, 0, 75)
sleep(1)
motor.run(1, 1, 75)
sleep(1)
motor.stop(1)
