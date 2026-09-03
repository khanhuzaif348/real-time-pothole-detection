from ultralytics import YOLO

# Load our trained model
model = YOLO(
    "runs/detect/outputs/pothole_model-3/weights/best.pt"
)

# Run prediction
results = model.predict(
    source="data/test/images",
    conf=0.25,
    save=True
)

# Process every image
for result in results:

    pothole_count = 0

    print("\nImage:", result.path)

    # Process every detected object
    for box in result.boxes:

        # Get class ID
        class_id = int(box.cls[0])

        # Get confidence
        confidence = float(box.conf[0])

        # Convert class ID to class name
        class_name = model.names[class_id]

        # Get bounding-box coordinates
        coordinates = box.xyxy[0].tolist()

        print(
            "Class:", class_name,
            "| Confidence:", round(confidence * 100, 2), "%"
        )

        print(
            "Coordinates:",
            [round(x, 2) for x in coordinates]
        )

        # Count only potholes
        if class_id == 2:
            pothole_count += 1

    print("Total potholes:", pothole_count)

print("\nPrediction completed!")