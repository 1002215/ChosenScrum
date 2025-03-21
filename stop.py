# Chosen Scrum Vehicle Movement Version 1.0
# Overview:
# Gets the tank to stop
# def stop(self):
#    Since it is in the TankRobot class, it must take in self as a parameter

def stop(self):
        pwm.setDutycycle(self.PWMA, 0)  # Stop left motor
        pwm.setDutycycle(self.PWMB, 0)  # Stop right motor
