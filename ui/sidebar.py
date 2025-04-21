import streamlit as st
from api.client import get_api_health, upload_scan, get_scan_list
from utils.notification import add_notification

def render_scan_list():
    """Render the list of available scans"""
    st.header("📋 Available Scans")
    
    # Get scans from API
    scans = get_scan_list()
    
    if not scans:
        st.info("No CTPA scans available yet")
    else:
        for scan in scans:
            is_current = st.session_state.current_scan == scan["scan_id"]
            button_style = "primary" if is_current else "secondary"
            
            col1, col2 = st.columns([4, 1])
            with col1:
                if st.button(f"{scan['filename']}", 
                          key=f"scan_{scan['scan_id']}",
                          type=button_style,
                          use_container_width=True):
                    st.session_state.current_scan = scan["scan_id"]
                    st.rerun()
            
            # Show scan upload date
            st.caption(f"Uploaded: {scan['upload_time'][:10]}")
            
            # Add spacing
            st.markdown("<hr style='margin: 0.5rem 0; opacity: 0.2'>", unsafe_allow_html=True)

def render_sidebar():
    """Render the sidebar UI components"""
    with st.sidebar:
        st.title("Chest CTPA Viewer")
        st.caption("For Pulmonary Embolism Detection")
        
        st.markdown("---")
        
        # API connection status
        api_health = get_api_health()
        if api_health["status"] == "healthy":
            st.success("✅ Connected to AI backend")
            
            if api_health["model_loaded"]:
                st.success("✅ AI models loaded")
            else:
                st.warning("⚠️ AI models loading...")
        else:
            st.error("❌ API connection error")
        
        st.markdown("---")
        
        # Scan upload section
        st.header("📂 Upload CTPA Scan")
        uploaded_file = st.file_uploader("Choose a scan file", type=["nii", "nii.gz", "npz"], 
                                         help="Supported formats: NIfTI (.nii or .nii.gz) or NumPy (.npz)")
        
        if uploaded_file is not None:
            process_button = st.button("Process CTPA Scan", type="primary", use_container_width=True)
            if process_button:
                with st.spinner("Processing CTPA scan..."):
                    # Upload the scan to the API
                    scan_info = upload_scan(uploaded_file)
                    
                    if scan_info:
                        st.session_state.current_scan = scan_info["scan_id"]
                        add_notification(f"Successfully processed {uploaded_file.name}", "success")
                        st.rerun()
        
        st.markdown("---")
        
        # Scan list section
        render_scan_list()