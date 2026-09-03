from ultralytics import YOLO

# Load pretrained YOLO11n
model = YOLO("yolo11n.pt")

# Train on our pothole dataset
results = model.train(
    data="data/data.yaml",
    epochs=10,
    imgsz=640,
    batch=4,
    workers=2,
    device="cpu",
    project="outputs",
    name="pothole_model"
)

print("Training completed!")