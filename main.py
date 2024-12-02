# The flask module allows us to create a flask framework, which we can use to send requests using http requests.
# The time module allows us to fix the duration of time each function moves by seconds.
# The PCA9685 module allows us to control how much electrical power needs to be sent
# The Login module returns the values showing whether the account was found in the database, whether the password matches, and whether the user has access to the Chosen network.
from flask import Flask, request, jsonify, render_template, redirect, url_for
from Login import *
from PCA9685 import PCA9685
import requests
import logging
from datetime import datetime

# Direct to where the electrical power needs to be sent and how much needs to be sent
pwm = PCA9685(0x40, debug=False)
pwm.setPWMFreq(20)

# Create the flask framework
app = Flask(__name__, template_folder='templates')

with open("filename.txt", "r") as f:
    log_messages = []
    for line in f:
        log_messages.append(line.strip())

def save_list(lst, filename="filename.txt"):
    with open(filename, "w") as f:
        for item in lst:
            f.write(f"{item}\n")

def log_action(message):
    logging.info(message)
    log_messages.append(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {message}")
    # Limit log list size if needed
    save_list(log_messages)


        # Endpoint to retrieve logs as JSON
@app.route('/logs', methods=['GET'])
def get_logs():
    return jsonify(log_messages)

def send_request(url):  # Sends requests to the host url
   x = requests.post(url)
   return x

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
        log_action("Rover moved forward")
# Gets the tank to move backward for three seconds before stopping, taking in speed as a parameter.
    def move_backward(self, speed):
        pwm.setDutycycle(self.PWMA, speed)
        pwm.setLevel(self.AIN1, 1) # Left motor goes backwards
        pwm.setLevel(self.AIN2, 0)
        pwm.setDutycycle(self.PWMB, speed)
        pwm.setLevel(self.BIN1, 0) #Right motor goes forwards
        pwm.setLevel(self.BIN2, 1)
        log_action("Rover moved backward")

# Gets the tank to turn left for three seconds before stopping, taking in speed as a parameter.
    def turn_left(self, speed):
        pwm.setDutycycle(self.PWMA, speed)
        pwm.setLevel(self.AIN1, 1)
        pwm.setLevel(self.AIN2, 0)   # Left motor goes backward
        pwm.setDutycycle(self.PWMB, speed)
        pwm.setLevel(self.BIN1, 1)
        pwm.setLevel(self.BIN2, 0)  # Right motor goes forward
        log_action("Rover turned left")

# Gets the tank to turn right for three seconds before stopping, taking in speed as a parameter.
    def turn_right(self, speed):
        pwm.setDutycycle(self.PWMA, speed) # Left motor goes forward
        pwm.setLevel(self.AIN1, 0)
        pwm.setLevel(self.AIN2, 1)
        pwm.setDutycycle(self.PWMB, speed) # Right motor goes backward
        pwm.setLevel(self.BIN1, 0)
        pwm.setLevel(self.BIN2, 1)
        log_action("Rover turned right")

# Gets the tank to stop, taking in no parameters
    def stop(self):
        pwm.setDutycycle(self.PWMA, 0)  # Stop left motor
        pwm.setDutycycle(self.PWMB, 0)  # Stop right motor
        log_action("Rover stopped")
tank_robot = TankRobot()

# We created a POST route with no parameters, then ran the move_fwd command on the tank_robot. Then, we returned the JSON dictionary storing the confirmation that the command was run.
@app.route('/fwd', methods=['POST'])
def fwd():
    tank_robot.move_fwd(50) # Move forward at speed 100
    return jsonify({'Move forward': True}) # Return confirmation that the function was ran

# We create the bwd command. We created a POST route with no parameters, then ran the move_bwd command on the tank_robot. Then, we returned the JSON dictionary storing the confirmation that the command was run.
@app.route('/bwd', methods=['POST'])
def bwd():
    tank_robot.move_backward(50) # Move backward at speed 100
    return jsonify({'Move backward': True}) # Return confirmation that the function was ran

# We create the right command. We created a POST route with no parameters, then ran the move_right command on the tank_robot. Then, we returned the JSON dictionary storing the confirmation that the command was run.
@app.route('/right', methods=['POST'])
def right():
    tank_robot.turn_right(50) # Turn right at speed 100
    return jsonify({'Turn right': True}) # Return confirmation that the function was ran

# We create the left command. We created a POST route with no parameters, then ran the move_left command on the tank_robot. Then, we returned the JSON dictionary storing the confirmation that the command was run.
@app.route('/left', methods=['POST'])
def left():
    tank_robot.turn_left(50) # Turn left at speed 100
    return jsonify({'Turn left': True}) # Return confirmation that the function was ran

# We create the stop command. We created a POST route with no parameters, then ran the stop command on the tank_robot. Then, we returned the JSON dictionary storing the confirmation that the command was run.
@app.route('/stop', methods=['POST'])
def stop():
    tank_robot.stop() # Stop
    return jsonify({'command': 'STOP'}) # Return confirmation that the function was ran

# This opens up the website at the login page
@app.route('/')
def start():
  log_action("Website opened at login page")
  return redirect(url_for('login'))

# Using values from the Login module, it determines whether the user exists in the database, whether the information is valid, and whether the user gets access to the Chosen Network. If they do, they get redirected to the main page.
@app.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':  # If the form is submitted via POSt
     send = Login()
     # Retrieve the form data using 'request.form' which is a dictionary-like object
     username = request.form['username']
     password = request.form['password']
     action = request.form.get('action')
     if action == 'login':
          send.sendinfo(username, password)
          user_exists = send.bFoundAccount
          user_valid = send.LoginSuccessful
          # You can now use this data for further processing (like checking credentials)
          if user_exists == True:
              if user_valid == True:
                  log_action(f"User {username} logged in successfully")
                  return redirect(url_for('screen'))
              else:
                  log_action(f"Login failed for user {username}: Incorrect password")
                  return 'Password is incorrect, please try again.'
          else:
              log_action(f"Login failed: Account {username} does not exist")
              return "This account does not exist."
     elif action == 'signup':
         send.sendinfo(username, password)
         user_exists = send.bFoundAccount
         if user_exists == True:
             log_action(f"Signup attempt failed: Username {username} already taken")
             return "This username is taken. Please try again."
         else:
             send.create_user(username, password)
             log_action(f"New account created for user {username}")
             return "Account created!"
  return render_template('login.html') # Use login html file for the aesthetics

# This function takes in JSON POST requests from the buttons, and makes the robot move accordingly by sending requests to the robot. 
@app.route('/buttons', methods=['GET', 'POST'])
def buttons():
   if request.method == 'POST':
       # Get JSON data from the buttons
       jsondata = request.get_json()
       action = jsondata.get('action')
       if action == 'fwd':
           send_request('http://192.168.1.25:5123/fwd')
       if action == 'bwd':
           send_request('http://192.168.1.25:5123/bwd')
       if action == 'right':
           send_request('http://192.168.1.25:5123/right')
       if action == 'left':
           send_request('http://192.168.1.25:5123/left')
       if action == 'stop':
        
   return render_template('buttons.html') # Use the buttons html file for the aesthetics
   
# Show the console log front end
@app.route('/logs', methods = ['GET', 'POST'])
def console():
    return render_template('logs.html')
#Show the screen separating the sebite into four parts: one with the buttons, one with the console log, and the rest as placeholders.
@app.route('/screen/', methods = ['GET', 'POST'])
def screen():
    return render_template('screen.html')
@app.route('/video', methods = ['GET', 'POST'])
def video():
    return render_template('video.html')

if __name__ == "__main__": # This runs the app
    app.run(host='192.168.1.25', debug=True, port=5123, use_reloader=False) # Where the API will be host
