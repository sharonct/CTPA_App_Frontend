import streamlit as st
from utils.session import initialize_session_state
from ui.header import render_header
from ui.sidebar import render_sidebar
from ui.welcome import render_welcome_message
from ui.viewer import render_viewer_section
from ui.report import render_report_section
from ui.chat import render_chat_interface
from ui.styles import apply_styles
from api.client import get_scan_metadata
from utils.notification import display_notifications

def render_main_content():
    """Render the main content area"""
    # Display any active notifications
    display_notifications()
    
    # Page title with user-friendly intro
    render_header()
    
    # Info message when no scan is loaded
    if not st.session_state.current_scan:
        render_welcome_message()
        return
    
    # Get current scan metadata
    scan_id = st.session_state.current_scan
    metadata = get_scan_metadata(scan_id)
    
    if not metadata:
        st.error(f"Error loading scan metadata")
        return
    
    # Display scan filename
    st.markdown(f"### Analyzing: {metadata['filename']}")
    
    # Create two columns for the report and visualization
    report_col, viewer_col = st.columns([1, 1])
    
    with report_col:
        render_report_section(scan_id)
        render_chat_interface(scan_id)

    with viewer_col:
        render_viewer_section(scan_id, metadata)

def main():
    # Set page config
    st.set_page_config(
        page_title="Chest CTPA Viewer",
        page_icon="🫁",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Apply CSS styles
    apply_styles()
    
    # Initialize session state
    initialize_session_state()
    
    # Render sidebar
    render_sidebar()
    
    # Render main content
    render_main_content()

if __name__ == "__main__":
    main()