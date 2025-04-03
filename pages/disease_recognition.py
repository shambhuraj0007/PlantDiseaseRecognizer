import streamlit as st
import time
import os
from PIL import Image
from app import load_model, model_prediction, get_disease_info  # Import from app.py

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
            with st.spinner("Analyzing image with AI..."):
                # Load the model
                model = load_model(plant_type)
                if model is None:
                    st.error("Model loading failed. Please try again.")
                    return

                # Save uploaded image temporarily
                with open("temp_image.jpg", "wb") as f:
                    f.write(st.session_state['selected_image'].getvalue())

                # Get prediction
                result_index, confidence, prediction = model_prediction(model, "temp_image.jpg")
                if result_index is None:
                    st.error("Prediction failed. Please try again.")
                    return

                # Mock disease names (replace with your actual class names)
                disease_names = ["Healthy", "Early Blight", "Late Blight", "Other"]
                detected_disease = disease_names[result_index]

                # Get disease info
                disease_info = get_disease_info(detected_disease)

                # Mark analysis as done
                st.session_state['analysis_done'] = True
                st.session_state['detected_disease'] = detected_disease
                st.session_state['confidence'] = confidence
                st.session_state['disease_info'] = disease_info

                # Clean up
                if os.path.exists("temp_image.jpg"):
                    os.remove("temp_image.jpg")

        # Show results if analysis is done
        if st.session_state.get('analysis_done', False):
            st.markdown(f"""
            <div class="dr-results-container">
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
                
                <div class="dr-diagnosis">
                    <h3>Detected Disease</h3>
                    <div class="dr-disease-name">{st.session_state['detected_disease']}</div>
                    <div class="dr-disease-info">
                        <h4>About this Disease</h4>
                        <p>{st.session_state['disease_info']}</p>
                    </div>
                </div>

                <div class="dr-actions">
                    <button class="dr-action-button primary">
                        <span>📋 View Detailed Report</span>
                    </button>
                    <button class="dr-action-button secondary">
                        <span>🔄 Try Another Image</span>
                    </button>
                    <button class="dr-action-button tertiary">
                        <span>💬 Consult Expert</span>
                    </button>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Action Buttons
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
