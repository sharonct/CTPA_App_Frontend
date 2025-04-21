import streamlit as st
from datetime import datetime

def add_notification(message, type="info"):
    """Add a notification to the session state"""
    st.session_state.notifications.append({
        "message": message,
        "type": type,
        "timestamp": datetime.now()
    })

def display_notifications():
    """Display active notifications"""
    for notification in st.session_state.notifications[:3]:
        msg_type = notification["type"]
        if msg_type == "error":
            st.error(notification["message"])
        elif msg_type == "success":
            st.success(notification["message"])
        else:
            st.info(notification["message"])
    
    # Clear notifications
    st.session_state.notifications = []