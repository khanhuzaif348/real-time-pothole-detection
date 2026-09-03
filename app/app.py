import streamlit as st
import sys
from pathlib import Path

# Project root: D:\AI_pothole_detection
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Add project root to Python's import path
sys.path.insert(0, str(PROJECT_ROOT))

from ultralytics import YOLO
from src.detection.voice_alert import speak
from PIL import Image
import tempfile
import os


# -----------------------------
# Page configuration
# -----------------------------

st.set_page_config(
    page_title="Pothole Detection",
    page_icon="🚧",
    layout="wide"
)


# -----------------------------
# Title
# -----------------------------

st.title("🚧 Pothole Detection System")
st.write("Choose a model and upload a road image.")


# -----------------------------
# Model selection
# -----------------------------

model_option = st.selectbox(
    "Choose Model",
    [
        "My Trained Model",
        "Pretrained Pothole Model"
    ]
)


# -----------------------------
# Load selected model
# -----------------------------

if model_option == "My Trained Model":

    model_path = (
        "runs/detect/outputs/"
        "pothole_model-5/weights/best.pt"
    )

else:

    model_path = "models/best.pt"


@st.cache_resource
def load_model(path):

    return YOLO(path)


model = load_model(model_path)


# -----------------------------
# Upload image
# -----------------------------

uploaded_file = st.file_uploader(
    "Upload a road image",
    type=["jpg", "jpeg", "png"]
)


if uploaded_file is not None:

    image = Image.open(uploaded_file)

    st.subheader("Original Image")

    st.image(
        image,
        use_container_width=True
    )


    # -------------------------
    # Temporary image
    # -------------------------

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".jpg"
    ) as temp_file:

        image.save(temp_file.name)

        temp_path = temp_file.name


    # -------------------------
    # Prediction
    # -------------------------

    results = model.predict(
        source=temp_path,
        conf=0.50,
        verbose=False
    )


    # -------------------------
    # Count potholes
    # -------------------------

    pothole_count = 0
    confidences = []


    for result in results:

        for box in result.boxes:

            class_id = int(box.cls[0])
            confidence = float(box.conf[0])

            # --------------------------------
            # Different class IDs
            # --------------------------------

            if model_option == "My Trained Model":

                # Your model:
                # 0 = crocodile crack
                # 1 = longitudinal crack
                # 2 = pothole

                if class_id == 2:

                    pothole_count += 1
                    confidences.append(confidence)

            else:

                # Pretrained model:
                # 0 = pothole

                if class_id == 0:

                    pothole_count += 1
                    confidences.append(confidence)


    # -------------------------
    # Display result
    # -------------------------

    result_image = results[0].plot()

    st.subheader("Detection Result")

    st.image(
        result_image,
        use_container_width=True
    )


    # -------------------------
    # Metrics
    # -------------------------

    col1, col2 = st.columns(2)


    with col1:

        st.metric(
            "Potholes Detected",
            pothole_count
        )


    with col2:

        if confidences:

            average_confidence = (
                sum(confidences)
                / len(confidences)
                * 100
            )

            st.metric(
                "Average Confidence",
                f"{average_confidence:.2f}%"
            )

        else:

            st.metric(
                "Average Confidence",
                "N/A"
            )


    # -------------------------
    # Individual detections
    # -------------------------

    if confidences:

        st.subheader("Individual Detections")

        for i, confidence in enumerate(
            confidences,
            start=1
        ):

            st.write(
                f"Pothole {i}: "
                f"{confidence * 100:.2f}%"
            )

    else:

        st.warning(
            "No potholes detected."
        )


    # -------------------------
    # Voice Alert logic 
    # -------------------------

    #--------------
# Voice Alert
# -------------------------

    if pothole_count > 0:

        average_confidence = (
        sum(confidences)
        / len(confidences)
        * 100
        )

    if pothole_count == 1:

        speak(
            f"Please ride safely. "
            f"One pothole detected ahead. "
            f"Confidence is {average_confidence:.1f} percent."
        )

    else:

        speak(
            f"Please ride safely. "
            f"{pothole_count} potholes detected ahead. "
            f"Average confidence is {average_confidence:.1f} percent."
        )

    # -------------------------
    # Remove temporary file
    # -------------------------

    os.remove(temp_path)