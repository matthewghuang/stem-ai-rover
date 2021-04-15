from PCA9685 import PCA9685

class MotorDriver():
    def __init__(self):
        self.pwm = PCA9685(0x40, debug=False)
        self.pwm.setPWMFreq(50)
        self.PWMA = 0
        self.AIN1 = 1
        self.AIN2 = 2
        self.PWMB = 5
        self.BIN1 = 3
        self.BIN2 = 4 

    def run(self, motor, direction, speed):
        if speed > 100:
            return

        self.pwm.setDutycycle(self.PWMA if motor == 0 else self.PWMB, speed)

        self.pwm.setLevel(self.AIN1 if motor == 0 else self.BIN1, 0 if direction == 0 else 1)
        self.pwm.setLevel(self.AIN2 if motor == 0 else self.BIN2, 1 if direction == 0 else 0)

    def stop(self, motor):
        self.pwm.setDutycycle(self.PWMA if motor == 0 else self.PWMB, 0)
