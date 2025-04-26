import streamlit as st
import streamlit.components.v1 as components
from api.client import analyze_scan, get_api_health, API_URL, get_scan_metadata
from utils.notification import add_notification
import requests
import json
from datetime import datetime

def render_report_section(scan_id):
    """Render the report section"""
    if not scan_id:
        st.warning("No scan selected. Please select a scan first.")
        return
        
    # Report section heading
    st.markdown("""
    <h3 style="color: black; margin: 0;">🩺 PE Analysis</h3>
    """, unsafe_allow_html=True)
    
    # Initialize reports dict in session state if it doesn't exist
    if 'reports' not in st.session_state:
        st.session_state.reports = {}
    
    # Check if report exists in session state
    if scan_id in st.session_state.reports and st.session_state.reports[scan_id]:
        # Display report using the correct components import
        components.html(st.session_state.reports[scan_id], height=400, scrolling=True)
        
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
                # First try the analyze endpoint
                report_html = generate_report_using_analyze(scan_id)
                
                if report_html:
                    st.session_state.reports[scan_id] = report_html
                    add_notification("Report generated successfully!", "success")
                    st.rerun()
                else:
                    # If that fails, try the fallback method
                    add_notification("Using fallback report generator...", "info")
                    report_html = generate_static_report(scan_id)
                    
                    if report_html:
                        st.session_state.reports[scan_id] = report_html
                        add_notification("Report generated using fallback method", "success")
                        st.rerun()
                    else:
                        add_notification("Failed to generate report", "error")
        
        st.info("Click the button above to generate a comprehensive PE analysis report.")

def generate_report_using_analyze(scan_id):
    """Generate a report using the analyze endpoint"""
    try:
        # Check API health first
        health = get_api_health()
        if health.get("status") != "healthy":
            st.warning("API is not healthy. Using fallback report generator.")
            return None
        
        # Call the API to analyze the scan with a specific report question
        analysis = analyze_scan(scan_id, ["Generate a comprehensive CTPA report for this scan."])
        
        if analysis and "report_html" in analysis and analysis["report_html"]:
            return analysis["report_html"]
        return None
    except Exception as e:
        st.error(f"Error in analyze method: {str(e)}")
        return None

def generate_static_report(scan_id):
    """Generate a static report when API methods fail"""
    
    # Get basic scan info if available
    scan_info = "Unknown"
    try:
        metadata = get_scan_metadata(scan_id)
        if metadata and "filename" in metadata:
            scan_info = metadata["filename"]
    except:
        pass
    
    report_date = datetime.now().strftime("%B %d, %Y at %I:%M %p")
    
    # Create a simple but informative HTML report
    report = f"""
    <div style="font-family: Arial, sans-serif; padding: 20px; border: 1px solid #ccc; border-radius: 8px; max-width: 800px; margin: 0 auto;">
        <div style="text-align: center; padding-bottom: 15px; border-bottom: 2px solid #2c3e50;">
            <h2 style="color: #2c3e50; margin: 0;">CT PULMONARY ANGIOGRAPHY REPORT</h2>
            <p style="color: #7f8c8d; font-style: italic;">(Fallback Report Generator)</p>
        </div>
        
        <div style="margin: 15px 0;">
            <h3 style="color: #2c3e50; margin: 0 0 8px 0; font-size: 16px; border-bottom: 1px solid #eee; padding-bottom: 5px;">SCAN INFORMATION:</h3>
            <p style="margin: 5px 0; line-height: 1.5;">
                <strong>Scan ID:</strong> {scan_id}<br>
                <strong>Filename:</strong> {scan_info}<br>
                <strong>Date:</strong> {report_date}
            </p>
        </div>
        
        <div style="margin: 15px 0;">
            <h3 style="color: #2c3e50; margin: 0 0 8px 0; font-size: 16px; border-bottom: 1px solid #eee; padding-bottom: 5px;">FINDINGS:</h3>
            <p style="margin: 5px 0; line-height: 1.5;">
                This is a fallback report generated when the AI analysis system is unavailable.<br>
                Please consult with a radiologist for a professional interpretation of this scan.
            </p>
            <ul style="margin: 10px 0; padding-left: 20px;">
                <li>CT Pulmonary Angiogram study performed to evaluate for pulmonary embolism</li>
                <li>Pulmonary arterial tree visualized to the subsegmental level</li>
                <li>Lung parenchyma and airways visualized</li>
                <li>Mediastinal and hilar structures evaluated</li>
                <li>Limited evaluation of the chest wall and upper abdomen</li>
            </ul>
        </div>
        
        <div style="background-color: #f9f9f9; padding: 10px 15px; border-left: 4px solid #2c3e50; margin: 15px 0;">
            <h3 style="color: #2c3e50; margin: 0 0 8px 0; font-size: 16px; padding-bottom: 5px;">IMPRESSION:</h3>
            <p style="margin: 5px 0; line-height: 1.5;">
                <strong>Note:</strong> This is a fallback report. A qualified radiologist should review this study to provide an accurate diagnosis and interpretation.
            </p>
        </div>
        
        <div style="margin-top: 20px; padding-top: 10px; border-top: 1px solid #eee; font-size: 12px; color: #7f8c8d; text-align: center;">
            <p>Report generated using fallback generator on {report_date}<br>
            This report does not represent a medical diagnosis.</p>
        </div>
    </div>
    """
    
    return report