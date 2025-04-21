import streamlit as st
from api.client import ask_question
from datetime import datetime

def render_chat_interface(scan_id):
    """Render a chat interface for asking questions about the scan"""
    # Initialize chat history for this scan if not already present
    if scan_id not in st.session_state.chat_history:
        st.session_state.chat_history[scan_id] = [
            {"role": "assistant", "content": "I'm your radiology assistant. How can I help you with this scan?", "time": datetime.now().strftime("%H:%M")}
        ]
    
    # Chat section title
    st.markdown("""
    <h3 style="margin-top: 30px; margin-bottom: 15px; color: #333; padding-bottom: 10px; border-bottom: 1px solid #ddd;">
        💬 Chat with AI Assistant
    </h3>
    """, unsafe_allow_html=True)
    
    # Display all messages
    for message in st.session_state.chat_history[scan_id]:
        if message["role"] == "assistant":
            st.markdown(f"""
            <div style="background-color: #f0f0f0; border-radius: 10px; padding: 10px; margin: 5px 0;">
                <p style="margin: 0;"><strong>AI Assistant:</strong> {message["content"]}</p>
                <p style="text-align: right; font-size: 12px; color: #777; margin: 5px 0 0 0;">{message.get("time", "")}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="background-color: #e6f7ff; border-radius: 10px; padding: 10px; margin: 5px 0;">
                <p style="margin: 0;"><strong>You:</strong> {message["content"]}</p>
                <p style="text-align: right; font-size: 12px; color: #777; margin: 5px 0 0 0;">{message.get("time", "")}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Input field
    with st.form(key=f"chat_form_{scan_id}"):
        user_question = st.text_input("Ask a question about this scan...")
        submit_button = st.form_submit_button("Send Message", type="primary")
        
        if submit_button and user_question:
            # Add user message to chat history
            st.session_state.chat_history[scan_id].append(
                {"role": "user", "content": user_question, "time": datetime.now().strftime("%H:%M")}
            )
            
            # Ask the API
            response = ask_question(scan_id, user_question)
            
            if response:
                # Add AI response to chat history
                st.session_state.chat_history[scan_id].append(
                    {"role": "assistant", "content": response["answer"], "time": datetime.now().strftime("%H:%M")}
                )
            else:
                # Add error message to chat history
                st.session_state.chat_history[scan_id].append(
                    {"role": "assistant", "content": "Sorry, I encountered an error processing your question.", "time": datetime.now().strftime("%H:%M")}
                )
            
            st.rerun()