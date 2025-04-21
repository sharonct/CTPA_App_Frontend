import streamlit as st

def initialize_session_state():
    """Initialize session state variables"""
    if 'uploaded_scans' not in st.session_state:
        st.session_state.uploaded_scans = []
    
    if 'current_scan' not in st.session_state:
        st.session_state.current_scan = None
    
    if 'reports' not in st.session_state:
        st.session_state.reports = {}
    
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = {}
    
    if 'scan_data' not in st.session_state:
        st.session_state.scan_data = {}
    
    if 'current_view' not in st.session_state:
        st.session_state.current_view = 'axial'
    
    if 'window_width' not in st.session_state:
        st.session_state.window_width = 1500  # Default pulmonary window
    
    if 'window_center' not in st.session_state:
        st.session_state.window_center = -600  # Default pulmonary window

    if 'axial_slice' not in st.session_state:
        st.session_state.axial_slice = 0
    
    if 'sagittal_slice' not in st.session_state:
        st.session_state.sagittal_slice = 0
    
    if 'coronal_slice' not in st.session_state:
        st.session_state.coronal_slice = 0
    
    if 'notifications' not in st.session_state:
        st.session_state.notifications = []