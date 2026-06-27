import cv2
import mediapipe as mp
import numpy as np
import os

# Initialize MediaPipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1)

# Drawing spec
mp_drawing = mp.solutions.drawing_utils
drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)

# Face direction thresholds
# Face direction thresholds
YAW_THRESHOLD = 0.03  # Left/right
PITCH_THRESHOLD_UP = 0.07  # Looking up
PITCH_THRESHOLD_DOWN = 0.12 # Looking down

# Landmark indices for iris and eyes
LEFT_IRIS = [474, 475, 476, 477]
RIGHT_IRIS = [469, 470, 471, 472]
LEFT_EYE = [33, 133]
RIGHT_EYE = [362, 263]



def detect_face_direction(landmarks):
    print("111111111111111")
    frame=cv2.imread(landmarks)
    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(image_rgb)
    print("2222222222222222222222222222")
    if results.multi_face_landmarks:
        print("++++++++==================")
        for face_landmarks in results.multi_face_landmarks:
            mp_drawing.draw_landmarks(frame, face_landmarks, mp_face_mesh.FACEMESH_CONTOURS, drawing_spec, drawing_spec)
            landmark_list = face_landmarks.landmark


            landmarks=landmark_list

            # nose_tip = landmarks[1]
            # head_center = landmarks[168]  # Mid forehead
            #
            # # Estimate yaw: horizontal rotation
            # yaw = nose_tip.x - head_center.x
            # print(yaw)
            # if yaw < -YAW_THRESHOLD:
            #     return "Looking Right"
            # elif yaw > YAW_THRESHOLD:
            #     return "Looking Left"
            # else:
            #     return "Facing Forward"
            nose_tip = landmarks[1]
            forehead = landmarks[168]
            chin = landmarks[152]

            yaw = nose_tip.x - forehead.x
            pitch = nose_tip.y - forehead.y
            print("pitch", pitch, "PITCH_THRESHOLD_DOWN", PITCH_THRESHOLD_DOWN, "PITCH_THRESHOLD_UP",
                  PITCH_THRESHOLD_UP)
            print("yaw", yaw, "YAW_THRESHOLD", YAW_THRESHOLD)

            print(pitch,"pitch")
            if yaw < -YAW_THRESHOLD:
                return "Looking Right"
            elif yaw > YAW_THRESHOLD:
                return "Looking Left"
            elif pitch > PITCH_THRESHOLD_DOWN:
                return "Looking Down"
            elif pitch < PITCH_THRESHOLD_UP:
                return "Looking Up"
            else:
                return "Facing Forward"

    return "No face"







# r=r"C:\Users\RABEEH\Downloads\online exam malpractice completed backup\online exam malpractice completed backup\New folder\onlinemalpratice\onlinemalpratice\media\CAP7030347199593648227.jpg"#input()
r=input()
print("======================+++++----")
print(r)
res=detect_face_direction(r)
print(res)

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(_SCRIPT_DIR, 'sample.txt'), 'w') as file:
    file.write(res)