# Level 9 – MasterPi: Computer Vision

## 🧠 Learning Objectives

* Use a USB camera with OpenCV
* Detect AprilTags, lines, objects, or colors
* Use image data to guide robot actions

## 🧰 Materials Needed

* MasterPi with USB camera
* Raspberry Pi (4 or 5 recommended)
* Python 3 with `opencv-python` and `apriltag` or `pupil-apriltags`

## 📝 Instructions

1. **OpenCV Setup**:

```python
import cv2
cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    cv2.imshow("Camera", frame)
    if cv2.waitKey(1) == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
```

2. **AprilTag Detection**:

* Use a detection library to get tag ID and pose
* Adjust robot position based on tag location

3. **Color or Line Detection**:

* Use masks or contours to detect features

## 🧪 Mini Challenge

* Program robot to approach a tag or follow a color line

## ✅ Checkpoint

To pass this level, demonstrate:

* Real-time camera feed
* Detection of at least one visual feature (tag, color, or line)
* Robot responds to that input in code

---

[Back to Main README](README.md)
