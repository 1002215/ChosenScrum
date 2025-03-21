# CHOSEN SCRUM BETA
#ALL code and functions are by Chosen
# This file connects videos, including starting lane detection and streaming video frames.
#
#PSUDOCODE:
#Def start_lane_detection():
#    Run lines.py asynchronously using subprocess
#    Return success message
#
#Def video_feed():
#    Return a stream of video frames from generate_video_frames()#
#
#Def serve_video(filename):
#    Serve the requested video file from the static directory
#############################################################################


from flask import Blueprint, jsonify, Response, send_from_directory
import subprocess
from lines import generate_video_frames

video_bp = Blueprint('video', __name__)

@video_bp.route("/start_lane_detection", methods=["POST"])
def start_lane_detection():
    subprocess.Popen(["python", "lines.py"])
    return jsonify({"message": "Lane Detection Started!"})

@video_bp.route("/video_feed")
def video_feed():
    return Response(generate_video_frames(), mimetype="multipart/x-mixed-replace; boundary=frame")

@video_bp.route("/video/<filename>")
def serve_video(filename):
    return send_from_directory("static", filename, as_attachment=False)
