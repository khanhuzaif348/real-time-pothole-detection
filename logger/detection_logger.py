import csv
from pathlib import Path
from datetime import datetime


# Location of CSV log file
LOG_FILE = Path("logger/detection_logs.csv")


def log_detection(
    model_name,
    input_type,
    image_name,
    pothole_count,
    confidences
):
    """
    Save one detection result into the CSV log.
    """

    # Create logger folder if it doesn't exist
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

    # Calculate confidence statistics
    if confidences:
        average_confidence = sum(confidences) / len(confidences)
        highest_confidence = max(confidences)
    else:
        average_confidence = 0
        highest_confidence = 0

    # Check whether CSV already exists
    file_exists = LOG_FILE.exists()

    with open(LOG_FILE, "a", newline="", encoding="utf-8") as file:

        writer = csv.writer(file)

        # Create header only once
        if not file_exists:
            writer.writerow([
                "timestamp",
                "model",
                "input_type",
                "image_name",
                "pothole_count",
                "average_confidence",
                "highest_confidence"
            ])

        # Add detection record
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            model_name,
            input_type,
            image_name,
            pothole_count,
            f"{average_confidence * 100:.2f}%",
            f"{highest_confidence * 100:.2f}%"
        ])