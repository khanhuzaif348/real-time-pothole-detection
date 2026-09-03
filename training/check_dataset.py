from ultralytics import YOLO
# load small pretrained yolo model
model = YOLO("yolo11n.pt")
#validation THE dataset
model.val(data="data\\data.yaml",split="val")


print("Dataset validation completed successfully. ")