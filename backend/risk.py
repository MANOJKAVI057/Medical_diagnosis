def calculate_risk(vitals, diagnosis):

    score = 0

    if vitals["heart_rate"] > 110:
        score += 2
    if vitals["spo2"] < 94:
        score += 3
    if vitals["temperature"] > 38:
        score += 2
    if vitals["systolic_bp"] > 150:
        score += 2

    if diagnosis != "Normal":
        score += 3

    if score <= 3:
        return "Low"
    elif score <= 6:
        return "Moderate"
    else:
        return "High"