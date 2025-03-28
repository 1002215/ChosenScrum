# Chosen Scrum Vehicle Movement Version 1.0
# Overview:
# Gets the tank to move forward, taking in speed as a parameter
# def move_fwd(self, speed):
#    Since it is in the TankRobot class, it must take in self as a parameter
#    Takes in speed as the parameter

def move_fwd(self, speed):
      pwm.setDutycycle(self.PWMA, speed)
      pwm.setLevel(self.AIN1, 0)
      pwm.setLevel(self.AIN2, 1)
      pwm.setDutycycle(self.PWMB, speed)
      pwm.setLevel(self.BIN1, 1)
      pwm.setLevel(self.BIN2, 0)
