'''import cv2

# Open camera using Windows DirectShow
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

if not cap.isOpened():
    print("Could not access camera")
    exit()

print("Camera started")
print("Press 'd' to capture the image")
print("Press 'q' to quit")

while True:

    # Read frame
    ret, frame = cap.read()

    if not ret:
        print("Could not read frame")
        break

    # Display live camera
    cv2.imshow("Live Camera", frame)

    # Wait for keyboard input
    key = cv2.waitKey(1) & 0xFF

    # DONE → capture image
    if key == ord("d"):

        cv2.imwrite("captured_road.jpg", frame)

        print("Image captured!")
        print("Saved as captured_road.jpg")

        # Show captured image
        cv2.imshow("Captured Road", frame)

        cv2.waitKey(0)
        break

    # Quit
    if key == ord("q"):
        break

# Release camera
cap.release()
cv2.destroyAllWindows()  pahle ka code 



import cv2
from ultralytics import YOLO

# Load trained model
model = YOLO(
    "runs/detect/outputs/pothole_model-5/weights/best.pt"
) 
# Load trained model


# Open camera
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

if not cap.isOpened():
    print("Could not access camera")
    exit()

while True:

    # Read frame from camera
    ret, frame = cap.read()

    if not ret:
        print("Could not read frame")
        break

    # Run YOLO on current frame
    results = model.predict(
        source=frame,
        conf=0.60,
        verbose=False
    )

    # Get first result
    result = results[0]

    pothole_count = 0

    # Process detections
    for box in result.boxes:

        class_id = int(box.cls[0])
        confidence = float(box.conf[0])

        # Only potholes
        if class_id == 2:

            pothole_count += 1

            # Coordinates
            x1, y1, x2, y2 = map(
                int,
                box.xyxy[0]
            )

            # Draw bounding box
            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                (0, 255, 0),
                2
            )

            # Label
            label = f"Pothole {confidence * 100:.1f}%"

            cv2.putText(
                frame,
                label,
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2
            )

    # Display pothole count
    cv2.putText(
        frame,
        f"Potholes: {pothole_count}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    # Show camera
    cv2.imshow(
        "Pothole Detection",
        frame
    )

    # Press Q to quit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


cap.release()
cv2.destroyAllWindows()




import cv2
from ultralytics import YOLO

# Load trained model
model = YOLO(
    "runs/detect/outputs/pothole_model-5/weights/best.pt"
)

# Open camera
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Could not access camera")
    exit()

print("Camera started")
print("Press D to detect potholes")
print("Press Q to quit")

while True:

    ret, frame = cap.read()

    if not ret:
        print("Could not read camera frame")
        break

    # Display live camera
    cv2.imshow("Pothole Detection - Live Camera", frame)

    key = cv2.waitKey(1) & 0xFF

    # Press D to detect
    if key == ord("d"):

        print("\nDetecting potholes...")

        results = model.predict(
            source=frame,
            conf=0.50,
            verbose=False
        )

        result = results[0]

        pothole_count = 0
        confidences = []

        # Check detections
        for box in result.boxes:

            class_id = int(box.cls[0])
            confidence = float(box.conf[0])

            if class_id == 2:

                pothole_count += 1
                confidences.append(confidence)

        # Draw YOLO results
        annotated_frame = result.plot()

        # Calculate average confidence
        if confidences:
            average_confidence = (
                sum(confidences) / len(confidences)
            ) * 100
        else:
            average_confidence = 0

        # Display information
        text = f"Potholes: {pothole_count}"

        cv2.putText(
            annotated_frame,
            text,
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

        text2 = f"Confidence: {average_confidence:.2f}%"

        cv2.putText(
            annotated_frame,
            text2,
            (20, 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )

        # Show detection result
        cv2.imshow(
            "Pothole Detection Result",
            annotated_frame
        )

        print("Potholes:", pothole_count)
        print(
            "Average Confidence:",
            round(average_confidence, 2),
            "%"
        )

    # Press Q to quit
    elif key == ord("q"):
        break


cap.release()
cv2.destroyAllWindows()

'''

import cv2
from ultralytics import YOLO

# -----------------------------
# Load model
# -----------------------------
model = YOLO(
    "runs/detect/outputs/pothole_model-5/weights/best.pt"
)

# -----------------------------
# Open camera
# -----------------------------
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Could not access camera")
    exit()

# Store current frame
current_frame = None

# Detection result
detection_frame = None


# -----------------------------
# DONE button
# -----------------------------
def mouse_callback(event, x, y, flags, param):

    global detection_frame

    if event == cv2.EVENT_LBUTTONDOWN:

        # DONE button area
        if 500 <= x <= 620 and 420 <= y <= 470:

            print("\nDONE clicked")
            print("Detecting potholes...")

            results = model.predict(
                source=current_frame,
                conf=0.90,
                verbose=False
            )

            result = results[0]

            pothole_count = 0
            confidences = []

            # -------------------------
            # Process detections
            # -------------------------
            for box in result.boxes:

                class_id = int(box.cls[0])
                confidence = float(box.conf[0])

                class_name = model.names[class_id]

                print(
                    "Class:",
                    class_name,
                    "| Confidence:",
                    round(confidence * 100, 2),
                    "%"
                )

                if class_id == 2:

                    pothole_count += 1
                    confidences.append(confidence)

            # -------------------------
            # Average confidence
            # -------------------------
            if confidences:

                average_confidence = (
                    sum(confidences) /
                    len(confidences)
                ) * 100

            else:

                average_confidence = 0

            # -------------------------
            # Draw YOLO boxes
            # -------------------------
            detection_frame = result.plot()

            # -------------------------
            # Display count
            # -------------------------
            cv2.putText(
                detection_frame,
                f"Potholes: {pothole_count}",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2
            )

            cv2.putText(
                detection_frame,
                f"Confidence: {average_confidence:.2f}%",
                (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2
            )

            print(
                "Potholes:",
                pothole_count
            )

            print(
                "Average Confidence:",
                round(average_confidence, 2),
                "%"
            )


# -----------------------------
# Create camera window
# -----------------------------
window_name = "Pothole Detection"

cv2.namedWindow(window_name)

cv2.setMouseCallback(
    window_name,
    mouse_callback
)


# -----------------------------
# Main loop
# -----------------------------
while True:

    ret, frame = cap.read()

    if not ret:
        print("Could not read camera frame")
        break

    current_frame = frame.copy()

    # If detection exists, show result
    if detection_frame is not None:

        display_frame = detection_frame.copy()

    else:

        display_frame = frame.copy()

    # -----------------------------
    # DONE button
    # -----------------------------
    cv2.rectangle(
        display_frame,
        (500, 420),
        (620, 470),
        (0, 255, 0),
        -1
    )

    cv2.putText(
        display_frame,
        "DONE",
        (525, 453),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 0, 0),
        2
    )

    # Show window
    cv2.imshow(
        window_name,
        display_frame
    )

    # Q = quit
    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break


# -----------------------------
# Cleanup
# -----------------------------
cap.release()
cv2.destroyAllWindows()