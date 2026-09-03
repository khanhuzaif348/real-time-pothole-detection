from ultralytics import YOLO

model = YOLO(
    "runs/detect/outputs/pothole_model-5/weights/best.pt"
)

print("Evaluating model on TEST dataset...")
print()

results = model.val(
    data="data/data.yaml",
    split="test",
    imgsz=640
)

print()
print("Evaluation completed.")
print("mAP50:", results.box.map50)
print("mAP50-95:", results.box.map)