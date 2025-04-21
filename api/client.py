import requests
import streamlit as st
import os

# API configuration
API_URL = os.environ.get("API_URL", "http://localhost:8000")

def get_api_health():
    """Check API health"""
    try:
        response = requests.get(f"{API_URL}/health")
        return response.json()
    except Exception as e:
        st.error(f"Error connecting to API: {str(e)}")
        return {"status": "error", "model_loaded": False}

def upload_scan(file):
    """Upload a scan to the API"""
    try:
        files = {"file": file}
        response = requests.post(f"{API_URL}/upload", files=files)
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error uploading scan: {response.text}")
            return None
    except Exception as e:
        st.error(f"Error uploading scan: {str(e)}")
        return None

def get_scan_list():
    """Get list of available scans"""
    try:
        response = requests.get(f"{API_URL}/scans")
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error getting scan list: {response.text}")
            return []
    except Exception as e:
        st.error(f"Error getting scan list: {str(e)}")
        return []

def get_scan_metadata(scan_id):
    """Get metadata for a specific scan"""
    try:
        response = requests.get(f"{API_URL}/scans/{scan_id}")
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error getting scan metadata: {response.text}")
            return None
    except Exception as e:
        st.error(f"Error getting scan metadata: {str(e)}")
        return None

def get_scan_slice(scan_id, view, slice_idx, window_center, window_width):
    """Get a specific slice from a scan"""
    try:
        params = {
            "view": view,
            "slice_idx": slice_idx,
            "window_center": window_center,
            "window_width": window_width
        }
        
        response = requests.get(f"{API_URL}/slice/{scan_id}", params=params)
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error getting scan slice: {response.text}")
            return None
    except Exception as e:
        st.error(f"Error getting scan slice: {str(e)}")
        return None

def ask_question(scan_id, question):
    """Ask a question about a scan"""
    try:
        data = {"text": question}
        response = requests.post(f"{API_URL}/ask/{scan_id}", json=data)
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error asking question: {response.text}")
            return None
    except Exception as e:
        st.error(f"Error asking question: {str(e)}")
        return None

def analyze_scan(scan_id, questions):
    """Analyze a scan with a list of questions"""
    try:
        data = {
            "scan_id": scan_id,
            "questions": [{"text": q} for q in questions]
        }
        
        response = requests.post(f"{API_URL}/analyze", json=data)
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error analyzing scan: {response.text}")
            return None
    except Exception as e:
        st.error(f"Error analyzing scan: {str(e)}")
        return None