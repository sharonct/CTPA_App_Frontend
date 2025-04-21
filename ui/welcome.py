import streamlit as st

def render_welcome_message():
    """Render welcome message when no scan is loaded"""
    st.info("👈 Please upload a CTPA scan file from the sidebar or select one from available scans")
    
    # Add helpful instructions for new users
    with st.expander("How to use this application", expanded=True):
        st.markdown("""
        ### Welcome to the Chest CTPA Viewer!
        
        This application helps radiologists and physicians visualize and analyze CTPA (CT Pulmonary Angiography) scans for the detection of pulmonary embolism. Here's how to get started:
        
        1. **Upload your scan**: Use the file uploader in the sidebar to select a NIfTI file (.nii or .nii.gz) or NPZ file (.npz)
        2. **Process the scan**: Click the "Process CTPA Scan" button to load your file
        3. **View the report**: Click "Generate Analysis Report" to get AI analysis
        4. **Explore the scan**: Use the view controls and slice navigator to examine the scan in different planes
        5. **Adjust windowing**: Use preset windows for optimal visualization of pulmonary structures
        6. **Ask questions**: Use the chat interface to ask specific questions about the scan
        
        Your uploaded scans will be available for future sessions.
        """)