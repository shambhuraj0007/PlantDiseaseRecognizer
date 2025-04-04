import tensorflow as tf
import numpy as np
import os
import gdown
import google.generativeai as genai
import streamlit as st

# Configure Gemini API Key (use environment variables in production)
genai.configure(api_key="AIzaSyAFVkuNLacQo8Z1ihcd3e6dHq3PICOvTRg")

@st.cache_resource
def load_model(plant_type):
    try:
        if plant_type == "Other":
            file_id = "1BRBQX4bC3acTwlAwbWqzQ64YzpT5KMrz"
            url = f"https://drive.google.com/uc?id={file_id}"
            model_path = "trained_model.h5"
            if not os.path.exists(model_path):
                st.info("Downloading model... This may take a moment.")
                gdown.download(url, model_path, quiet=False)
        else:
            model_path = f"{plant_type.lower()}_model.h5"
            if not os.path.exists(model_path):
                st.error(f"Model file not found: {model_path}")
                return None
        
        st.info("Loading model...")
        model = tf.keras.models.load_model(model_path, compile=False)
        model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
        return model
    except Exception as e:
        st.error(f"Error loading model: {str(e)}")
        return None

def model_prediction(model, test_image):
    try:
        # Load and preprocess the image
        image = tf.keras.preprocessing.image.load_img(test_image, target_size=(128, 128))
        input_arr = tf.keras.preprocessing.image.img_to_array(image)
        input_arr = np.expand_dims(input_arr, axis=0)
        
        # Normalize the input
        input_arr = input_arr / 255.0
        
        # Make prediction
        prediction = model.predict(input_arr)
        
        # Get confidence and result index
        confidence = float(np.max(prediction[0])) * 100
        result_index = np.argmax(prediction)
        
        return result_index, confidence, prediction
    except Exception as e:
        st.error(f"Error during prediction: {str(e)}")
        return None, None, None

def get_disease_info(disease_name):
    prompt = f"""
    Provide detailed information about the plant disease '{disease_name}', including:
    - Symptoms
    - Causes
    - Best Treatments & Prevention Methods
    - Impact on Crops
    - Natural Remedies
    don't say anything extra suggest in information in a well structured manner 
    """
    try:
        response = genai.GenerativeModel("gemini-2.0-flash").generate_content(prompt)
        return response.text
    except Exception as e:
        st.warning("⚠️ Unable to fetch detailed disease information at the moment. Please try again later.")
        print(f"Error calling Gemini API: {e}")
        return "Detailed disease information could not be retrieved due to an API error."
