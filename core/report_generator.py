import time
from datetime import datetime

def generate_ctpa_report(scan_data):
    """
    Generate a CTPA report
    
    Parameters:
    -----------
    scan_data : numpy.ndarray
        The scan data for analysis
        
    Returns:
    --------
    str
        HTML string containing the formatted report
    """
    try:
        # Simulate processing time
        time.sleep(1)
        
        # In a real application, this would analyze the scan data
        # and generate a real report based on medical findings
        
        report_date = datetime.now().strftime("%B %d, %Y at %I:%M %p")
        
        # For demonstration, always show a PE case (or toggle based on your needs)
        pe_present = True
        
        # Define CSS styling for the report
        css_style = """
        <style>
            .report-container {
                font-family: 'Arial', sans-serif;
                max-width: 800px;
                margin: 20px auto;
                padding: 25px;
                border: 1px solid #ccc;
                border-radius: 8px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                background-color: #fff;
            }
            
            .report-header {
                text-align: center;
                padding-bottom: 15px;
                border-bottom: 2px solid #2c3e50;
            }
            
            .report-title {
                color: #2c3e50;
                margin: 0;
                font-size: 22px;
                font-weight: 700;
            }
            
            .logo-container {
                text-align: center;
                margin-bottom: 15px;
            }
            
            .report-section {
                margin: 15px 0;
                padding-bottom: 10px;
            }
            
            .report-section h4 {
                color: #2c3e50;
                margin: 0 0 8px 0;
                font-size: 16px;
                font-weight: 600;
                border-bottom: 1px solid #eee;
                padding-bottom: 5px;
            }
            
            .report-section p, .report-section li {
                margin: 5px 0;
                line-height: 1.5;
                color: #333;
                font-size: 14px;
            }
            
            .report-section ul {
                padding-left: 20px;
            }
            
            .pe-finding {
                color: #c0392b;
                font-weight: 600;
            }
            
            .normal-finding {
                color: #27ae60;
                font-weight: 600;
            }
            
            .report-footer {
                margin-top: 20px;
                padding-top: 10px;
                border-top: 1px solid #eee;
                font-size: 12px;
                color: #7f8c8d;
                text-align: center;
            }
            
            .impression-section {
                background-color: #f9f9f9;
                padding: 10px 15px;
                border-left: 4px solid #2c3e50;
                margin: 15px 0;
            }
            
            .recommendation-section {
                background-color: #f9f9f9;
                padding: 10px 15px;
                border-left: 4px solid #3498db;
                margin: 15px 0;
            }
            
            @media print {
                .report-container {
                    box-shadow: none;
                    border: none;
                }
            }
        </style>
        """
        
        if pe_present:
            findings = """
            <div class="report-section">
                <h4>FINDINGS:</h4>
                <ul>
                    <li><div class="pe-finding">Filling defect in the right lower lobe pulmonary artery consistent with acute pulmonary embolism</div></li>
                    <li>No evidence of right heart strain</li>
                    <li>Lung parenchyma shows no consolidation or ground glass opacity</li>
                    <li>No pleural effusion</li>
                    <li>Mediastinal and hilar lymph nodes within normal limits</li>
                </ul>
            </div>
            
            <div class="report-section impression-section">
                <h4>IMPRESSION:</h4>
                <p><strong>Acute pulmonary embolism</strong> in the right lower lobe pulmonary artery without evidence of right heart strain.</p>
            </div>
            
            <div class="report-section recommendation-section">
                <h4>RECOMMENDATION:</h4>
                <p>Anticoagulation therapy as per institutional protocol. Clinical correlation recommended.</p>
            </div>
            """
        else:
            findings = """
            <div class="report-section">
                <h4>FINDINGS:</h4>
                <ul>
                    <li><div class="normal-finding">No filling defects in the main, lobar, segmental, or subsegmental pulmonary arteries</div></li>
                    <li>Normal caliber of the main pulmonary artery</li>
                    <li>Lung parenchyma shows no consolidation or ground glass opacity</li>
                    <li>No pleural effusion</li>
                    <li>Mediastinal and hilar lymph nodes within normal limits</li>
                </ul>
            </div>
            
            <div class="report-section impression-section">
                <h4>IMPRESSION:</h4>
                <p><strong class="normal-finding">No evidence of pulmonary embolism.</strong></p>
            </div>
            
            <div class="report-section recommendation-section">
                <h4>RECOMMENDATION:</h4>
                <p>No further imaging required for suspected pulmonary embolism. Clinical correlation recommended.</p>
            </div>
            """
        
        return f"""
        {css_style}
        <div class="report-container">
            <div class="report-header">
                <div class="logo-container">
                    <!-- Hospital logo could go here -->
                    <!-- <img src="hospital_logo.png" alt="Hospital Logo" width="180"> -->
                </div>
                <h3 class="report-title">CT PULMONARY ANGIOGRAPHY REPORT</h3>
            </div>
            
            <div class="report-section">
                <h4>PATIENT INFORMATION:</h4>
                <p>
                    <strong>Patient ID:</strong> {getattr(scan_data, 'patient_id', 'Anonymous')} <br>
                    <strong>Name:</strong> {getattr(scan_data, 'patient_name', 'Anonymous')} <br>
                    <strong>DOB:</strong> {getattr(scan_data, 'patient_dob', '12/12/1990')} <br>
                    <strong>Gender:</strong> {getattr(scan_data, 'patient_gender', 'Anonymous')} <br>
                    <strong>Referring Physician:</strong> {getattr(scan_data, 'referring_physician', 'Dr Jane Doe')}
                </p>
            </div>
            
            <div class="report-section">
                <h4>EXAM:</h4>
                <p>CT Pulmonary Angiography (CTPA)</p>
            </div>
            
            <div class="report-section">
                <h4>DATE:</h4>
                <p>{report_date}</p>
            </div>
            
            <div class="report-section">
                <h4>TECHNIQUE:</h4>
                <p>Contrast-enhanced CT of the chest with pulmonary arterial phase imaging.<br>
                IV contrast: 70 ml of non-ionic contrast material.<br>
                Slice thickness: 1.0 mm</p>
            </div>
            
            {findings}
            
            <div class="report-footer">
                <p>Report generated by Dr. {getattr(scan_data, 'radiologist', 'Dr Jane Doe')}<br>
                This report was electronically signed on {report_date}</p>
            </div>
        </div>
        """
    except Exception as e:
        return f"""
        <div style="color: red; padding: 20px; border: 1px solid red; border-radius: 5px; margin: 20px;">
            <h3>Error Generating Report</h3>
            <p>{str(e)}</p>
        </div>
        """