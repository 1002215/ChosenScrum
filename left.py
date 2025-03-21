# Chosen Scrum Vehicle Movement Version 1.0
# Overview:
# Gets the tank to turn left, taking in speed as a parameter
# def turn_left(self, speed):
#    Since it is in the TankRobot class, it must take in self as a parameter
#    Takes in speed as the parameter

    def turn_left(self, speed):
        pwm.setDutycycle(self.PWMA, speed)
        pwm.setLevel(self.AIN1, 1)
        pwm.setLevel(self.AIN2, 0)   # Left motor goes backward
        pwm.setDutycycle(self.PWMB, speed)
        pwm.setLevel(self.BIN1, 1)
        pwm.setLevel(self.BIN2, 0)  # Right motor goes forward
