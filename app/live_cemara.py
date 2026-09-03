import streamlit as st
import cv2
import sys
from pathlib import Path

from PIL import Image
from ultralytics import YOLO
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase


# =========================================================
# PROJECT ROOT
# =========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(PROJECT_ROOT))


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Pothole Detection",
    page_icon="🚧",
    layout="wide"
)


# =========================================================
# TITLE
# =========================================================

st.title("🚧 Pothole Detection System")


# =========================================================
# INPUT SELECTION
# =========================================================

input_option = st.radio(
    "Choose Input",
    [
        "Upload Image",
        "Live Camera"
    ],
    horizontal=True
)


# =========================================================
# MODEL SELECTION
# =========================================================

model_option = st.selectbox(
    "Choose Model",
    [
        "My Trained Model",
        "Pretrained Pothole Model"
    ]
)


# =========================================================
# MODEL CONFIGURATION
# =========================================================

if model_option == "My Trained Model":

    model_path = (
        PROJECT_ROOT
        / "runs"
        / "detect"
        / "outputs"
        / "pothole_model-5"
        / "weights"
        / "best.pt"
    )

    pothole_class_id = 2

else:

    model_path = (
        PROJECT_ROOT
        / "models"
        / "best.pt"
    )

    pothole_class_id = 0


@st.cache_resource
def load_model(path):

    return YOLO(str(path))


model = load_model(model_path)


# =========================================================
# UPLOAD IMAGE
# =========================================================

if input_option == "Upload Image":

    uploaded_file = st.file_uploader(
        "Choose an image from your folder",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded_file is not None:

        image = Image.open(uploaded_file)

        st.subheader("Original Image")

        st.image(
            image,
            use_container_width=True
        )

        # ---------------------------------------------
        # Detect button
        # ---------------------------------------------

        if st.button("🔍 Detect Potholes"):

            results = model.predict(
                source=image,
                conf=0.50,
                verbose=False
            )

            result = results[0]

            pothole_count = 0
            confidences = []

            # -----------------------------------------
            # Process detections
            # -----------------------------------------

            for box in result.boxes:

                class_id = int(box.cls[0])
                confidence = float(box.conf[0])

                if class_id == pothole_class_id:

                    pothole_count += 1
                    confidences.append(confidence)

            # -----------------------------------------
            # Result image
            # -----------------------------------------

            result_image = result.plot()

            st.subheader("Detection Result")

            st.image(
                result_image,
                use_container_width=True
            )

            # -----------------------------------------
            # Metrics
            # -----------------------------------------

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

            # -----------------------------------------
            # Individual detections
            # -----------------------------------------

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


# =========================================================
# LIVE CAMERA
# =========================================================

else:

    st.subheader("📷 Live Camera")

    st.write(
        "Click START and allow camera permission."
    )


    # =====================================================
    # LIVE CAMERA PROCESSOR
    # =====================================================

    class PotholeProcessor(VideoProcessorBase):

        def __init__(self):

            self.pothole_count = 0
            self.average_confidence = 0.0


        def recv(self, frame):

            # Convert camera frame to OpenCV
            img = frame.to_ndarray(
                format="bgr24"
            )

            # YOLO prediction
            results = model.predict(
                source=img,
                conf=0.50,
                verbose=False
            )

            result = results[0]

            pothole_count = 0
            confidences = []


            # -----------------------------------------
            # Process detections
            # -----------------------------------------

            for box in result.boxes:

                class_id = int(box.cls[0])
                confidence = float(box.conf[0])

                if class_id == pothole_class_id:

                    pothole_count += 1
                    confidences.append(
                        confidence
                    )


            # -----------------------------------------
            # Average confidence
            # -----------------------------------------

            if confidences:

                average_confidence = (
                    sum(confidences)
                    / len(confidences)
                    * 100
                )

            else:

                average_confidence = 0.0


            # -----------------------------------------
            # Save values
            # -----------------------------------------

            self.pothole_count = pothole_count
            self.average_confidence = (
                average_confidence
            )


            # -----------------------------------------
            # Draw YOLO result
            # -----------------------------------------

            annotated_frame = result.plot()


            # -----------------------------------------
            # Display pothole count
            # -----------------------------------------

            cv2.putText(
                annotated_frame,
                f"Potholes: {pothole_count}",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2
            )


            # -----------------------------------------
            # Display confidence
            # -----------------------------------------

            cv2.putText(
                annotated_frame,
                f"Confidence: {average_confidence:.2f}%",
                (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2
            )


            # Return frame
            return frame.from_ndarray(
                annotated_frame,
                format="bgr24"
            )


    # =====================================================
    # START CAMERA
    # =====================================================

    webrtc_streamer(
        key="pothole-live-camera",
        video_processor_factory=PotholeProcessor,
        media_stream_constraints={
            "video": True,
            "audio": False
        },
        async_processing=True
    )