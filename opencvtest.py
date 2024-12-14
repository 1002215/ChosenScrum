import sys
import math
import cv2 as cv
import numpy as np
from flask import Flask, render_template, Response




app = Flask(__name__)




camera = cv.VideoCapture(0)


def draw_lines(img, lines, color=[0, 0, 255], thickness=10):
 if lines is None:
     return img
 img = np.copy(img)
 line_img = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)
 for line in lines:
     for x1, y1, x2, y2 in line:
         cv.line(line_img, (x1, y1), (x2, y2), color, thickness)
 img = cv.addWeighted(img, 0.8, line_img, 1.0, 0.0)
 return img

def region_of_interest(img, vertices):
    mask = np.zeros_like(img)
    cv.fillPoly(mask, vertices, 255)
    masked_image = cv.bitwise_and(img, mask)
    
    return masked_image



def generate_frames(frame):
    height, width, _ = frame.shape

    gray_frame = cv.cvtColor(frame, cv.COLOR_RGB2GRAY)

    blurred_frame = cv.GaussianBlur(gray_frame, (5, 5), 0)

    canny_frame = cv.Canny(blurred_frame, 150, 300)

    vertices = np.array([[(200, 100), (400, 100), (450, 300), (150, 300)]], dtype=np.int32)

    region_interest = region_of_interest(canny_frame, vertices)


    src_pts = np.float32([
    [width * 0.2, height * 0.1],  
    [width * 0.8, height * 0.1],  
    [width * 0.85, height * 0.8],  
    [width * 0.15, height * 0.8]   
])
    dst_pts = np.float32([[0, 0], [width, 0], [width, height], [0, height]])

    M = cv.getPerspectiveTransform(src_pts, dst_pts)
    warped_frame = cv.warpPerspective(region_interest, M, (frame.shape[1], frame.shape[0]))

  
    lines = cv.HoughLinesP(
        warped_frame,  
        rho=1,
        theta=np.pi / 180,
        threshold=100,
        minLineLength=100,
        maxLineGap=20
    )
    left_line_x = []
    left_line_y = []
    right_line_x = []
    right_line_y = []
    if lines is not None and len(lines) > 0:
        for line in lines:
            for x1, y1, x2, y2 in line:
                slope = (y2 - y1) / (x2 - x1)
                if math.fabs(slope) < 0.5:
                    continue
                if slope <= 0:
                    left_line_x.extend([x1, x2])
                    left_line_y.extend([y1, y2])
                else:
                    right_line_x.extend([x1, x2])
                    right_line_y.extend([y1, y2])

    left_lines = [[(left_line_x[i], left_line_y[i], left_line_x[i+1], left_line_y[i+1]) for i in range(0, len(left_line_x)-1, 2)]]
    right_lines = [[(right_line_x[i], right_line_y[i], right_line_x[i+1], right_line_y[i+1]) for i in range(0, len(right_line_x)-1, 2)]]

# Now, you can use the draw_lines function to draw these lines on the image
    frame_with_lines = draw_lines(frame, left_lines + right_lines, color=[0, 255, 0], thickness=5)

    return frame_with_lines


def generate_color_frames():
   """Generate color video frames."""
   while True:
       success, frame = camera.read()
       if not success:
           break
       # Encode the color frame
       ret1, buffer1 = cv.imencode('.jpg', frame)
       if not ret1:
           print("Error: Failed to encode color frame")
           break


       # Yield color frame
       yield (b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + buffer1.tobytes() + b'\r\n')




def generate_gray_frames():
   """Generate grayscale video frames."""
   while True:
       success, fram = camera.read()
       if not success:
           break
       # Convert to grayscale
       fixed = generate_frames(fram)


       # Encode the grayscale frame
       ret2, buffer2 = cv.imencode('.jpg', fixed)
       if not ret2:
           print("Error: Failed to encode grayscale frame")
           break


       # Yield grayscale frame
       yield (b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + buffer2.tobytes() + b'\r\n')




@app.route('/')
def index():
   """Render the main webpage."""
   return render_template('video.html')




@app.route('/color_feed')
def color_feed():
   """Endpoint for the color video feed."""
   return Response(generate_color_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')




@app.route('/gray_feed')
def gray_feed():
   """Endpoint for the grayscale video feed."""
   return Response(generate_gray_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')




if __name__ == '__main__':
 app.run(host='0.0.0.0', debug=True, port=8000)




