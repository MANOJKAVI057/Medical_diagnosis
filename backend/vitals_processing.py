import numpy as np

def prepare_vitals(vitals):
    v = [
        vitals["age"],
        vitals["spo2"],
        vitals["systolic_bp"],
        vitals["diastolic_bp"],
        vitals["heart_rate"],
        vitals["temperature"],
	vitals.get("respiratory", 15)
    ]
    return np.array(v).reshape(1, -1)  # shape [1,6]