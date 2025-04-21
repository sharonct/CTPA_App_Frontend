import os
import streamlit as st
from datetime import datetime
from config import DATA_DIR
from CTPA_App_Frontend.utils.notification import add_notification

def is_valid_file_type(filename):
    """
    Check if the file is a valid NIfTI file
    
    Parameters:
    -----------
    filename : str
        The name of the file to check
        
    Returns:
    --------
    bool
        True if the file is a valid NIfTI file, False otherwise
    """
    return filename.lower().endswith(('.nii', '.nii.gz'))

def save_uploaded_scan(uploaded_file):
    """
    Save an uploaded scan file to disk
    
    Parameters:
    -----------
    uploaded_file : UploadedFile
        The file uploaded by the user
        
    Returns:
    --------
    str or None
        The path to the saved file, or None if saving failed
    """
    # Create a safe filename
    original_filename = uploaded_file.name
    safe_filename = ''.join(c if c.isalnum() or c in ['.', '-', '_'] else '_' for c in original_filename)
    
    file_path = os.path.join(DATA_DIR, safe_filename)
    
    try:
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        scan_info = {
            "filename": original_filename,
            "safe_filename": safe_filename,
            "upload_time": timestamp,
            "path": file_path
        }
        
        if original_filename not in [scan["filename"] for scan in st.session_state.uploaded_scans]:
            st.session_state.uploaded_scans.append(scan_info)
            st.session_state.reports[original_filename] = ""
        
        return file_path
    except Exception as e:
        add_notification(f"Error saving file: {str(e)}", "error")
        return None