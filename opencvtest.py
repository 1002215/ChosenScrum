import sys
import math
import cv2
import numpy as np
from flask import Flask, render_template, Response


camera = cv2.VideoCapture(0)

app = Flask(__name__)
def region_of_interest(img, vertices):
    mask = np.zeros_like(img)
    cv2.fillPoly(mask, vertices, 255)
    masked_image = cv2.bitwise_and(img, mask)
    
    return masked_image




def hough_transform(image):
       """
       Determine and cut the region of interest in the input image.
       Parameter:
           image: grayscale image which should be an output from the edge detector
       """
       # Distance resolution of the accumulator in pixels.
       rho = 1
       # Angle resolution of the accumulator in radians.
       theta = np.pi / 180
       # Only lines that are greater than threshold will be returned.
       threshold = 20
       # Line segments shorter than that are rejected.
       minLineLength = 20
       # Maximum allowed gap between points on the same line to link them
       maxLineGap = 500
       # function returns an array containing dimensions of straight lines
       # appearing in the input image
       return cv2.HoughLinesP(image, rho=rho, theta=theta, threshold=threshold,
                              minLineLength=minLineLength, maxLineGap=maxLineGap)




def average_slope_intercept(lines):
       """
       Find the slope and intercept of the left and right lanes of each image.
       Parameters:
           lines: output from Hough Transform
       """
       left_lines = []  # (slope, intercept)
       left_weights = []  # (length,)
       right_lines = []  # (slope, intercept)
       right_weights = []  # (length,)


       for line in lines:
           for x1, y1, x2, y2 in line:
               if x1 == x2:
                   continue
               slope = (y2 - y1) / (x2 - x1)
               # calculating intercept of a line
               intercept = y1 - (slope * x1)
               # calculating length of a line
               length = np.sqrt(((y2 - y1) ** 2) + ((x2 - x1) ** 2))
               # slope of left lane is negative and for right lane slope is positive
               if slope < 0:
                   left_lines.append((slope, intercept))
                   left_weights.append((length))
               else:
                   right_lines.append((slope, intercept))
                   right_weights.append((length))
       #
       left_lane = np.dot(left_weights, left_lines) / np.sum(left_weights) if len(left_weights) > 0 else None
       #left_slope = (left_lane[0].y - left_lane[-1].y)/(left_lane[0].x - left_lane[-1].x)
       right_lane = np.dot(right_weights, right_lines) / np.sum(right_weights) if len(right_weights) > 0 else None
       
       #center_lane = right_lane
       return left_lane, right_lane




def pixel_points( y1, y2, line):
       """
       Converts the slope and intercept of each line into pixel points.
           Parameters:
               y1: y-value of the line's starting point.
               y2: y-value of the line's end point.
               line: The slope and intercept of the line.
       """
       if line is None:
           return None
       slope, intercept = line
       x1 = int((y1 - intercept) / slope)
       x2 = int((y2 - intercept) / slope)
       y1 = int(y1)
       y2 = int(y2)
       return ((x1, y1), (x2, y2))




def lane_lines(image, lines):
       """
       Create full lenght lines from pixel points.
           Parameters:
               image: The input test image.
               lines: The output lines from Hough Transform.
       """
       center_lane = []
       left_lane, right_lane = average_slope_intercept(lines)
       y1 = image.shape[0]

       m1, b1 = left_lane[0], left_lane[1]
       n1 = 1/(math.sqrt(m1*m1+1))
       m2, b2 = right_lane[0], right_lane[1]
       n2 = 1/(math.sqrt(m2*m2+1))
       center_slope = (n2*m2-n1*m1)/(n2-n1)
       center_intercept = (n2*b2-n1*b1)/(n2-n1)
       center_lane = [center_slope, center_intercept]
       y2 = y1 * m1*((b2-b1)/(m1-m2))+b1

       left_line = pixel_points(y1, y2, left_lane)
       right_line = pixel_points(y1, y2, right_lane)
       center_line = pixel_points(y1, y2, center_lane)
       return left_line, right_line, center_line




def draw_lane_lines( image, lines, color=[0, 0, 255], thickness=20):
       """
       Draw lines onto the input image.
           Parameters:
               image: The input test image (video frame in our case).
               lines: The output lines from Hough Transform.
               color (Default = red): Line color.
               thickness (Default = 12): Line thickness.
       """
       line_image = np.zeros_like(image)

       for i in range(len(lines)):
            line = lines[i]
            if line is not None:
                if i == len(lines)-1:
                    cv2.line(line_image, *line, [0,255,0], thickness)
                else:
                    cv2.line(line_image, *line, color, thickness)
            else:
                continue

       return cv2.addWeighted(image, 1.0, line_image, 1.0, 0.0)









def frame_processor(image):
       height, width, _ = image.shape
       """
       Process the input frame to detect lane lines.
       Parameters:
           image: image of a road where one wants to detect lane lines
           (we will be passing frames of video to this function)
       """
       # convert the RGB image to Gray scale
       grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
       # applying gaussian Blur which removes noise from the image
       # and focuses on our region of interest
       # size of gaussian kernel
       kernel_size = 5
       # Applying gaussian blur to remove noise from the frames
       blur = cv2.GaussianBlur(grayscale, (kernel_size, kernel_size), 0)
       # first threshold for the hysteresis procedure
       low_t = 50
       # second threshold for the hysteresis procedure
       high_t = 150
       # applying canny edge detection and save edges in a variable
       edges = cv2.Canny(blur, low_t, high_t)
       # since we are getting too many edges from our image, we apply
       # a mask polygon to only focus on the road
       vertices = np.array([[(200, 100), (400, 100), (450, 300), (150, 300)]], dtype=np.int32)

       # Will explain Region selection in detail in further steps
       region = region_of_interest(edges, vertices)
       # Applying hough transform to get straight lines from our image
       # and find the lane lines
       # Will explain Hough Transform in detail in further steps
       '''src_pts = np.float32([
    [width * 0.2, height * 0.1],  
    [width * 0.8, height * 0.1],  
    [width * 0.85, height * 0.8],  
    [width * 0.15, height * 0.8]   
])
       dst_pts = np.float32([[0, 0], [width, 0], [width, height], [0, height]])

       M = cv2.getPerspectiveTransform(src_pts, dst_pts)
       warped_frame = cv2.warpPerspective(region, M, (image.shape[1], image.shape[0]))
'''
  
       hough = hough_transform(region)
       # lastly we draw the lines on our resulting frame and return it as output
       result = draw_lane_lines(image, lane_lines(image, hough))
       return result



def generate_gray_frames():
   """Generate grayscale video frames."""
   while True:
       success, frame = camera.read()
       if not success:
           break
       # Convert to grayscale
       fixed = frame_processor(frame)


       # Encode the grayscale frame
       ret2, buffer2 = cv2.imencode('.jpg', fixed)
       if not ret2:
           print("Error: Failed to encode grayscale frame")
           break


       # Yield grayscale frame
       yield (b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + buffer2.tobytes() + b'\r\n')

def generate_color_frames():
   """Generate color video frames."""
   while True:
       success, frame = camera.read()
       if not success:
           break
       # Encode the color frame
       ret1, buffer1 = cv2.imencode('.jpg', frame)
       if not ret1:
           print("Error: Failed to encode color frame")
           break


       # Yield color frame
       yield (b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + buffer1.tobytes() + b'\r\n')


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




