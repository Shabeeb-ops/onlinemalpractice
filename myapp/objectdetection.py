# USAGE
# python yolo_video.py --input videos/airport.mp4 --output output/airport_output.avi --yolo yolo-coco

# import the necessary packages
import numpy as np
import argparse
# import imutils
import time
import cv2
import os

# Base directory: parent of the 'myapp' folder (i.e. project root)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

labelsPath = os.path.join(BASE_DIR, "yolo", "coco.names")
LABELS = open(labelsPath).read().strip().split("\n")

# initialize a list of colors to represent each possible class label
np.random.seed(42)
COLORS = np.random.randint(0, 255, size=(len(LABELS), 3),
	dtype="uint8")

# derive the paths to the YOLO weights and model configuration
weightsPath = os.path.join(BASE_DIR, "yolo", "yolov3.weights")
configPath = os.path.join(BASE_DIR, "yolo", "yolov3.cfg")

# load our YOLO object detector trained on COCO dataset (80 classes)
# and determine only the *output* layer names that we need from YOLO
print("[INFO] loading YOLO from disk...")
net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)
ln = net.getLayerNames()
print(type(ln),'========================================================')
# ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]
layer_names = net.getLayerNames()
try:
    ln = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
except:
    ln = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]


def objdet(path):
    objects=[]
    writer = None
    writer = None
    (W, H) = (None, None)
    frame = cv2.imread(os.path.join(BASE_DIR, "media", path))

    if W is None or H is None:
        (H, W) = frame.shape[:2]

    # construct a blob from the input frame and then perform a forward
    # pass of the YOLO object detector, giving us our bounding boxes
    # and associated probabilities
    blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416),
                                 swapRB=True, crop=False)
    net.setInput(blob)
    start = time.time()
    layerOutputs = net.forward(ln)
    end = time.time()

    # initialize our lists of detected bounding boxes, confidences,
    # and class IDs, respectively
    boxes = []
    confidences = []
    classIDs = []

    # loop over each of the layer outputs
    for output in layerOutputs:
        # loop over each of the detections
        for detection in output:
            # extract the class ID and confidence (i.e., probability)
            # of the current object detection
            scores = detection[5:]
            classID = np.argmax(scores)
            confidence = scores[classID]

            # filter out weak predictions by ensuring the detected
            # probability is greater than the minimum probability
            if confidence > 0.35:
                # scale the bounding box coordinates back relative to
                # the size of the image, keeping in mind that YOLO
                # actually returns the center (x, y)-coordinates of
                # the bounding box followed by the boxes' width and
                # height
                box = detection[0:4] * np.array([W, H, W, H])
                (centerX, centerY, width, height) = box.astype("int")

                # use the center (x, y)-coordinates to derive the top
                # and and left corner of the bounding box
                x = int(centerX - (width / 2))
                y = int(centerY - (height / 2))

                # update our list of bounding box coordinates,
                # confidences, and class IDs
                boxes.append([x, y, int(width), int(height)])
                confidences.append(float(confidence))
                classIDs.append(classID)

    # apply non-maxima suppression to suppress weak, overlapping
    # bounding boxes
    idxs = cv2.dnn.NMSBoxes(boxes, confidences, 0.4,
                            0.5)

    # ensure at least one detection exists
    if len(idxs) > 0:
        # loop over the indexes we are keeping
        for i in idxs.flatten():
            # extract the bounding box coordinates
            # (x, y) = (boxes[i][0], boxes[i][1])
            # (w, h) = (boxes[i][2], boxes[i][3])
            #
            # # draw a bounding box rectangle and label on the frame
            # color = [int(c) for c in COLORS[classIDs[i]]]
            # cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            # text = "{}: {:.4f}".format(LABELS[classIDs[i]],
            #                            confidences[i])
            if True:

                    objects.append(LABELS[classIDs[i]])
            # cv2.putText(frame, text, (x, y - 5),
            #             cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)



    print("okkkk")
    cv2.imwrite("output/" + "sample" + ".jpg", frame)
    return objects

# print(objdet(r"C:\Users\USER\PycharmProjects\personalityprediction\output_image.jpg"))