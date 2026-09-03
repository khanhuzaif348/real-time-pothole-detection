import streamlit as st
import cv2
import sys
import time
import platform
import streamlit.components.v1 as components
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
# VOICE ALERT
# =========================================================

from src.detection.voice_alert import speak


def browser_speak(message):
    """
    Browser-based text-to-speech.

    This is used on Streamlit Cloud because
    pyttsx3/SAPI5 is Windows-only.
    """

    # Escape characters for JavaScript
    safe_message = (
        message
        .replace("\\", "\\\\")
        .replace("'", "\\'")
        .replace("\n", " ")
    )

    components.html(
        f"""
        <script>
            const message = new SpeechSynthesisUtterance(
                '{safe_message}'
            );

            message.rate = 1.0;
            message.volume = 1.0;

            window.speechSynthesis.cancel();
            window.speechSynthesis.speak(message);
        </script>
        """,
        height=0
    )


def voice_alert(message):
    """
    Use Windows TTS locally.
    Use browser TTS on Streamlit Cloud.
    """

    if platform.system() == "Windows":

        # Local Windows computer
        speak(message)

    else:

        # Streamlit Cloud / Linux
        browser_speak(message)


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

st.write(
    "Pothole detection using a pretrained YOLO model."
)


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
# PRETRAINED MODEL
# =========================================================

model_path = PROJECT_ROOT / "models" / "best.pt"

# Pretrained model:
# 0 = pothole

pothole_class_id = 0


# =========================================================
# LOAD MODEL
# =========================================================

@st.cache_resource
def load_model(path):
    return YOLO(str(path))


model = load_model(model_path)


# =========================================================
# UPLOAD IMAGE
# =========================================================

if input_option == "Upload Image":

    st.subheader("📁 Upload Road Image")

    uploaded_file = st.file_uploader(
        "Choose an image from your folder",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded_file is not None:

        # ---------------------------------------------
        # Read image
        # ---------------------------------------------

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
            # Calculate average confidence
            # -----------------------------------------

            if confidences:

                average_confidence = (
                    sum(confidences)
                    / len(confidences)
                    * 100
                )

            else:

                average_confidence = 0


            # -----------------------------------------
            # Metrics
            # -----------------------------------------

            col1, col2 = st.columns(2)

            with col1:

                st.metric(
                    "🚧 Potholes Detected",
                    pothole_count
                )

            with col2:

                if confidences:

                    st.metric(
                        "📊 Average Confidence",
                        f"{average_confidence:.2f}%"
                    )

                else:

                    st.metric(
                        "📊 Average Confidence",
                        "N/A"
                    )


            # -----------------------------------------
            # Individual detections
            # -----------------------------------------

            if confidences:

                st.subheader("📈 Individual Detections")

                for i, confidence in enumerate(
                    confidences,
                    start=1
                ):

                    st.write(
                        f"Pothole {i}: "
                        f"{confidence * 100:.2f}%"
                    )


                # =====================================
                # VOICE ALERT
                # =====================================

                if pothole_count == 1:

                    message = (
                        "Please ride safely. "
                        "One pothole detected ahead. "
                        f"Confidence is "
                        f"{average_confidence:.1f} percent."
                    )

                else:

                    message = (
                        "Please ride safely. "
                        f"{pothole_count} potholes detected ahead. "
                        f"Average confidence is "
                        f"{average_confidence:.1f} percent."
                    )

                voice_alert(message)


            else:

                st.warning(
                    "No potholes detected."
                )

                message = (
                    "No potholes detected. "
                    "You can continue safely."
                )

                voice_alert(message)


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

            # Time of previous voice alert
            self.last_voice_time = 0

            # Wait 5 seconds before speaking again
            self.voice_cooldown = 5


        def recv(self, frame):

            # -----------------------------------------
            # Convert camera frame
            # -----------------------------------------

            img = frame.to_ndarray(
                format="bgr24"
            )


            # -----------------------------------------
            # YOLO prediction
            # -----------------------------------------

            results = model.predict(
                source=img,
                conf=0.50,
                verbose=False
            )

            result = results[0]


            # -----------------------------------------
            # Process detections
            # -----------------------------------------

            pothole_count = 0
            confidences = []


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


            # =========================================
            # LIVE VOICE ALERT
            # =========================================

            current_time = time.time()


            if (
                pothole_count > 0
                and
                current_time - self.last_voice_time
                >= self.voice_cooldown
            ):

                if pothole_count == 1:

                    message = (
                        "Warning. "
                        "One pothole detected ahead. "
                        f"Confidence is "
                        f"{average_confidence:.0f} percent."
                    )

                else:

                    message = (
                        "Warning. "
                        f"{pothole_count} potholes detected ahead. "
                        f"Average confidence is "
                        f"{average_confidence:.0f} percent."
                    )


                # -------------------------------------
                # Voice
                # -------------------------------------

                voice_alert(message)


                self.last_voice_time = current_time


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


            # -----------------------------------------
            # Return frame
            # -----------------------------------------

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

        rtc_configuration={
            "iceServers": [
                {
                    "urls": [
                        "stun:stun.l.google.com:19302"
                    ]
                }
            ]
        },

        media_stream_constraints={
            "video": True,
            "audio": False
        },

        async_processing=True
    )