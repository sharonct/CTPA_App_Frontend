import streamlit as st
from datetime import datetime
from CTPA_App_Frontend.utils.notification import display_notifications, add_notification
from core.scan_viewer import display_scan_views

def render_main_content():
    """Render the main content area"""
    # Display any active notifications
    display_notifications()
    
    # Page title with user-friendly intro
    render_header()
    
    # Info message when no scan is loaded
    if not st.session_state.current_scan:
        render_welcome_message()
        return
    
    # If a scan is loaded, display the content in a two-column layout
    current_filename = st.session_state.current_scan
    
    # Create two columns for the report and visualization
    report_col, viewer_col = st.columns([1, 1])
    
    with report_col:
        render_report_section(current_filename)

    with viewer_col:
        render_viewer_section(current_filename)

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

def render_welcome_message():
    """Render welcome message when no scan is loaded"""
    st.info("👈 Please upload a CTPA scan file from the sidebar or select one from patient history")
    
    # Add helpful instructions for new users
    with st.expander("How to use this application", expanded=True):
        st.markdown("""
        ### Welcome to the Chest CTPA Viewer!
        
        This application helps radiologists and physicians visualize and analyze CTPA (CT Pulmonary Angiography) scans for the detection of pulmonary embolism. Here's how to get started:
        
        1. **Upload your scan**: Use the file uploader in the sidebar to select a NIfTI file (.nii or .nii.gz)
        2. **Process the scan**: Click the "Process CTPA Scan" button to load your file
        3. **View the report**: A preliminary PE analysis report will be automatically generated
        4. **Explore the scan**: Use the view controls and slice navigator to examine the scan in different planes
        5. **Adjust windowing**: Use preset windows for optimal visualization of pulmonary structures
        
        Your uploaded scans will be saved in patient history for easy access in future sessions.
        """)

def render_report_section(current_filename):
    """
    Render the report section
    
    Parameters:
    -----------
    current_filename : str
        The filename of the current scan
    """
    # Report section heading
    st.markdown(f"""
    <div style="padding: 8px 16px; border-radius: 8px; margin-bottom: 10px;">
        <h3 style="color: black; margin: 0;">🩺 PE Analysis: {current_filename}</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Display the report
    if st.session_state.reports[current_filename]:
        # Display report
        st.components.v1.html(st.session_state.reports[current_filename], height=400, scrolling=True)
        
        # Report action buttons
        cols = st.columns([1, 1, 1])
        with cols[0]:
            if st.button("📋 Copy Report", use_container_width=True):
                # Placeholder for copy functionality
                add_notification("Report copied to clipboard!", "success")
        with cols[1]:
            if st.button("📤 Export PDF", use_container_width=True):
                # Placeholder for export functionality
                add_notification("PDF export not implemented in this demo", "info")
        with cols[2]:
            if st.button("📝 Edit Report", use_container_width=True):
                # Placeholder for edit functionality
                add_notification("Report editing not implemented in this demo", "info")
        
        # Add chat interface - using the dedicated function
        render_chat_interface(current_filename)
    else:
        st.info("Analyzing scan for pulmonary embolism...")

def render_chat_interface(current_filename):
    """
    Render a chat interface for asking questions about the scan
    
    Parameters:
    -----------
    current_filename : str
        The filename of the current scan
    """
    # Initialize chat history for this scan if not already present
    if current_filename not in st.session_state.chat_history:
        st.session_state.chat_history[current_filename] = [
            {"role": "assistant", "content": "I'm your radiology assistant. How can I help you with this scan?", "time": datetime.now().strftime("%H:%M")}
        ]
    
    # Chat section title - OUTSIDE any containers to ensure visibility
    st.markdown("""
    <h3 style="margin-top: 30px; margin-bottom: 15px; color: #333; padding-bottom: 10px; border-bottom: 1px solid #ddd;">
        💬 Chat with AI Assistant
    </h3>
    """, unsafe_allow_html=True)
    
    # Create a container for the chat messages
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    # Display all messages
    for message in st.session_state.chat_history[current_filename]:
        if message["role"] == "assistant":
            st.markdown(f"""
            <div class="chat-message-ai">
                <p style="margin: 0;"><strong>AI Assistant:</strong> {message["content"]}</p>
                <p style="text-align: right; font-size: 12px; color: #777; margin: 5px 0 0 0;">{message.get("time", "")}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="chat-message-user">
                <p style="margin: 0;"><strong>You:</strong> {message["content"]}</p>
                <p style="text-align: right; font-size: 12px; color: #777; margin: 5px 0 0 0;">{message.get("time", "")}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Close the chat container
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Input field - Use a separate form container
    st.markdown('<div style="margin-top: 20px;">', unsafe_allow_html=True)
    
    # Create unique keys for the form elements
    form_key = f"chat_form_{current_filename}_{id(current_filename)}"
    input_key = f"chat_input_{current_filename}_{id(current_filename)}"
    
    # Add the form using Streamlit's form
    with st.form(key=form_key):
        # Message input field
        user_question = st.text_input(
            "Ask a question about this scan...",
            key=input_key
        )
        
        # Submit button that stands out visually
        submit_col1, submit_col2, submit_col3 = st.columns([1, 2, 1])
        with submit_col2:
            submit_button = st.form_submit_button(
                "Send Message",
                use_container_width=True,
                type="primary"
            )
        
        if submit_button and user_question:
            # Add user message to chat history
            st.session_state.chat_history[current_filename].append(
                {"role": "user", "content": user_question, "time": datetime.now().strftime("%H:%M")}
            )
            
            # Generate AI response
            pe_present = "pulmonary embolism" in st.session_state.reports.get(current_filename, "").lower()
            
            if "treatment" in user_question.lower():
                if pe_present:
                    ai_response = "Standard treatment for pulmonary embolism usually includes anticoagulation therapy. The specific medication and duration depends on patient factors and the severity of the PE. For this patient, I recommend following your institution's PE protocol."
                else:
                    ai_response = "No pulmonary embolism was detected in this scan, so no specific PE treatment is needed. However, you may want to consider the patient's symptoms and investigate other possible causes."
            elif "location" in user_question.lower() or "where" in user_question.lower():
                if pe_present:
                    ai_response = "The pulmonary embolism is located in the right lower lobe pulmonary artery as indicated in the report. This is a segmental branch, which is considered clinically significant."
                else:
                    ai_response = "No pulmonary embolism was detected in this scan. All major pulmonary arteries appear patent with normal contrast enhancement."
            elif "risk" in user_question.lower() or "prognosis" in user_question.lower():
                if pe_present:
                    ai_response = "This patient has a pulmonary embolism without evidence of right heart strain, which generally indicates a better prognosis. However, close monitoring is still recommended, and risk stratification should be performed according to your institution's guidelines."
                else:
                    ai_response = "No pulmonary embolism was detected, so the immediate risk from PE is not present. However, the patient's risk factors should still be addressed if they were initially suspected of having a PE."
            else:
                if pe_present:
                    ai_response = "Based on the scan, there is a filling defect in the right lower lobe pulmonary artery consistent with acute pulmonary embolism. There is no evidence of right heart strain, which is a positive prognostic indicator. Would you like more specific information about the location, severity, or recommended follow-up?"
                else:
                    ai_response = "The scan shows no evidence of pulmonary embolism. All pulmonary arteries appear to be filling normally with contrast. Is there a specific aspect of the scan you'd like me to elaborate on?"
            
            # Add AI response to chat history
            st.session_state.chat_history[current_filename].append(
                {"role": "assistant", "content": ai_response, "time": datetime.now().strftime("%H:%M")}
            )
            
            # Use st.rerun() to update the UI
            st.rerun()
    
    # Close the input container div
    st.markdown('</div>', unsafe_allow_html=True)

def render_viewer_section(current_filename):
    """
    Render the scan viewer section
    
    Parameters:
    -----------
    current_filename : str
        The filename of the current scan
    """
    # Scan visualization section heading
    st.markdown("""
    <div style="padding: 8px 16px; border-radius: 8px; margin-bottom: 10px;">
        <h3 style="color: black; margin: 0;">🩺 CTPA Visualization</h3>
    </div>
    """, unsafe_allow_html=True)
    
    if current_filename in st.session_state.scan_data:
        try:
            display_scan_views(st.session_state.scan_data[current_filename])
        except Exception as e:
            st.error(f"Error displaying scan: {str(e)}")
    else:
        st.warning("Scan data not available")