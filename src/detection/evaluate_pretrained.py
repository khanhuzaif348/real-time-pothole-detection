from ultralytics import YOLO

model = YOLO("models/best.pt")

print("Evaluating pretrained pothole model...")
print()

results = model.val(
    data="data/pothole_test.yaml",
    split="test",
    imgsz=640
)

print()
print("Evaluation completed.")
print("mAP50:", results.box.map50)
print("mAP50-95:", results.box.map)