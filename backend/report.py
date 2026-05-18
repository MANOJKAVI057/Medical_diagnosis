from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.enums import TA_CENTER
import uuid
import os
from datetime import datetime


# -------------------- RECOMMENDATION LOGIC --------------------
def get_recommendation(diagnosis):
    recommendations = {
        "Hypoxia": "Oxygen levels are low. Immediate medical evaluation is recommended. Supplemental oxygen therapy may be required.",
        
        "Hypertension": "Blood pressure is elevated. Reduce salt intake, manage stress, exercise regularly, and consult a cardiologist.",
        
        "Hypotension": "Blood pressure is low. Increase fluid intake and consult a doctor if dizziness or weakness persists.",
        
        "Tachycardia": "Heart rate is elevated. Avoid stimulants like caffeine and seek medical evaluation if symptoms continue.",
        
        "Bradycardia": "Heart rate is below normal. Medical assessment is advised, especially if fatigue or fainting occurs.",
        
        "Fever": "Elevated body temperature detected. Stay hydrated, rest, and seek medical care if temperature remains high.",
        
        "Pneumonia": "Possible lung infection detected. Immediate medical consultation and possible antibiotic treatment required.",
        
        "Heart Disease": "Cardiac risk identified. Urgent cardiology consultation and diagnostic testing recommended.",
        
        "Sepsis": "Critical condition suspected. Immediate emergency medical attention is required.",
        
        "Normal": "All vital parameters are within normal range. Maintain a healthy lifestyle and regular check-ups."
    }

    return recommendations.get(
        diagnosis,
        "Consult a healthcare professional for further evaluation."
    )


# -------------------- MAIN REPORT FUNCTION --------------------
def generate_report(data):

    if not os.path.exists("reports"):
        os.makedirs("reports")

    filename = f"reports/{uuid.uuid4()}.pdf"
    doc = SimpleDocTemplate(filename, pagesize=A4)
    elements = []

    styles = getSampleStyleSheet()

    # Extract vitals dictionary
    vitals = data.get("vitals", {})

    # -------------------- TITLE --------------------
    title_style = styles["Heading1"]
    title_style.alignment = TA_CENTER
    elements.append(Paragraph("MEDICAL DIAGNOSIS REPORT", title_style))
    elements.append(Spacer(1, 20))

    # -------------------- DATE & TIME --------------------
    current_datetime = datetime.now().strftime("%d-%m-%Y %I:%M %p")
    elements.append(Paragraph(f"<b>Date & Time:</b> {current_datetime}", styles["Normal"]))
    elements.append(Spacer(1, 20))

    # -------------------- PATIENT DETAILS --------------------
    patient_data = [
        ["NAME:", data.get("patient_name", "-")],
        ["AGE:", vitals.get("age", "-")]  # Age from vitals
    ]

    patient_table = Table(patient_data, colWidths=[120, 300])
    patient_table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))

    elements.append(patient_table)
    elements.append(Spacer(1, 25))

    # -------------------- VITALS SECTION --------------------
    elements.append(Paragraph("<b>PATIENT INFORMATION</b>", styles["Heading2"]))
    elements.append(Spacer(1, 10))

    vitals_data = [
        ["HEART RATE", vitals.get("heart_rate", "-")],
        ["SYSTOLIC BP", vitals.get("systolic_bp", "-")],
        ["DIASTOLIC BP", vitals.get("diastolic_bp", "-")],
        ["SPO2", vitals.get("spo2", "-")],
        ["TEMPERATURE", vitals.get("temperature", "-")],
    ]

    vitals_table = Table(vitals_data, colWidths=[200, 200])
    vitals_table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))

    elements.append(vitals_table)
    elements.append(Spacer(1, 25))

    # -------------------- DIAGNOSIS SECTION --------------------
    elements.append(Paragraph("<b>DIAGNOSIS RESULT</b>", styles["Heading2"]))
    elements.append(Spacer(1, 10))

    diagnosis = data.get("diagnosis", "-")

    diagnosis_data = [
        ["DIAGNOSIS", diagnosis],
        ["CONFIDENCE", f"{data.get('confidence', '-')} %"],
        ["RISK LEVEL", data.get("risk_level", "-")],
    ]

    diagnosis_table = Table(diagnosis_data, colWidths=[200, 200])
    diagnosis_table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))

    elements.append(diagnosis_table)
    elements.append(Spacer(1, 25))

    # -------------------- RECOMMENDATION SECTION --------------------
    elements.append(Paragraph("<b>RECOMMENDATION</b>", styles["Heading2"]))
    elements.append(Spacer(1, 10))

    recommendation_text = get_recommendation(diagnosis)
    elements.append(Paragraph(recommendation_text, styles["Normal"]))
    elements.append(Spacer(1, 30))

    # -------------------- FOOTER --------------------
    footer = f"© {datetime.now().year} Diagnosis System | All Rights Reserved"
    elements.append(Paragraph(footer, styles["Normal"]))

    doc.build(elements)

    return filename