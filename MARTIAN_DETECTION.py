import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import os


def ORB():
   img = cv.imread('templates/martian.png', 0)
   img2 = cv.imread('templates/test.jpeg', 0)
   img2 = cv.resize(img2, (312,380))
   img2 = cv.blur(img2, (15,15))
   #gray_img2 = cv.imread(img2, cv.IMREAD_GRAYSCALE)
   #gray_img = cv.imread(img, cv.IMREAD_GRAYSCALE)


   orb = cv.ORB_create()

   keypoints1, descriptors1 = orb.detectAndCompute(img, None)
   keypoints2, descriptors2 = orb.detectAndCompute(img2, None)

   bf = cv.BFMatcher(cv.NORM_HAMMING, crossCheck=True)
   try:
      matches = bf.match(descriptors1,descriptors2) # descriptors2 is None
      matches = sorted(matches, key=lambda x: x.distance)
      num_matches = len(matches)  # 104 for other matches, 400+ for same image w/o blur
      # Draw first 50 matches.*
      img3 = cv.drawMatches(img, keypoints1, img2, keypoints2, matches[:50], None, flags=2)

      plt.imshow(img3), plt.show()
      if num_matches > 5:
         print("we are not alone")
   except:
      print("no matches")









if __name__ == '__main__':
   ORB()
