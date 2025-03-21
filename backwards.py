# Chosen Scrum Vehicle Movement Version 1.0
# Overview:
# Gets the tank to move backward, taking in speed as a parameter
# def move_backward(self, speed):
#    Since it is in the TankRobot class, it must take in self as a parameter
#    Takes in speed as the parameter

def move_backward(self, speed):
        pwm.setDutycycle(self.PWMA, speed)
        pwm.setLevel(self.AIN1, 1) # Left motor goes backwards
        pwm.setLevel(self.AIN2, 0)
        pwm.setDutycycle(self.PWMB, speed)
        pwm.setLevel(self.BIN1, 0) #Right motor goes forwards
        pwm.setLevel(self.BIN2, 1)
