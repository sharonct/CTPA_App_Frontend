import streamlit as st
from api.client import analyze_scan
from utils.notification import add_notification

def render_report_section(scan_id):
    """Render the report section"""
    # Report section heading
    st.markdown("""
    <h3 style="color: black; margin: 0;">🩺 PE Analysis</h3>
    """, unsafe_allow_html=True)
    
    # Check if report exists in session state
    if scan_id in st.session_state.reports and st.session_state.reports[scan_id]:
        # Display report
        st.components.v1.html(st.session_state.reports[scan_id], height=400, scrolling=True)
        
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
    else:
        # Generate report button
        if st.button("🔍 Generate Analysis Report", type="primary", use_container_width=True):
            with st.spinner("Analyzing scan and generating report..."):
                # Call the API to analyze the scan with a specific report question
                analysis = analyze_scan(scan_id, ["Generate a comprehensive CTPA report for this scan."])
                
                if analysis and "report_html" in analysis and analysis["report_html"]:
                    # Save report to session state
                    st.session_state.reports[scan_id] = analysis["report_html"]
                    add_notification("Report generated successfully!", "success")
                    st.rerun()
                else:
                    add_notification("Failed to generate report", "error")
        
        st.info("Click the button above to generate a comprehensive PE analysis report.")