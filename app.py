import streamlit as st
from ui.sidebar import render_sidebar
from ui.report import render_report_section
from utils.notification import check_notifications
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

def main():
    # Set page config
    st.set_page_config(
        page_title="CT Pulmonary Angiography Viewer",
        page_icon="🫁",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize session state
    if 'current_scan' not in st.session_state:
        st.session_state.current_scan = None
    if 'reports' not in st.session_state:
        st.session_state.reports = {}
    if 'notifications' not in st.session_state:
        st.session_state.notifications = []
    
    # Render sidebar
    render_sidebar()
    
    # Main content area
    st.title("CT Pulmonary Angiography Viewer")
    
    # Display notifications
    check_notifications()
    
    # Check if a scan is selected
    if st.session_state.current_scan:
        # Render visualization section
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("### 🔍 CTPA Visualization")
            # Visualization component would go here
            st.info("Visualization component placeholder")
        
        with col2:
            # Pass the current scan_id to the report component
            render_report_section(st.session_state.current_scan)
    else:
        st.info("👈 Please select a scan from the sidebar or upload a new one.")
        
        # Show system info in expanded state
        with st.expander("System Information"):
            from api.client import get_api_health
            health = get_api_health()
            
            st.write("### API Status")
            if health["status"] == "healthy":
                st.success("✅ API server is running")
            else:
                st.error("❌ API server is not responding")
                
            st.write("### Model Status")
            if health.get("model_loaded", False):
                st.success("✅ AI models are loaded")
            else:
                st.warning("⚠️ AI models are not loaded")
            
            st.write("### Environment")
            st.code(f"API URL: {health.get('api_url', 'Unknown')}")
            st.code(f"Device: {health.get('device', 'Unknown')}")

if __name__ == "__main__":
    main()