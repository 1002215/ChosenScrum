# CHOSEN SCRUM BETA
# ALL code and functions are by Chosen.
# Manages user authentication, including login, logout, and session-protected screen view.
#
# PSUDOCODE:
# Def login():
#    If POST request:
#        Get form data (username, password, action)
#        Connect to database
#        If action is signup:
#            Attempt to insert new user
#            If duplicate, return error
#            Else, log user in and redirect
#        If action is login:
#            Check credentials and start session
#            If invalid, return error
#        Close database
#    Render login template with error if any#
#
#Def logout():
#    Clear session and redirect to login#
#
#Def screen():
#    If user not in session, redirect to login
#    Else, render the screen page
######################################################################################################

from flask import Blueprint, render_template, request, redirect, url_for, session
import sqlite3

auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        action = request.form["action"]

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        if action == "signup":
            try:
                cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
                conn.commit()
                session["username"] = username  # Automatically log in after signup
                return redirect(url_for("auth.screen"))
            except sqlite3.IntegrityError:
                error = "Username already exists. Try another one."
        elif action == "login":
            cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
            user = cursor.fetchone()
            if user:
                session["username"] = username
                return redirect(url_for("auth.screen"))
            else:
                error = "Invalid username or password."

        conn.close()

    return render_template("login.html", error=error)

@auth_bp.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("auth.login"))

@auth_bp.route("/screen")
def screen():
    if "username" not in session:
        return redirect(url_for("auth.login"))
    return render_template("screen.html")
