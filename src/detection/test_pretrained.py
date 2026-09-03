from ultralytics import YOLO
from pathlib import Path

# Load pretrained pothole model
model = YOLO("models/best.pt")

image_folder = Path("data/my_test")

print("Testing pretrained pothole model...")
print()

for image in image_folder.glob("*.jpg"):

    print("Testing:", image.name)

    results = model.predict(
        source=str(image),
        conf=0.50,
        save=True,
        verbose=False
    )

    count = 0

    for result in results:
        for box in result.boxes:
            class_id = int(box.cls[0])
            confidence = float(box.conf[0])

            if class_id == 0:
                count += 1

                print(
                    f"  Pothole: {confidence * 100:.2f}%"
                )

    print(f"  Total potholes: {count}")
    print()

print("Done!")