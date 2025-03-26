import streamlit as st
import tensorflow as tf
import numpy as np
import os
import gdown
import google.generativeai as genai
import speech_recognition as sr
from gtts import gTTS
from googletrans import Translator
import tempfile
import whisper
from io import BytesIO
import base64

# Configure Gemini API Key
genai.configure(api_key="AIzaSyAFVkuNLacQo8Z1ihcd3e6dHq3PICOvTRg") 

# Function to load the model
@st.cache_resource
def load_model(plant_type):
    if plant_type == "Other":
        file_id = "1BRBQX4bC3acTwlAwbWqzQ64YzpT5KMrz"  
        url = f"https://drive.google.com/uc?id={file_id}"
        model_path = "trained_model.h5"
        try:
            gdown.download(url, model_path, quiet=False)
        except Exception as e:
            st.error(f"Error downloading model: {e}")
            return None
    else:
        model_path = f"{plant_type.lower()}_model.h5"
    
    try:
        return tf.keras.models.load_model(model_path, compile=False)
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None

# Function for prediction with improved error handling
def model_prediction(model, test_image):
    try:
        image = tf.keras.preprocessing.image.load_img(test_image, target_size=(128, 128))
        input_arr = tf.keras.preprocessing.image.img_to_array(image)
        input_arr = np.expand_dims(input_arr, axis=0)
        prediction = model.predict(input_arr)
        return np.argmax(prediction)
    except Exception as e:
        st.error(f"Error processing image: {e}")
        return None

# Improved speech-to-text function
def process_speech_input():
    try:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            st.write("🎤 Listening...")
            audio = r.listen(source, timeout=5)  # Add timeout
            try:
                text = r.recognize_google(audio)
                return text
            except sr.UnknownValueError:
                st.error("Could not understand audio")
            except sr.RequestError as e:
                st.error(f"Could not request results; {e}")
    except Exception as e:
        st.error(f"Microphone not available: {e}")
    return None

# Cached text-to-speech function
@st.cache_data
def text_to_speech(text, language='en'):
    try:
        tts = gTTS(text=text, lang=language)
        fp = BytesIO()
        tts.write_to_fp(fp)
        return fp.getvalue()
    except Exception as e:
        st.error(f"Error generating speech: {e}")
        return None

# Helper function to create audio player HTML
def get_audio_player_html(audio_data):
    if audio_data:
        b64 = base64.b64encode(audio_data).decode()
        return f'<audio controls><source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>'
    return ""

# Improved get_disease_info function with translation support
def get_disease_info(disease_name, target_language='en'):
    prompt = f"""
    Provide detailed information about the plant disease '{disease_name}', including:
    - Symptoms
    - Causes
    - Best Treatments & Prevention Methods
    - Impact on Crops
    - Natural Remedies
    don't say anything extra suggest in information in  a well structured manner 
    """
    try:
        response = genai.GenerativeModel("gemini-2.0-flash").generate_content(prompt)
        text = response.text
        
        if target_language != 'en':
            try:
                translator = Translator()
                translated = translator.translate(text, dest=target_language)
                if translated and translated.text:
                    text = translated.text
                else:
                    st.warning(f"Translation failed, showing English content")
            except Exception as e:
                st.warning(f"Translation error: {e}. Showing English content")
        return text
    except Exception as e:
        st.warning("⚠️ Unable to fetch or translate disease information.")
        print(f"Error: {e}")
        return "Information could not be retrieved."

# Spotify-like UI Styling
st.markdown("""
<style>
    body {
        background-color: #121212;
        color: #ffffff;
        font-family: 'Arial', sans-serif;
    }
    .header {
        font-size: 36px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 20px;
        color: #1DB954;
    }
    .stButton>button {
        background-color: #1DB954;
        color: #ffffff;
        font-size: 16px;
        padding: 10px 20px;
        border-radius: 5px;
        border: none;
        cursor: pointer;
    }
    .stButton>button:hover {
        background-color: #1ed760;
    }
    .stImage>img {
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    .text-box {
        background-color: rgba(255, 255, 255, 0.1);
        padding: 15px;
        border-radius: 10px;
        margin-top: 20px;
        font-size: 18px;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar Navigation
st.sidebar.title("🎛️ Dashboard")
app_mode = st.sidebar.selectbox("Select Page", ["Home", "About", "Disease Recognition"])

# Home Page
if app_mode == "Home":
    st.markdown('<div class="header">🔍 PLANT DISEASE RECOGNITION SYSTEM 🌿</div>', unsafe_allow_html=True)
    image_path = os.path.join(os.path.dirname(__file__), "home_page.jpg")

    if os.path.exists(image_path):
        st.image(image_path, use_column_width=True)
    else:
        st.error(f"Image not found: {image_path}")
    st.markdown("""
    <div class="text-box">
    **🌿 Welcome to the Plant Disease Recognition System!**
    Our **AI-powered system** helps in identifying plant diseases efficiently. Simply **upload an image**, and our model will analyze it within seconds.
    </div>
    """, unsafe_allow_html=True)

# About Page
elif app_mode == "About":
    st.markdown('<div class="header">📖 About</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="text-box">
    **🌿 About the Dataset**
    This dataset consists of **87,000+ high-resolution images** of healthy and diseased plants, categorized into **38 classes**.
    </div>
    """, unsafe_allow_html=True)

# Disease Recognition Page
elif app_mode == "Disease Recognition":
    st.markdown('<div class="header">🔬 Disease Recognition</div>', unsafe_allow_html=True)
    
    # Initialize session state for language
    if 'language' not in st.session_state:
        st.session_state.language = 'English'
    
    # Language selection
    languages = {
        'English': 'en', 'Spanish': 'es', 'French': 'fr', 
        'German': 'de', 'Italian': 'it', 'Hindi': 'hi'
    }
    selected_language = st.selectbox("🌍 Select Language", 
                                   list(languages.keys()),
                                   key='language')
    lang_code = languages[selected_language]
    
    # Plant type selection with voice input
    col1, col2 = st.columns([3, 1])
    with col1:
        plant_type = st.selectbox("Select Plant Type", ["Other"])
    with col2:
        if st.button("🎤 Voice Input"):
            plant_name = process_speech_input()
            if plant_name:
                st.write(f"Heard: {plant_name}")
                
    # Image upload section
    use_camera = st.checkbox("📷 Use Camera")
    camera_image = st.camera_input("Take a picture:") if use_camera else None
    test_image = st.file_uploader("📁 Upload Image")
    selected_image = camera_image if camera_image is not None else test_image

    if selected_image:
        st.image(selected_image, use_column_width=True, caption="📷 Selected Image")
        if st.button("🔍 Predict Disease"):
            # Load model with status indicator
            with st.spinner("Loading model..."):
                model = load_model(plant_type)
            
            if model:
                with st.spinner("Analyzing the image..."):
                    result_index = model_prediction(model, selected_image)
                    if result_index is not None:
                        disease_name = class_name[result_index]
                        st.success(f"🌱 Identified Disease: **{disease_name}**")
                        
                        # Get disease information in selected language
                        st.subheader("📖 Disease Information & Treatment")
                        with st.spinner("Fetching disease information..."):
                            disease_info = get_disease_info(disease_name, lang_code)
                            st.markdown(f"<div class='text-box'>{disease_info}</div>", 
                                      unsafe_allow_html=True)
                        
                        # Text-to-speech output
                        with st.spinner("Generating audio..."):
                            audio_data = text_to_speech(disease_info, lang_code)
                            if audio_data:
                                st.markdown("🔊 Listen to the information:")
                                st.markdown(get_audio_player_html(audio_data), 
                                          unsafe_allow_html=True)
                    else:
                        st.error("Failed to process the image. Please try again.")
            else:
                st.error("Failed to load the model. Please check the plant type and try again.")
    else:
        st.warning("📌 Please upload or capture an image to proceed.")
