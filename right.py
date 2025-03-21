# Chosen Scrum Vehicle Movement Version 1.0
# Overview:
# Gets the tank to turn right, taking in speed as a parameter
# def turn_right(self, speed):
#    Since it is in the TankRobot class, it must take in self as a parameter
#    Takes in speed as the parameter

    def turn_right(self, speed):
        pwm.setDutycycle(self.PWMA, speed) # Left motor goes forward
        pwm.setLevel(self.AIN1, 0)
        pwm.setLevel(self.AIN2, 1)
        pwm.setDutycycle(self.PWMB, speed) # Right motor goes backward
        pwm.setLevel(self.BIN1, 0)
        pwm.setLevel(self.BIN2, 1)
