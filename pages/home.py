import streamlit as st
import streamlit.components.v1 as components

def load_home_page():
    # Hero Section
    st.markdown("""
    <div class="page-transition">
        <div class="glass-card hero-section">
            <div class="hero-overlay"></div>
            <div class="hero-content">
                <div class="welcome-text">Welcome to</div>
                <h1 class="main-title">Plant Disease Detection</h1>
                <div class="subtitle">Your AI-Powered Plant Healthcare Assistant</div>
                <p class="description">
                    Detect plant diseases instantly with our advanced AI technology. 
                    Protect your crops and improve yields with accurate diagnostics.
                </p>
                <div class="cta-container">
                    <button class="primary-button" onclick="window.location.href='?page=Disease+Recognition'">
                        <span class="button-icon">🔍</span>
                        Start Detection
                    </button>
                    <button class="secondary-button" onclick="window.location.href='?page=About'">
                        <span class="button-icon">ℹ️</span>
                        Learn More
                    </button>
                </div>
            </div>
            <div class="hero-cards">
                <div class="feature-highlight">
                    <div class="highlight-card">
                        <span class="highlight-icon">🎯</span>
                        <div class="highlight-text">95% Accuracy</div>
                    </div>
                    <div class="highlight-card">
                        <span class="highlight-icon">⚡</span>
                        <div class="highlight-text">Instant Results</div>
                    </div>
                    <div class="highlight-card">
                        <span class="highlight-icon">🌿</span>
                        <div class="highlight-text">38+ Diseases</div>
                    </div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Quick Actions Section
    st.markdown("""
        <div class="glass-card feature-section">
            <div class="quick-actions">
                <div class="action-title">Quick Actions</div>
                <div class="action-cards">
                    <div class="action-card" onclick="window.location.href='?page=Disease+Recognition'">
                        <div class="action-icon">📸</div>
                        <div class="action-text">Upload Photo</div>
                        <div class="action-description">Scan your plant for diseases</div>
                    </div>
                    <div class="action-card" onclick="window.location.href='?page=Disease+Recognition'">
                        <div class="action-icon">📱</div>
                        <div class="action-text">Use Camera</div>
                        <div class="action-description">Take a photo directly</div>
                    </div>
                    <div class="action-card" onclick="window.location.href='?page=About'">
                        <div class="action-icon">📖</div>
                        <div class="action-text">View Guide</div>
                        <div class="action-description">Learn how to use</div>
                    </div>
                </div>
            </div>
    """, unsafe_allow_html=True)

    # How It Works Section
    st.markdown('<div class="section-title">How It Works</div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="step-card">
            <div class="step-icon">📸</div>
            <h3>Upload Image</h3>
            <p>Take or upload a photo of your plant's affected area</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="step-card">
            <div class="step-icon">🔍</div>
            <h3>AI Analysis</h3>
            <p>Our AI model analyzes the image in real-time</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="step-card">
            <div class="step-icon">💡</div>
            <h3>Get Results</h3>
            <p>Receive instant diagnosis and treatment recommendations</p>
        </div>
        """, unsafe_allow_html=True)

    # Key Features Section
    st.markdown('<div class="section-title">Key Features</div>', unsafe_allow_html=True)
    features_col1, features_col2 = st.columns(2)
    
    with features_col1:
        st.markdown("""
        <div class="feature-card">
            <h3>🎯 High Accuracy</h3>
            <p>95% accurate disease detection powered by advanced AI</p>
        </div>
        <div class="feature-card">
            <h3>⚡ Real-time Analysis</h3>
            <p>Get instant results and recommendations</p>
        </div>
        """, unsafe_allow_html=True)
    
    with features_col2:
        st.markdown("""
        <div class="feature-card">
            <h3>📱 Easy to Use</h3>
            <p>Simple interface for farmers and agricultural experts</p>
        </div>
        <div class="feature-card">
            <h3>🌐 Comprehensive Database</h3>
            <p>Covers 38+ different plant diseases</p>
        </div>
        """, unsafe_allow_html=True)

    # Statistics Section
    st.markdown('<div class="section-title">Impact Statistics</div>', unsafe_allow_html=True)
    stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
    
    with stat_col1:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-number counter">50K+</div>
            <div class="stat-label">Users</div>
        </div>
        """, unsafe_allow_html=True)
    
    with stat_col2:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-number counter">100K+</div>
            <div class="stat-label">Scans</div>
        </div>
        """, unsafe_allow_html=True)
    
    with stat_col3:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-number counter">38+</div>
            <div class="stat-label">Diseases</div>
        </div>
        """, unsafe_allow_html=True)
    
    with stat_col4:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-number counter">95%</div>
            <div class="stat-label">Accuracy</div>
        </div>
        """, unsafe_allow_html=True)

    # Close the remaining divs
    st.markdown("""
        </div>
    </div>
    """, unsafe_allow_html=True)
