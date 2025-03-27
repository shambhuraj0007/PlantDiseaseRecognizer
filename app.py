import streamlit as st
import tensorflow as tf
import numpy as np
import os
import gdown
import google.generativeai as genai
import time
from PIL import Image
import datetime
import pandas as pd
import pathlib
from pages.home import load_home_page
from pages.disease_recognition import load_disease_recognition_page
from components.sidebar import initialize_sidebar

# Configure Gemini API Key
genai.configure(api_key="AIzaSyAFVkuNLacQo8Z1ihcd3e6dHq3PICOvTRg") 

def add_bg_elements():
    """Add background elements to the page"""
    st.markdown("""
    <div class="page-overlay"></div>
    <div class="particles">
        <div class="particle" style="left: 10%; top: 20%; width: 8px; height: 8px;"></div>
        <div class="particle" style="left: 20%; top: 60%; width: 12px; height: 12px;"></div>
        <div class="particle" style="left: 50%; top: 30%; width: 10px; height: 10px;"></div>
        <div class="particle" style="left: 70%; top: 70%; width: 15px; height: 15px;"></div>
        <div class="particle" style="left: 80%; top: 20%; width: 6px; height: 6px;"></div>
        <div class="particle" style="left: 30%; top: 80%; width: 9px; height: 9px;"></div>
    </div>
    """, unsafe_allow_html=True)

def load_css():
    """Load and apply CSS styles"""
    css_files = [
        pathlib.Path(__file__).parent / 'static' / 'background_styles.css',
        pathlib.Path(__file__).parent / 'static' / 'styles.css',
        pathlib.Path(__file__).parent / 'static' / 'home_styles.css',
        pathlib.Path(__file__).parent / 'static' / 'disease_recognition_styles.css',
        pathlib.Path(__file__).parent / 'static' / 'sidebar_styles.css'
    ]
    
    for css_file in css_files:
        try:
            with open(css_file) as f:
                st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
        except FileNotFoundError:
            st.error(f"CSS file not found: {css_file}")

# Initialize CSS and background
def initialize_app():
    load_css()
    add_bg_elements()

# Function to load the model
@st.cache_resource
def load_model(plant_type):
    try:
        if plant_type == "Other":
            file_id = "1BRBQX4bC3acTwlAwbWqzQ64YzpT5KMrz"  
            url = f"https://drive.google.com/uc?id={file_id}"
            model_path = "trained_model.h5"
            gdown.download(url, model_path, quiet=False)
        else:
            model_path = f"{plant_type.lower()}_model.h5"
        
        return tf.keras.models.load_model(model_path, compile=False)
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None

# Function for prediction
def model_prediction(model, test_image):
    try:
        image = tf.keras.preprocessing.image.load_img(test_image, target_size=(128, 128))
        input_arr = tf.keras.preprocessing.image.img_to_array(image)
        input_arr = np.expand_dims(input_arr, axis=0)
        prediction = model.predict(input_arr)
        confidence = float(np.max(prediction[0])) * 100
        result_index = np.argmax(prediction)
        return result_index, confidence, prediction
    except Exception as e:
        st.error(f"Error during prediction: {e}")
        return None, None, None

# Function to get disease info
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

def render_feedback_support():
    st.markdown('<div class="header fade-in">📢 Feedback & Support Center</div>', unsafe_allow_html=True)
    
    feedback_tab, support_tab, survey_tab, collaboration_tab = st.tabs([
        "Submit Feedback", "Get Support", "User Survey", "Collaboration"
    ])
    
    with feedback_tab:
        render_feedback_form()
    
    with support_tab:
        render_support_section()
    
    with survey_tab:
        render_survey_form()
    
    with collaboration_tab:
        render_collaboration_form()

def render_feedback_form():
    st.markdown("""
    <div class="about-section fade-in">
        <h2>🌟 Share Your Experience</h2>
        <p>Your feedback helps us improve and serve farmers better across the nation.</p>
    </div>
    """, unsafe_allow_html=True)
    
    feedback_form = st.form("feedback_form")
    with feedback_form:
        user_type = st.selectbox(
            "I am a:",
            ["Farmer", "Agricultural Expert", "Researcher", "Student", "Other"]
        )
        
        state = st.selectbox(
            "State:",
            ["Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", 
             "Chhattisgarh", "Goa", "Gujarat", "Haryana", "Himachal Pradesh",
             "Jharkhand", "Karnataka", "Kerala", "Madhya Pradesh", 
             "Maharashtra", "Manipur", "Meghalaya", "Mizoram", "Nagaland",
             "Odisha", "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu",
             "Telangana", "Tripura", "Uttar Pradesh", "Uttarakhand",
             "West Bengal"]
        )
        
        rating = st.slider("How would you rate our service?", 1, 5, 5)
        
        feedback_categories = st.multiselect(
            "What aspects would you like to provide feedback on?",
            ["Disease Detection Accuracy", "User Interface", "Speed",
             "Treatment Recommendations", "Mobile Experience",
             "Local Language Support", "Other"]
        )
        
        detailed_feedback = st.text_area("Your Detailed Feedback")
        
        if st.form_submit_button("Submit Feedback"):
            st.success("Thank you for your valuable feedback! Your input helps us serve farmers better across India.")

def render_support_section():
    st.markdown("""
    <div class="about-section fade-in">
        <h2>🆘 Get Support</h2>
        <p>Need help? We're here to support you.</p>
    </div>
    """, unsafe_allow_html=True)
    
    support_type = st.selectbox(
        "What kind of support do you need?",
        ["Technical Support", "Disease Identification Help", "App Usage Guide",
         "Regional Language Support", "Other"]
    )
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="about-section">
            <h3>📞 Helpline Numbers</h3>
            <ul>
                <li>Technical Support: 1800-XXX-XXXX</li>
                <li>Agricultural Expert: 1800-XXX-XXXX</li>
                <li>24x7 Support: 1800-XXX-XXXX</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="about-section">
            <h3>📧 Email Support</h3>
            <ul>
                <li>Technical: support@plantcare.in</li>
                <li>General: info@plantcare.in</li>
                <li>Collaboration: partner@plantcare.in</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

def render_survey_form():
    st.markdown("""
    <div class="about-section fade-in">
        <h2>📊 Agricultural Survey</h2>
        <p>Help us understand the agricultural landscape better.</p>
    </div>
    """, unsafe_allow_html=True)
    
    survey_form = st.form("survey_form")
    with survey_form:
        farm_size = st.selectbox(
            "Farm Size (in acres)",
            ["Less than 1", "1-5", "5-10", "10-20", "More than 20"]
        )
        
        crops = st.multiselect(
            "What crops do you primarily grow?",
            ["Rice", "Wheat", "Cotton", "Sugarcane", "Pulses",
             "Vegetables", "Fruits", "Other"]
        )
        
        challenges = st.multiselect(
            "What are your biggest challenges?",
            ["Plant Diseases", "Weather", "Water Supply", "Market Prices",
             "Labor", "Technology Adoption", "Other"]
        )
        
        tech_usage = st.select_slider(
            "How comfortable are you with agricultural technology?",
            options=["Beginner", "Intermediate", "Advanced", "Expert"]
        )
        
        if st.form_submit_button("Submit Survey"):
            st.success("Thank you for participating in our survey! Your insights will help shape the future of Indian agriculture.")

def render_collaboration_form():
    st.markdown("""
    <div class="about-section fade-in">
        <h2>🤝 Collaboration Opportunities</h2>
        <p>Partner with us in revolutionizing Indian agriculture.</p>
    </div>
    """, unsafe_allow_html=True)
    
    partner_type = st.selectbox(
        "Partnership Category",
        ["Agricultural Institution", "Research Organization", "Government Body",
         "NGO", "Private Company", "Educational Institution", "Other"]
    )
    
    collab_form = st.form("collaboration_form")
    with collab_form:
        organization = st.text_input("Organization Name")
        contact_person = st.text_input("Contact Person")
        email = st.text_input("Official Email")
        phone = st.text_input("Contact Number")
        
        collaboration_interest = st.multiselect(
            "Areas of Interest",
            ["Research Partnership", "Data Sharing", "Technology Integration",
             "Field Testing", "Training Programs", "Funding", "Other"]
        )
        
        proposal = st.text_area("Brief Proposal")
        
        if st.form_submit_button("Submit Proposal"):
            st.success("Thank you for your interest in collaboration! Our team will contact you soon.")

def render_about_page():
    st.markdown('<div class="header fade-in">📖 About Our Project</div>', unsafe_allow_html=True)
    
    # Project Overview Section
    st.markdown("""
    <div class="about-section fade-in">
        <h2>🎯 Project Overview</h2>
        <p>Our Plant Disease Recognition System leverages cutting-edge AI technology to help farmers and gardeners 
        identify plant diseases quickly and accurately. This project aims to revolutionize agricultural practices 
        by making disease detection accessible to everyone.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Dataset Statistics with Animation
    st.markdown('<h2 class="fade-in">📊 Dataset Statistics</h2>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="stats-box fade-in">
        """, unsafe_allow_html=True)

def main():
    initialize_app()
    initialize_sidebar()
    
    # Navigation handling
    with st.sidebar:
        st.markdown('<div class="sidebar-header">Navigation</div>', unsafe_allow_html=True)
        
        pages = ["Home", "Disease Recognition", "About", "Feedback & Support"]
        app_mode = None
        
        for page in pages:
            icon = {
                "Home": "🏠",
                "Disease Recognition": "🔍",
                "About": "ℹ️",
                "Feedback & Support": "📝"
            }[page]
            
            if st.sidebar.button(f"{icon} {page}", key=page, use_container_width=True):
                app_mode = page
        
        if app_mode is None:
            app_mode = "Home"

    # Page routing
    if app_mode == "Home":
        load_home_page()
    elif app_mode == "Disease Recognition":
        load_disease_recognition_page()
    elif app_mode == "About":
        render_about_page()
    elif app_mode == "Feedback & Support":
        render_feedback_support()

if __name__ == "__main__":
    main()
