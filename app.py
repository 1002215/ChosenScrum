# CHOSEN SCRUM BETA
# All code is by Chosen
#  Flask application file that initializes, registers blueprints the app and starts the server.
#PSUDOCODE:
#Import necessary modules and route blueprints
#Initialize Flask app with a secret key
#Call create_database() to ensure database tables exist
#Register blueprints for auth, video, and log routes
#Run the app in debug mode if executed directly
###############################################################


from flask import Flask
from auth_routes import auth_bp
from video_routes import video_bp
from log_routes import log_bp
from db import create_database

app = Flask(__name__)
app.secret_key = "supersecretkey"

create_database()

app.register_blueprint(auth_bp)
app.register_blueprint(video_bp)
app.register_blueprint(log_bp)

if __name__ == "__main__":
    app.run(debug=True)
