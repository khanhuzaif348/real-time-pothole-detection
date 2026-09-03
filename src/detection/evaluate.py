from ultralytics import YOLO
from pathlib import Path

# Load trained model
model = YOLO(
    "runs/detect/outputs/pothole_model-5/weights/best.pt"
)

image_folder = Path("data/my_test")

# Write the ACTUAL number of potholes in each image
actual_potholes = {
    "pothole_img.jpg": 1,
    "pothole_img1.jpg": 1,
    "pothole_img3.jpg": 1,
    "pothole_img4.jpg": 2,
}

correct = 0
total_images = 0

for image_path in image_folder.glob("*.jpg"):

    # Skip images that don't have an actual count
    if image_path.name not in actual_potholes:
        continue

    total_images += 1

    actual = actual_potholes[image_path.name]

    results = model.predict(
        source=str(image_path),
        conf=0.50,
        verbose=False
    )

    result = results[0]

    predicted = 0

    for box in result.boxes:

        class_id = int(box.cls[0])

        if class_id == 2:
            predicted += 1

    print("\nImage:", image_path.name)
    print("Actual:", actual)
    print("Predicted:", predicted)

    if actual == predicted:
        print("Result: CORRECT")
        correct += 1
    else:
        print("Result: WRONG")


accuracy = (correct / total_images) * 100

print("\n==============================")
print("Images tested:", total_images)
print("Correct:", correct)
print("Accuracy:", round(accuracy, 2), "%")
print("==============================")