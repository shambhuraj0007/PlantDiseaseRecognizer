import streamlit as st
import time

def load_disease_recognition_page():
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
        use_camera = st.checkbox("📷 Use Camera", key="dr_camera")
    with col2:
        st.markdown('<div class="dr-sample-text">or try a sample image</div>', unsafe_allow_html=True)
        
    # Camera/Upload Interface
    if use_camera:
        camera_image = st.camera_input("", key="dr_camera_input")
        selected_image = camera_image
    else:
        uploaded_file = st.file_uploader("", type=["jpg", "jpeg", "png"], key="dr_file_upload")
        selected_image = uploaded_file

    st.markdown("</div></div>", unsafe_allow_html=True)

    # Display and Analysis Section
    if selected_image:
        st.markdown('<div class="dr-analysis-section">', unsafe_allow_html=True)
        
        # Image Preview
        st.markdown('<div class="dr-preview-container">', unsafe_allow_html=True)
        st.image(selected_image, use_column_width=True, caption="Selected Image")
        st.markdown('</div>', unsafe_allow_html=True)

        # Analysis Button
        if st.button("🔍 Analyze Image", key="dr_analyze"):
            with st.spinner(""):
                st.markdown("""
                <div class="dr-loading">
                    <div class="dr-loading-text">Analyzing image with AI...</div>
                    <div class="dr-loading-bar"></div>
                </div>
                """, unsafe_allow_html=True)
                time.sleep(2)  # Simulate processing time

                # Results Section
                st.markdown("""
                <div class="dr-results-container">
                    <div class="dr-result-header">
                        <h2>Analysis Results</h2>
                        <div class="dr-confidence">
                            <div class="dr-confidence-label">Confidence Score</div>
                            <div class="dr-confidence-meter">
                                <div class="dr-confidence-fill" style="width: 95%;"></div>
                            </div>
                            <div class="dr-confidence-value">95%</div>
                        </div>
                    </div>
                    
                    <div class="dr-diagnosis">
                        <h3>Detected Disease</h3>
                        <div class="dr-disease-name">Early Blight</div>
                        <div class="dr-disease-info">
                            <h4>About this Disease</h4>
                            <p>Early blight is a common disease affecting tomato plants...</p>
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