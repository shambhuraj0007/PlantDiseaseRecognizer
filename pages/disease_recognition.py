import streamlit as st
import time
import os
from PIL import Image
from utils import load_model, model_prediction, get_disease_info  # Import from utils.py

def load_disease_recognition_page():
    # Initialize session state for persistence
    if 'use_camera' not in st.session_state:
        st.session_state['use_camera'] = False
    if 'selected_image' not in st.session_state:
        st.session_state['selected_image'] = None
    if 'analysis_done' not in st.session_state:
        st.session_state['analysis_done'] = False

    # Hero Section
    st.markdown("""
    <div class="page-transition">
        <div class="glass-card dr-hero-section">
            <div class="dr-hero-content">
                <h1 class="dr-title">AI-Powered Disease Detection</h1>
                <p class="dr-tagline">Get instant, accurate plant disease diagnosis with our advanced AI technology</p>
                <div class="dr-stats">
                    <div class="dr-stat-item">
                        <div class="dr-stat-number">95%</div>
                        <div class="dr-stat-label">Accuracy</div>
                    </div>
                    <div class="dr-stat-item">
                        <div class="dr-stat-number">38+</div>
                        <div class="dr-stat-label">Diseases</div>
                    </div>
                    <div class="dr-stat-item">
                        <div class="dr-stat-number">10K+</div>
                        <div class="dr-stat-label">Scans</div>
                    </div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Upload Section
    st.markdown("""
        <div class="glass-card dr-upload-section">
            <div class="dr-upload-container">
                <div class="dr-upload-header">
                    <h2>Upload Plant Image</h2>
                    <p>Drag and drop or click to upload</p>
                </div>
    """, unsafe_allow_html=True)

    # Upload Options
    col1, col2 = st.columns(2)
    with col1:
        st.session_state['use_camera'] = st.checkbox("📷 Use Camera", key="dr_camera", value=st.session_state['use_camera'])
    with col2:
        st.markdown('<div class="dr-sample-text">or try a sample image</div>', unsafe_allow_html=True)

    # Camera/Upload Interface
    if st.session_state['use_camera']:
        camera_image = st.camera_input("", key="dr_camera_input")
        if camera_image:
            st.session_state['selected_image'] = camera_image
    else:
        uploaded_file = st.file_uploader("", type=["jpg", "jpeg", "png"], key="dr_file_upload")
        if uploaded_file:
            st.session_state['selected_image'] = uploaded_file

    st.markdown("</div></div>", unsafe_allow_html=True)

    # Display and Analysis Section
    if st.session_state['selected_image']:
        st.markdown('<div class="dr-analysis-section">', unsafe_allow_html=True)
        
        # Image Preview
        st.markdown('<div class="dr-preview-container">', unsafe_allow_html=True)
        st.image(st.session_state['selected_image'], use_column_width=True, caption="Selected Image")
        st.markdown('</div>', unsafe_allow_html=True)

        # Plant Type Selection
        plant_type = st.selectbox("Select Plant Type", ["Tomato", "Potato", "Other"], key="dr_plant_type")
        
        # Analysis Button
        if st.button("🔍 Analyze Image", key="dr_analyze"):
            try:
                with st.spinner("Analyzing image with AI..."):
                    # Load the model
                    model = load_model(plant_type)
                    if model is None:
                        st.error("Model loading failed. Please try again.")
                        return

                    # Create temp directory if it doesn't exist
                    temp_dir = "temp"
                    if not os.path.exists(temp_dir):
                        os.makedirs(temp_dir)

                    # Save uploaded image temporarily with unique name
                    temp_image_path = os.path.join(temp_dir, f"temp_image_{time.time()}.jpg")
                    try:
                        # Convert image to RGB if needed
                        image = Image.open(st.session_state['selected_image'])
                        if image.mode != 'RGB':
                            image = image.convert('RGB')
                        image.save(temp_image_path)

                        # Get prediction
                        result_index, confidence, prediction = model_prediction(model, temp_image_path)
                        if result_index is None:
                            st.error("Prediction failed. Please try again.")
                            return

                        # Define disease names based on your model
                        disease_names = [
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

                        if result_index >= len(disease_names):
                            st.error("Invalid prediction result. Please try again.")
                            return

                        detected_disease = disease_names[result_index]

                        # Get disease info
                        disease_info = get_disease_info(detected_disease)

                        # Store results in session state
                        st.session_state['analysis_done'] = True
                        st.session_state['detected_disease'] = detected_disease
                        st.session_state['confidence'] = confidence
                        st.session_state['disease_info'] = disease_info

                    finally:
                        # Clean up temporary file
                        if os.path.exists(temp_image_path):
                            os.remove(temp_image_path)
                        
            except Exception as e:
                st.error(f"An error occurred during analysis: {str(e)}")
                st.session_state['analysis_done'] = False

        # Display Results if Analysis is Done
        if st.session_state['analysis_done']:
            # Dynamically render results using Streamlit components
            st.markdown('<div class="dr-results-container">', unsafe_allow_html=True)
            
            # Header with Confidence
            st.markdown(f"""
            <div class="dr-result-header">
                <h2>Analysis Results</h2>
                <div class="dr-confidence">
                    <div class="dr-confidence-label">Confidence Score</div>
                    <div class="dr-confidence-meter">
                        <div class="dr-confidence-fill" style="width: {st.session_state['confidence']}%;"></div>
                    </div>
                    <div class="dr-confidence-value">{st.session_state['confidence']:.1f}%</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Diagnosis Section
            st.markdown('<div class="dr-diagnosis">', unsafe_allow_html=True)
            st.markdown("<h3>Detected Disease</h3>", unsafe_allow_html=True)
            st.markdown(f'<div class="dr-disease-name">{st.session_state["detected_disease"]}</div>', unsafe_allow_html=True)
            st.markdown('<div class="dr-disease-info">', unsafe_allow_html=True)
            st.markdown("<h4>About this Disease</h4>", unsafe_allow_html=True)
            st.markdown(f'<p>{st.session_state["disease_info"]}</p>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

            # Action Buttons
            st.markdown('<div class="dr-actions">', unsafe_allow_html=True)
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("📋 View Detailed Report", key="dr_report"):
                    st.write(st.session_state['disease_info'])
            with col2:
                if st.button("🔄 Try Another Image", key="dr_reset"):
                    st.session_state['selected_image'] = None
                    st.session_state['analysis_done'] = False
                    st.experimental_rerun()
            with col3:
                if st.button("💬 Consult Expert", key="dr_consult"):
                    st.write("Contact our experts at support@plantcare.in or call 1800-XXX-XXXX")
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    # Quick Tips Section
    st.markdown("""
    <div class="dr-tips-section">
        <h3>📸 Tips for Better Results</h3>
        <div class="dr-tips-container">
            <div class="dr-tip-card">
                <div class="dr-tip-icon">🎯</div>
                <div class="dr-tip-text">Focus on affected area</div>
            </div>
            <div class="dr-tip-card">
                <div class="dr-tip-icon">☀️</div>
                <div class="dr-tip-text">Good lighting</div>
            </div>
            <div class="dr-tip-card">
                <div class="dr-tip-icon">📏</div>
                <div class="dr-tip-text">Close-up shot</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
