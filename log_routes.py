# CHOSEN SCRUM BETA
#All code and functions are by Chosen.
#This file provides endpoints to log user actions and retrieve most recent logs.
#PSUDOCODE:
#Def log_action():
#    Get action from JSON request
#    Connect to database and insert the action
#    Close connection
#    Return confirmation message#
#
#Def logs():
#    Connect to database
#    Retrieve last 10 actions from logs table
#    Return logs as JSON
#################################################################################

from flask import Blueprint, request, jsonify
import sqlite3

log_bp = Blueprint('log', __name__)

@log_bp.route("/log_action", methods=["POST"])
def log_action():
    data = request.json
    action = data.get("action", "")
    
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO logs (action) VALUES (?)", (action,))
    conn.commit()
    conn.close()
    
    return jsonify({"message": "Action logged!"})

@log_bp.route("/logs")
def logs():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT action FROM logs ORDER BY id DESC LIMIT 10")
    logs = [row[0] for row in cursor.fetchall()]
    conn.close()
    
    return jsonify(logs)
