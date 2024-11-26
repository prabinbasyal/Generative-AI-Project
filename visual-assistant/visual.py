import streamlit as st
from PIL import Image
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_core.messages import HumanMessage
import pytesseract
from gtts import gTTS
import io
import base64
import logging

# Initialize API and models
GOOGLE_API_KEY = "AIzaSyD4RC0-z-0l0bWQKG9Gohgq-cWF-pQwceQ"
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=GOOGLE_API_KEY)
vision_llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=GOOGLE_API_KEY)

def handle_error(error):
    logging.error(error)
    st.error(f"Error: {str(error)}")

def analyze_image(image, prompt):
    try:
        image_bytes = io.BytesIO()
        image.save(image_bytes, format='PNG')
        image_bytes = image_bytes.getvalue()

        message = HumanMessage(content=[
            {"type": "text", "text": prompt},
            {"type": "image_url", "image_url": f"data:image/png;base64,{base64.b64encode(image_bytes).decode()}"}
        ])
        return vision_llm.invoke([message]).content
    except Exception as e:
        handle_error(e)


def text_to_speech(text):
    try:
        tts = gTTS(text=text, lang='en')
        mp3_fp = io.BytesIO()
        tts.write_to_fp(mp3_fp)
        mp3_fp.seek(0)
        return mp3_fp.getvalue()
    except Exception as e:
        handle_error(e)

def main():
    st.set_page_config(page_title="Vision Assistant", layout="wide")
    st.title(" AI Assistant for Visually Impaired")


# Add a sidebar with bullet points
    st.sidebar.title('About project')
    st.sidebar.info("AI Assistant for visually impaired users. Upload images to get: ")


# Adding bullet points to the sidebar
    st.sidebar.markdown("""
    - Real-Time Scene Understanding
    - Text-to-Speech Conversion for Visual Content
    - Object and Obstacle Detection for Safe Navigation
    - Personalized Assistance for Daily Tasks
    """)

    uploaded_file = st.file_uploader("Upload an image", type=['jpg', 'jpeg', 'png'])

    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image")

        feature = st.radio("Select Feature", ["Scene Description", "Object Detection", "Task Assistance"])

        if feature == "Scene Description" and st.button("Analyze Scene"):
            with st.spinner("Analyzing scene..."):
                description = analyze_image(image, "Provide a detailed description of this image for a visually impaired person.")
                st.write(description)
                st.audio(text_to_speech(description), format="audio/mp3")


        elif feature == "Object Detection" and st.button("Detect Objects"):
            with st.spinner("Analyzing objects..."):
                objects_info = analyze_image(image, "Identify objects and obstacles in this image.")
                st.write(objects_info)
                st.audio(text_to_speech(objects_info), format="audio/mp3")

        elif feature == "Task Assistance":
            task_type = st.selectbox("Select Task Type", ["item_identification", "label_reading", "navigation_help", "daily_tasks"])
            task_prompts = {
                "item_identification": "Identify and describe items in this image.",
                "label_reading": "Analyze labels and text in this image.",
                "navigation_help": "Provide navigation guidance for this space.",
                "daily_tasks": "Give step-by-step guidance for daily tasks in this image."
            }
            if st.button("Get Assistance"):
                with st.spinner("Generating assistance..."):
                    guidance = analyze_image(image, task_prompts[task_type])
                    st.write(guidance)
                    st.audio(text_to_speech(guidance), format="audio/mp3")

if __name__ == "__main__":
    main()
