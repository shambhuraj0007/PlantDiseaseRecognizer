import streamlit as st
import tensorflow as tf
import numpy as np
import os
import gdown
import google.generativeai as genai

# Configure Gemini API Key
genai.configure(api_key="AIzaSyA07RIpDDtDlsEF7BxoTAmCYceXHPycdAk") 

# Function to load the model
@st.cache_resource
def load_model(plant_type):
    if plant_type == "Other":
        file_id = "1BRBQX4bC3acTwlAwbWqzQ64YzpT5KMrz"  
        url = f"https://drive.google.com/uc?id={file_id}"
        model_path = "trained_model.h5"
        gdown.download(url, model_path, quiet=False)
    else:
        model_path = f"{plant_type.lower()}_model.h5"
    
    try:
        return tf.keras.models.load_model(model_path, compile=False)
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None

# Function for prediction
def model_prediction(model, test_image):
    image = tf.keras.preprocessing.image.load_img(test_image, target_size=(128, 128))
    input_arr = tf.keras.preprocessing.image.img_to_array(image)
    input_arr = np.expand_dims(input_arr, axis=0)
    prediction = model.predict(input_arr)
    return np.argmax(prediction)

# Function to get disease info
def get_disease_info(disease_name):
    prompt = f"""
    Provide detailed information about the plant disease '{disease_name}', including:
    - Symptoms
    - Causes
    - Best Treatments & Prevention Methods
    - Impact on Crops
    - Natural Remedies
    """
    response = genai.GenerativeModel("gemini-pro").generate_content(prompt)
    return response.text

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
    plant_type = st.selectbox("Select Plant Type", ["Other"])
    use_camera = st.checkbox("📷 Use Camera")
    camera_image = st.camera_input("Take a picture:") if use_camera else None
    test_image = st.file_uploader("📁 Upload Image")
    selected_image = camera_image if camera_image is not None else test_image

    if selected_image:
        st.image(selected_image, use_container_width=True, caption="📷 Selected Image")
        if st.button("🔍 Predict Disease"):
            with st.spinner("Analyzing the image..."):
                model = load_model(plant_type)
                if model:
                    result_index = model_prediction(model, selected_image)
                    class_name = [
        'Apple__Apple_scab', 'Apple_Black_rot', 'Apple_Cedar_apple_rust', 'Apple__healthy',
        'Blueberry__healthy', 'Cherry(including_sour)___Powdery_mildew', 
        'Cherry_(including_sour)__healthy', 'Corn(maize)___Cercospora_leaf_spot Gray_leaf_spot',
        'Corn_(maize)__Common_rust', 'Corn_(maize)__Northern_Leaf_Blight', 'Corn(maize)___healthy',
        'Grape__Black_rot', 'Grape_Esca(Black_Measles)', 'Grape__Leaf_blight(Isariopsis_Leaf_Spot)',
        'Grape__healthy', 'Orange_Haunglongbing(Citrus_greening)', 'Peach___Bacterial_spot',
        'Peach__healthy', 'Pepper,_bell_Bacterial_spot', 'Pepper,_bell_healthy', 'Potato__Early_blight',
        'Potato__Late_blight', 'Potato_healthy', 'Raspberry_healthy', 'Soybean__healthy',
        'Squash__Powdery_mildew', 'Strawberry_Leaf_scorch', 'Strawberry_healthy', 'Tomato__Bacterial_spot',
        'Tomato__Early_blight', 'Tomato_Late_blight', 'Tomato_Leaf_Mold', 'Tomato__Septoria_leaf_spot',
        'Tomato__Spider_mites Two-spotted_spider_mite', 'Tomato__Target_Spot', 
        'Tomato__Tomato_Yellow_Leaf_Curl_Virus', 'Tomato_Tomato_mosaic_virus', 'Tomato__healthy'
    ]
                    disease_name = class_name[result_index]
                    st.success(f"🌱 Identified Disease: **{disease_name}**")
                    st.subheader("📖 Disease Information & Treatment")
                    disease_info = get_disease_info(disease_name)
                    st.markdown(f"<div class='text-box'>{disease_info}</div>", unsafe_allow_html=True)
                else:
                    st.error("Failed to load the model. Please check the plant type and try again.")
    else:
        st.warning("📌 Please upload or capture an image to proceed.")
