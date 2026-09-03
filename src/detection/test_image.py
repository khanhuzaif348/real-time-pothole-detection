'''from ultralytics import YOLO

# Load trained model
model = YOLO(
    "runs/detect/outputs/pothole_model-5/weights/best.pt"
)

# Image to test
image_path = "D:\AI_pothole_detection\data\my_test\pothole_img1.jpg"

# Run prediction
results = model.predict(
    source=image_path,
    conf=0.50,
    save=True
)

# Process prediction
for result in results:

    pothole_count = 0

    print("\nImage:", result.path)

    for box in result.boxes:

        class_id = int(box.cls[0])
        confidence = float(box.conf[0])

        class_name = model.names[class_id]

        # Only count potholes
        if class_id == 2:

            pothole_count += 1

            coordinates = box.xyxy[0].tolist()

            print(
                "Class:", class_name,
                "| Confidence:",
                round(confidence * 100, 2),
                "%"
            )

            print(
                "Coordinates:",
                [round(x, 2) for x in coordinates]
            )

    print("Total potholes:", pothole_count)

print("\nPrediction completed!")



'''


from ultralytics import YOLO
from pathlib import Path

# Load trained model
model = YOLO(
    "runs/detect/outputs/pothole_model-5/weights/best.pt"
)

# Folder containing test images
image_folder = Path("data/my_test")

# Get all image files
image_files = list(image_folder.glob("*.jpg"))

# Loop through every image
for image_path in image_files:

    print("\n" + "=" * 50)
    print("Image:", image_path.name)

    # Predict one image
    results = model.predict(
        source=str(image_path),
        conf=0.50,
        save=True,
        verbose=False
    )

    result = results[0]

    pothole_count = 0

    # Loop through detected objects
    for box in result.boxes:

        class_id = int(box.cls[0])
        confidence = float(box.conf[0])

        class_name = model.names[class_id]

        if class_id == 2:

            pothole_count += 1

            print(
                "Class:", class_name,
                "| Confidence:",
                round(confidence * 100, 2),
                "%"
            )

    print("Total potholes:", pothole_count)

print("\nAll images processed!")