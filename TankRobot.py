from PCA9685 import PCA9685

# The TankRobot class allows us to connect to the motors and control the amount of electrical power being sent to each of the motors. It also has the functions to get the tank to move forward, backward, left, right, and stop.
class TankRobot:
    def __init__(self):
        self.PWMA = 0 # Controls the power supplied and connects it to hardware
        self.AIN1 = 1 # Controls direction of the first motor
        self.AIN2 = 2 # Controls the opposite direction of the first motor
        self.PWMB = 5 # Controls the power supplied and connects it to hardware
        self.BIN1 = 3 # Controls direction of the second motor
        self.BIN2 = 4 # Controls the opposite direction of the second motor

# Gets the tank to move forward for three seconds before stopping, taking in speed as a parameter
    def move_fwd(self, speed):
        pwm.setDutycycle(self.PWMA, speed)
        pwm.setLevel(self.AIN1, 0)
        pwm.setLevel(self.AIN2, 1)
        pwm.setDutycycle(self.PWMB, speed)
        pwm.setLevel(self.BIN1, 1)
        pwm.setLevel(self.BIN2, 0)

# Gets the tank to move backward for three seconds before stopping, taking in speed as a parameter.
    def move_backward(self, speed):
        pwm.setDutycycle(self.PWMA, speed)
        pwm.setLevel(self.AIN1, 1) # Left motor goes backwards
        pwm.setLevel(self.AIN2, 0)
        pwm.setDutycycle(self.PWMB, speed)
        pwm.setLevel(self.BIN1, 0) #Right motor goes forwards
        pwm.setLevel(self.BIN2, 1)


# Gets the tank to turn left for three seconds before stopping, taking in speed as a parameter.
    def turn_left(self, speed):
        pwm.setDutycycle(self.PWMA, speed)
        pwm.setLevel(self.AIN1, 1)
        pwm.setLevel(self.AIN2, 0)   # Left motor goes backward
        pwm.setDutycycle(self.PWMB, speed)
        pwm.setLevel(self.BIN1, 1)
        pwm.setLevel(self.BIN2, 0)  # Right motor goes forward


# Gets the tank to turn right for three seconds before stopping, taking in speed as a parameter.
    def turn_right(self, speed):
        pwm.setDutycycle(self.PWMA, speed) # Left motor goes forward
        pwm.setLevel(self.AIN1, 0)
        pwm.setLevel(self.AIN2, 1)
        pwm.setDutycycle(self.PWMB, speed) # Right motor goes backward
        pwm.setLevel(self.BIN1, 0)
        pwm.setLevel(self.BIN2, 1)


# Gets the tank to stop, taking in no parameters
    def stop(self):
        pwm.setDutycycle(self.PWMA, 0)  # Stop left motor
        pwm.setDutycycle(self.PWMB, 0)  # Stop right motor
