import streamlit as st
import os

# Application constants
APP_TITLE = "Chest CTPA Viewer"
APP_ICON = "🫁"
APP_LAYOUT = "wide"
INITIAL_SIDEBAR_STATE = "expanded"

# Default window settings
DEFAULT_WINDOW_WIDTH = 400  # Default pulmonary window
DEFAULT_WINDOW_CENTER = -600  # Default pulmonary window

# Data directory
DATA_DIR = "data/ctpa_scan_data"

def set_page_config():
    """Set Streamlit page configuration"""
    st.set_page_config(
        page_title=APP_TITLE,
        page_icon=APP_ICON,
        layout=APP_LAYOUT,
        initial_sidebar_state=INITIAL_SIDEBAR_STATE
    )

# Create data directory if it doesn't exist
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR, exist_ok=True)