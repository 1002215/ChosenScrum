# camera.py
import cv2 as cv

# This class will take in a VideoCamera object and use it to return a video stream. The class will be able to get each frame and return each frame as a jpeg file.
class VideoCamera(object):
    def __init__(self):
        self.video = cv.VideoCapture(0)  # Open the default webcam (change if needed)
        self.width = 640  # Desired width
        self.height = 480  # Desired height

    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, frame = self.video.read()
        if success:
            # Resize the frame
            frame = cv.resize(frame, (self.width, self.height))
            _, jpeg = cv.imencode('.jpg', frame)
            return jpeg.tobytes()
