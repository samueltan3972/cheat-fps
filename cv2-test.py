# import the necessary packages
import numpy as np
import cv2

# initialize the HOG descriptor/person detector
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

cv2.startWindowThread()

# open webcam video stream
# cap = cv2.VideoCapture(0)

img = cv2.imread("./ApexLegends.jpg")

boxes, weights = hog.detectMultiScale(img, winStride=(8, 8))

boxes = np.array([[x, y, x + w, y + h] for (x, y, w, h) in boxes])

for (xA, yA, xB, yB) in boxes:
    # display the detected boxes in the colour picture
    cv2.rectangle(img, (xA, yA), (xB, yB),
                  (0, 255, 0), 2)

# Display the resulting frame
cv2.imshow('frame', img)
cv2.waitKey(0)

# while (True):
#     # Capture frame-by-frame
#     ret, frame = cap.read()
#
#     # resizing for faster detection
#     frame = cv2.resize(frame, (640, 480))
#     # using a greyscale picture, also for faster detection
#     # gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
#
#     # detect people in the image
#     # returns the bounding boxes for the detected objects
#     boxes, weights = hog.detectMultiScale(frame, winStride=(8, 8))
#
#     boxes = np.array([[x, y, x + w, y + h] for (x, y, w, h) in boxes])
#
#     for (xA, yA, xB, yB) in boxes:
#         # display the detected boxes in the colour picture
#         cv2.rectangle(frame, (xA, yA), (xB, yB),
#                       (0, 255, 0), 2)
#
#     # Display the resulting frame
#     cv2.imshow('frame', frame)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break