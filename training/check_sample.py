from ultralytics import YOLO
from pathlib import Path
import random

# Load trained model
model = YOLO(
    "runs/detect/outputs/pothole_model-5/weights/best.pt"
)

# Training images
image_folder = Path("data/train/images")

# Get images
images = list(image_folder.glob("*.jpg"))

# Select only 10 random images
samples = random.sample(images, min(10, len(images)))

print("Testing", len(samples), "training images...")

for image in samples:

    print("Testing:", image.name)

    model.predict(
        source=str(image),
        conf=0.50,
        save=True,
        verbose=False
    )

print("Done!")