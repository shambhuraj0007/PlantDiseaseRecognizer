import streamlit as st
import time
from PIL import Image
import datetime
import pandas as pd
import pathlib
from utils import load_model, model_prediction, get_disease_info  # Import from utils.py
from pages.home import load_home_page
from pages.disease_recognition import load_disease_recognition_page
from components.sidebar import initialize_sidebar

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

def initialize_app():
    load_css()
    add_bg_elements()

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
    
    st.markdown("""
    <div class="about-section fade-in">
        <h2>🎯 Project Overview</h2>
        <p>Our Plant Disease Recognition System leverages cutting-edge AI technology to help farmers and gardeners 
        identify plant diseases quickly and accurately. This project aims to revolutionize agricultural practices 
        by making disease detection accessible to everyone.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<h2 class="fade-in">📊 Dataset Statistics</h2>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="stats-box fade-in">
        """, unsafe_allow_html=True)

def main():
    initialize_app()
    initialize_sidebar()
    
    # Initialize session state for page persistence
    if 'app_mode' not in st.session_state:
        st.session_state['app_mode'] = "Home"

    # Navigation handling
    with st.sidebar:
        st.markdown('<div class="sidebar-header">Navigation</div>', unsafe_allow_html=True)
        
        pages = ["Home", "Disease Recognition", "About", "Feedback & Support"]
        icons = {
            "Home": "🏠",
            "Disease Recognition": "🔍",
            "About": "ℹ️",
            "Feedback & Support": "📝"
        }
        
        for page in pages:
            if st.sidebar.button(f"{icons[page]} {page}", key=page, use_container_width=True):
                st.session_state['app_mode'] = page

    # Page routing
    if st.session_state['app_mode'] == "Home":
        load_home_page()
    elif st.session_state['app_mode'] == "Disease Recognition":
        load_disease_recognition_page()
    elif st.session_state['app_mode'] == "About":
        render_about_page()
    elif st.session_state['app_mode'] == "Feedback & Support":
        render_feedback_support()

if __name__ == "__main__":
    main()
