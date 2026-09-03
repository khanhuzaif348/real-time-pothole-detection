from detection_logger import log_detection


log_detection(
    model_name="Pretrained YOLOv8",
    input_type="Camera",
    image_name="test.jpg",
    pothole_count=2,
    confidences=[0.91, 0.84]
)

print("Detection logged successfully!")