# USAGE
# python yolo_video.py --input videos/airport.mp4 --output output/airport_output.avi --yolo yolo-coco

import time
import os

# All heavy imports and model loading are done lazily inside objdet()
# so that Vercel can import this module without cv2/numpy installed.

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

_net = None
_ln = None
_LABELS = None
_COLORS = None


def _load_model():
    """Lazy-load the YOLO model and labels only when first needed."""
    global _net, _ln, _LABELS, _COLORS

    if _net is not None:
        return  # already loaded

    try:
        import numpy as np
        import cv2
    except ImportError:
        raise RuntimeError("cv2 and numpy are required for object detection but are not installed.")

    labelsPath = os.path.join(BASE_DIR, "yolo", "coco.names")
    _LABELS = open(labelsPath).read().strip().split("\n")

    np.random.seed(42)
    _COLORS = np.random.randint(0, 255, size=(len(_LABELS), 3), dtype="uint8")

    weightsPath = os.path.join(BASE_DIR, "yolo", "yolov3.weights")
    configPath = os.path.join(BASE_DIR, "yolo", "yolov3.cfg")

    print("[INFO] loading YOLO from disk...")
    _net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)
    layer_names = _net.getLayerNames()
    try:
        _ln = [layer_names[i - 1] for i in _net.getUnconnectedOutLayers()]
    except Exception:
        _ln = [layer_names[i[0] - 1] for i in _net.getUnconnectedOutLayers()]


def objdet(path):
    try:
        import numpy as np
        import cv2
    except ImportError:
        print("[WARNING] cv2/numpy not available — skipping object detection.")
        return []

    _load_model()

    objects = []
    (W, H) = (None, None)
    frame = cv2.imread(os.path.join(BASE_DIR, "media", path))

    if frame is None:
        return []

    if W is None or H is None:
        (H, W) = frame.shape[:2]

    blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416), swapRB=True, crop=False)
    _net.setInput(blob)
    start = time.time()
    layerOutputs = _net.forward(_ln)
    end = time.time()

    boxes = []
    confidences = []
    classIDs = []

    for output in layerOutputs:
        for detection in output:
            scores = detection[5:]
            classID = np.argmax(scores)
            confidence = scores[classID]

            if confidence > 0.35:
                box = detection[0:4] * np.array([W, H, W, H])
                (centerX, centerY, width, height) = box.astype("int")

                x = int(centerX - (width / 2))
                y = int(centerY - (height / 2))

                boxes.append([x, y, int(width), int(height)])
                confidences.append(float(confidence))
                classIDs.append(classID)

    idxs = cv2.dnn.NMSBoxes(boxes, confidences, 0.4, 0.5)

    if len(idxs) > 0:
        for i in idxs.flatten():
            objects.append(_LABELS[classIDs[i]])

    print("okkkk")
    cv2.imwrite("output/" + "sample" + ".jpg", frame)
    return objects