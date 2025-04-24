import streamlit as st
import time

def add_notification(message, type="info"):
    """Add a notification to the queue"""
    if 'notifications' not in st.session_state:
        st.session_state.notifications = []
    
    # Add notification with timestamp
    st.session_state.notifications.append({
        "message": message,
        "type": type,
        "time": time.time()
    })

def check_notifications():
    """Check and display any pending notifications"""
    if 'notifications' not in st.session_state:
        return
    
    # Display each notification
    for notification in st.session_state.notifications:
        if notification["type"] == "error":
            st.error(notification["message"])
        elif notification["type"] == "warning":
            st.warning(notification["message"])
        elif notification["type"] == "success":
            st.success(notification["message"])
        else:
            st.info(notification["message"])
    
    # Clear notifications
    st.session_state.notifications = []