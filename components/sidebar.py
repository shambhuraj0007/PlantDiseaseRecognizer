import streamlit as st
import streamlit.components.v1 as components

def initialize_sidebar():
    # Add custom JavaScript for sidebar toggle
    st.markdown("""
        <script>
        document.addEventListener('DOMContentLoaded', function() {
            const sidebar = document.querySelector('.css-1d391kg');
            const toggleButton = document.createElement('button');
            toggleButton.innerHTML = '☰';
            toggleButton.className = 'sidebar-toggle';
            document.body.appendChild(toggleButton);

            let sidebarVisible = true;
            toggleButton.addEventListener('click', () => {
                sidebarVisible = !sidebarVisible;
                if (!sidebarVisible) {
                    sidebar.classList.add('sidebar-hidden');
                    toggleButton.innerHTML = '☰';
                } else {
                    sidebar.classList.remove('sidebar-hidden');
                    toggleButton.innerHTML = '×';
                }
            });
        });
        </script>
        <style>
        .sidebar-toggle {
            position: fixed;
            top: 1rem;
            left: 1rem;
            z-index: 1000;
            background: rgba(255, 255, 255, 0.1);
            border: none;
            padding: 0.5rem;
            font-size: 1.5rem;
            border-radius: 5px;
            cursor: pointer;
            backdrop-filter: blur(5px);
            transition: all 0.3s ease;
        }
        .sidebar-toggle:hover {
            background: rgba(255, 255, 255, 0.2);
            transform: scale(1.1);
        }
        </style>
    """, unsafe_allow_html=True)

    # Create sidebar navigation
    with st.sidebar:
        st.markdown('<div class="sidebar-title">Plant Disease Detection</div>', unsafe_allow_html=True)
        
        # Navigation links with icons
        nav_items = {
            "Home": "🏠",
            "Disease Recognition": "🔍",
            "About": "ℹ️",
            "Feedback & Support": "📝"
        }

        for page, icon in nav_items.items():
            active_class = "active" if st.session_state.get("page") == page else ""
            st.markdown(f"""
                <a href="?page={page}" class="nav-link {active_class}">
                    <span class="nav-icon">{icon}</span>
                    {page}
                </a>
            """, unsafe_allow_html=True)

    st.markdown("""
        <script>
        document.addEventListener('DOMContentLoaded', function() {
            // Get current page from URL
            const urlParams = new URLSearchParams(window.location.search);
            const currentPage = urlParams.get('page') || 'Home';
            
            // Set active state for buttons
            document.querySelectorAll('.stButton > button').forEach(button => {
                if (button.innerText.includes(currentPage)) {
                    button.setAttribute('data-active', 'true');
                }
            });
            
            // Add hover animation
            document.querySelectorAll('.stButton > button').forEach(button => {
                button.addEventListener('mouseover', function() {
                    this.style.transform = 'translateX(5px)';
                });
                
                button.addEventListener('mouseout', function() {
                    this.style.transform = 'translateX(0)';
                });
            });
        });
        </script>
    """, unsafe_allow_html=True) 