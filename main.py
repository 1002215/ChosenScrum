# The flask module allows us to create a flask framework, which we can use to send requests using http requests.
# The time module allows us to fix the duration of time each function moves by seconds.
# The PCA9685 module allows us to control how much electrical power needs to be sent
# The Login module returns the values showing whether the account was found in the database, whether the password matches, and whether the user has access to the Chosen network.
from flask import Flask, request, jsonify, render_template, redirect, url_for, Response
from Login import *
from PCA9685 import PCA9685
import requests
import logging
from datetime import datetime
from TankRobot import *

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
           send_request('http://192.168.240.20:5123/fwd')
           log_action(request)
       if action == 'bwd':
           send_request('http://192.168.240.20:5123/bwd')
           log_action(request)
       if action == 'right':
           send_request('http://192.168.240.20:5123/right')
           log_action(request)
       if action == 'left':
           send_request('http://192.168.240.20:5123/left')
           log_action(request)
       if action == 'stop':
           send_request('http://192.168.240.20:5123/stop')
           log_action(request)
   return render_template('buttons.html') # Use the buttons html file for the aesthetics
   
# Show the console log front end
@app.route('/logs', methods = ['GET', 'POST'])
def console():
    return render_template('logs.html')
    
#Show the screen separating the webite into four parts: one with the buttons, one with the console log, and the rest as placeholders.
@app.route('/screen/', methods = ['GET', 'POST'])
def screen():
    return render_template('screen.html')


@app.route('/video', methods = ['GET', 'POST'])
def gen(camera):
   while True:
       frame = camera.get_frame()
       yield (b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


# Show the live camera feed front end
@app.route('/video_feed_page')
def video_feed_page():
    return render_template('video_feed.html')  # This renders the page with the stream

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__": # This runs the app
    app.run(host='192.168.240.20', debug=True, port=5123, use_reloader=False) # Where the API will be host
