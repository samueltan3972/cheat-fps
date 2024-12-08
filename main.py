import dxcam
from PIL import Image
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
import numpy as np
from win32api import GetSystemMetrics
import win32api, win32con
import pyautogui
import cv2

width = GetSystemMetrics(0)
height = GetSystemMetrics(1)

####################################### --------------------------------------
# def draw_landmarks_on_image(rgb_image, detection_result):
#     pose_landmarks_list = detection_result.pose_landmarks
#     annotated_image = np.copy(rgb_image)
#
#     # Loop through the detected poses to visualize.
#     for idx in range(len(pose_landmarks_list)):
#         pose_landmarks = pose_landmarks_list[idx]
#
#         # Draw the pose landmarks.
#         pose_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
#         pose_landmarks_proto.landmark.extend([
#             landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in pose_landmarks
#         ])
#         solutions.drawing_utils.draw_landmarks(
#             annotated_image,
#             pose_landmarks_proto,
#             solutions.pose.POSE_CONNECTIONS,
#             solutions.drawing_styles.get_default_pose_landmarks_style())
#     return annotated_image
#
# def get_location(detection_result):
#     pose_landmarks_list = detection_result.pose_landmarks
#     nose_coordinate = pose_landmarks_list[0][4]
#     # print(nose_coordinate.x)
#     # # Loop through the detected poses to visualize.
#     # for idx in range(len(pose_landmarks_list)):
#     #     pose_landmarks = pose_landmarks_list[idx]
#     #
#     return nose_coordinate.x, nose_coordinate.y
#
# ########################
#
# import mediapipe as mp
# from mediapipe.tasks import python
# from mediapipe.tasks.python import vision
# import cv2
#
# # Download model at https://developers.google.com/mediapipe/solutions/vision/pose_landmarker/index#models
# model_path = './pose_landmarker_lite.task'
#
# # https://developers.google.com/mediapipe/solutions/vision/pose_landmarker/python#image
# BaseOptions = mp.tasks.BaseOptions
# PoseLandmarker = mp.tasks.vision.PoseLandmarker
# PoseLandmarkerOptions = mp.tasks.vision.PoseLandmarkerOptions
# VisionRunningMode = mp.tasks.vision.RunningMode
#
# # img = cv2.imread("./ApexLegends.jpg")
# # cv2.imshow("Title", img)
#
# options = PoseLandmarkerOptions(
#     base_options=BaseOptions(model_asset_path=model_path),
#     running_mode=VisionRunningMode.IMAGE,
#     min_pose_detection_confidence=0.25,
#     min_pose_presence_confidence=0.25)
#
#
# # Load the input image from an image file.
# # mp_image = mp.Image.create_from_file('./ApexLegends2.jpg')
#
# def detect_pose(frame):
#     # Load the input image from a numpy array.
#     mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
#
#     with PoseLandmarker.create_from_options(options) as landmarker:
#         pose_landmarker_result = landmarker.detect(mp_image)
#         x, y = get_location(pose_landmarker_result)
#         # print(pose_landmarker_result)
#         # annotated_image = draw_landmarks_on_image(mp_image.numpy_view(), pose_landmarker_result)
#         # cv2.imshow("Title", cv2.cvtColor(annotated_image, cv2.COLOR_RGB2BGR))
#         # cv2.waitKey(0)
#
#     return x, y
#

##################################
####################################### --------------------------------------

# CV2 Human Detection


# Detect mouse clicked
from pynput import mouse

mouse_ = mouse.Controller()
button = mouse.Button

def click(x,y):
    # win32api.SetCursorPos((x,y))
    # win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
    # win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, x, y, 0, 0)

import win32gui

def transform_relative(val, tres0, tres1, acc, speed):
    ret = val
    val = abs(val)
    if val > tres0 and acc:
        ret *= 2
    if val > tres1 and acc == 2:
        ret *= 2
    return round(ret * speed / 10)

def set_pos_mouse_event(x, y, absolute_coordinates=True):
    flags = win32con.MOUSEEVENTF_MOVE
    if absolute_coordinates:
        flags |= win32con.MOUSEEVENTF_ABSOLUTE
        normx = round(x * 0xFFFF / (win32api.GetSystemMetrics(win32con.SM_CXSCREEN) - 1))
        normy = round(y * 0xFFFF / (win32api.GetSystemMetrics(win32con.SM_CYSCREEN) - 1))
    else:  # @TODO - cfati: Not working yet!!!
        tres0, tres1, acc = win32gui.SystemParametersInfo(win32con.SPI_GETMOUSE)
        speed = win32gui.SystemParametersInfo(win32con.SPI_GETMOUSESPEED)
        #print(tres0, tres1, acc, speed)
        normx = transform_relative(x, tres0, tres1, acc, speed)
        normy = transform_relative(y, tres0, tres1, acc, speed)
    print(f"Move with: ({x}, {y}) ({normx}, {normy})")
    win32api.mouse_event(flags, normx, normy)

def set_pos_cursor_pos(x, y, absolute_coordinates=True):
    print(f"Move with: ({x}, {y})")
    if absolute_coordinates:
        win32api.SetCursorPos((x, y))
    else:
        curx, cury = win32api.GetCursorPos()
        win32api.SetCursorPos((curx + x, cury + y))

def on_move(x, y):
    print('Pointer moved to {0}'.format(
        (x, y)))

def on_click(x, y, button, pressed):
    btn = button.name

    if btn == 'middle':
        if pressed:
            # Screen Capture
            camera = dxcam.create()
            frame = camera.grab()
            no_coordinate = 0

            win32api.SetCursorPos((int(width/2), int(height/2)))

            pos = win32api.GetCursorPos()
            print("Pos:", pos)

            # Image.fromarray(frame).show()
            try:
                x, y = detect_pose(frame)
            except:
                no_coordinate = 1
                print("No coordinate detect")

            if no_coordinate == 0:
                # Move pointer relative to current position

                denormalized_x = round(x * width)
                denormalized_y = round(y * height)

                distance_x = denormalized_x - pos[0]
                distance_y = denormalized_y - pos[1]

                print("Denormailized:", denormalized_x, denormalized_y)
                print("Distance:", distance_x, distance_y)

                # set_pos_mouse_event(denormalized_x, denormalized_y)
                # set_pos_mouse_event(distance_x, distance_y, True)
                # set_pos_cursor_pos(denormalized_x, denormalized_y)

                click(distance_x, distance_y)

                # mouse_.move(50, 50)
                # pyautogui.moveRel(100, 100, duration=0.2)
                # mouse_.position = (x * width, y * height)
                mouse_.click(button.left, 1)
                # print('works')

    # if btn == 'left':
    #     if pressed:
    #         print('Left Clicked')

with mouse.Listener(
        on_click=on_click,
        # on_move=on_move
) as listener:
    listener.join()


# Code example: Refer https://github.com/googlesamples/mediapipe/tree/main/examples/pose_landmarker/python

# if __name__ == '__main__':
#     main()
