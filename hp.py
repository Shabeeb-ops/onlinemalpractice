import cv2
import mediapipe as mp
import numpy as np
import os

# Initialize MediaPipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1,refine_landmarks=True )

# Drawing spec
mp_drawing = mp.solutions.drawing_utils
drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)

# Face direction thresholds
YAW_THRESHOLD = 0.03  # Left/right
PITCH_THRESHOLD_UP = 0.07  # Looking up
PITCH_THRESHOLD_DOWN = 0.14  # Looking down

# Landmark indices for iris and eyes
LEFT_IRIS = [474, 475, 476, 477]
RIGHT_IRIS = [469, 470, 471, 472]
LEFT_EYE = [33, 133]
RIGHT_EYE = [362, 263]


def get_eye_direction(iris_indices, eye_corner_indices, landmarks):
    try:
        # Check if indices are in range
        if max(iris_indices + eye_corner_indices) >= len(landmarks):
            return "Unknown"

        iris_center_x = np.mean([landmarks[i].x for i in iris_indices])
        eye_left_x = landmarks[eye_corner_indices[0]].x
        eye_right_x = landmarks[eye_corner_indices[1]].x
        eye_center_x = (eye_left_x + eye_right_x) / 2
        print("iris_center_x",iris_center_x,"eye_center_x",eye_center_x,"eye_left_x",eye_left_x,"eye_right_x",eye_right_x)
        if iris_center_x < eye_center_x - 0.3:
            return "Looking Left"
        elif iris_center_x > eye_center_x + 0.3:
            return "Looking Right"
        else:
            return "Looking Center"
    except Exception as e:
        return f"Error: {str(e)}"

def detect_face_direction(image_path):
    frame = cv2.imread(image_path)
    if frame is None:
        return "Image Not Found", "No Eye Direction"

    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(image_rgb)

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:

            mp_drawing.draw_landmarks(frame, face_landmarks, mp_face_mesh.FACEMESH_CONTOURS, drawing_spec, drawing_spec)
            landmarks = face_landmarks.landmark


            # Debug: print landmark count
            print(f"Total landmarks detected: {len(landmarks)}")

            # Face direction
            nose_tip = landmarks[1]
            forehead = landmarks[168]
            chin = landmarks[152]

            yaw = nose_tip.x - forehead.x
            pitch = nose_tip.y - forehead.y

            if yaw < -YAW_THRESHOLD:
                face_direction = "Looking Right"
            elif yaw > YAW_THRESHOLD:
                face_direction = "Looking Left"
            elif pitch > PITCH_THRESHOLD_DOWN:
                face_direction = "Looking Down"
            elif pitch < PITCH_THRESHOLD_UP:
                face_direction = "Looking Up"
            else:
                face_direction = "Facing Forward"

            # Eye direction
            left_eye_direction = get_eye_direction(LEFT_IRIS, LEFT_EYE, landmarks)
            right_eye_direction = get_eye_direction(RIGHT_IRIS, RIGHT_EYE, landmarks)

            eye_direction = f"{left_eye_direction} (L), {right_eye_direction} (R)"
            return face_direction, eye_direction

    return "No Face Detected", "No Eye Direction"

# Run detection
image_path = input("Enter image path: ")
face_dir, eye_dir = detect_face_direction(image_path)

print("Face Direction:", face_dir)
print("Eye Direction:", eye_dir)

# Save to file
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
output_path = os.path.join(_SCRIPT_DIR, 'eye_face_direction.txt')
with open(output_path, 'w') as file:
    file.write(f"Face Direction: {face_dir}\n")