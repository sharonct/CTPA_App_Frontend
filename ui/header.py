import streamlit as st

def render_header():
    """Render the page header"""
    st.markdown("""
    <div style="background: linear-gradient(to right, #ff4b4b, #ff6b6b); 
                padding: 1rem 1rem; 
                border-radius: 12px; 
                margin-bottom: 15px; 
                text-align: center; 
                box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);">
        <h1 style="color: white; margin: 0; font-size: 2.2rem; font-weight: 600;">
            🫁 Chest CTPA Report Generator
        </h1>
    </div>
    """, unsafe_allow_html=True)