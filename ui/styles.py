import streamlit as st

def apply_styles():
    """Apply CSS styles to the Streamlit application"""
    st.markdown("""
    <style>
        /* Main container spacing */
        .main .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
            max-width: 1200px;
        }
        
        /* Report styling */
        .report-container {
            background-color: white;
            border-radius: 0.75rem;
            padding: 1.75rem;
            margin-bottom: 2rem;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
            border-left: 4px solid #e63946;
        }
        
        /* Image viewer styling */
        .viewer-container {
            background-color: white;
            border-radius: 0.75rem;
            padding: 1.5rem;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        }
        
        /* Button styling */
        .stButton>button {
            border-radius: 30px;
            height: 2.5rem;
            font-weight: 500;
            transition: all 0.3s ease;
        }
        
        .view-btn {
            background-color: #f8f9fa;
            border: 1px solid #dee2e6;
            width: 100%;
        }
        
        .view-btn:hover {
            background-color: #e9ecef;
            border-color: #adb5bd;
        }
        
        .active-view {
            background-color: #e63946 !important;
            color: white !important;
        }
        
        /* Status messages */
        .success-msg {
            padding: 1rem;
            border-radius: 0.5rem;
            background-color: #d4edda;
            color: #155724;
            margin-bottom: 1rem;
        }
        
        .error-msg {
            padding: 1rem;
            border-radius: 0.5rem;
            background-color: #f8d7da;
            color: #721c24;
            margin-bottom: 1rem;
        }
        
        /* Headers */
        h1, h2, h3 {
            font-weight: 400;
            color: #333;
        }
        
        /* Sidebar styling */
        .css-1d391kg {
            padding-top: 2rem;
            background: linear-gradient(to bottom, #1a3a8f, #0d326e);
        }
        
        .scan-history-btn {
            text-align: left;
            margin-bottom: 0.5rem;
            border-radius: 0.5rem;
            transition: background-color 0.2s;
        }
        
        .scan-history-btn:hover {
            background-color: #f8f9fa;
        }
        
        /* Slider styling */
        .stSlider > div {
            padding-top: 0.5rem;
            padding-bottom: 2rem;
        }
        
        /* PE findings highlight */
        .pe-finding {
            background-color: #fae2e3;
            border-left: 3px solid #e63946;
            padding: 0.75rem;
            margin: 0.5rem 0;
            border-radius: 0 0.5rem 0.5rem 0;
            font-weight: 500;
        }
        
        /* Window controls */
        .window-control {
            padding: 0.5rem;
            background-color: #f8f9fa;
            border-radius: 0.5rem;
            margin-bottom: 1rem;
        }
        
        /* Report sections */
        .report-section {
            margin-bottom: 1.5rem;
        }
        
        .report-section h4 {
            color: #1d3557;
            margin-bottom: 0.5rem;
            font-weight: 600;
        }
        
        .report-section ul {
            padding-left: 1.2rem;
            margin-top: 0.5rem;
        }
        
        .report-section li {
            margin-bottom: 0.4rem;
        }
    </style>
    """, unsafe_allow_html=True)