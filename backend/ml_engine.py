import os
import torch
import torch.nn as nn
import torchvision.models as models
import numpy as np
import pickle

# =========================================================
# ------------------- CONFIGURATION -----------------------
# =========================================================

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

conditions = [
    "Hypoxia",
    "Hypertension",
    "Hypotension",
    "Tachycardia",
    "Bradycardia",
    "Fever",
    "Pneumonia",
    "Heart Disease",
    "Sepsis",
    "Normal"
]

num_classes = len(conditions)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

IMAGE_MODEL_PATH = os.path.join(BASE_DIR, "trained_models/image_model_state.pt")
VITALS_MODEL_PATH = os.path.join(BASE_DIR, "trained_models/vitals_model.pkl")

# =========================================================
# ------------------- IMAGE MODEL -------------------------
# =========================================================

def load_image_model():
    model = models.resnet18(weights=None)
    model.fc = nn.Linear(model.fc.in_features, num_classes)

    model.load_state_dict(
        torch.load(IMAGE_MODEL_PATH, map_location=DEVICE)
    )

    model.to(DEVICE)
    model.eval()
    return model


# =========================================================
# ------------------- VITALS MODEL ------------------------
# =========================================================

def load_vitals_model():
    with open(VITALS_MODEL_PATH, "rb") as f:
        model = pickle.load(f)
    return model


# =========================================================
# ------------------- SYSTEM CLASS ------------------------
# =========================================================

class MedicalDiagnosisSystem:

    def __init__(self):
        print("Loading ML models...")
        self.image_model = load_image_model()
        self.vitals_model = load_vitals_model()
        print("Models loaded successfully.")

    def predict_image(self, image_tensor):
        image_tensor = image_tensor.to(DEVICE)

        # Convert grayscale to 3 channels
        if image_tensor.dim() == 4 and image_tensor.shape[1] == 1:
            image_tensor = image_tensor.repeat(1, 3, 1, 1)

        with torch.no_grad():
            logits = self.image_model(image_tensor)
            probs = torch.softmax(logits, dim=1)

        return probs.cpu().numpy()[0]

    def predict_vitals(self, vitals_list):
        v = np.array(vitals_list).reshape(1, -1)
        probs = self.vitals_model.predict_proba(v)
        return probs[0]

    def final_diagnosis(self, img_probs, vit_probs, img_weight=0.6, vit_weight=0.4):
        # Make lengths equal
        if len(img_probs) != len(vit_probs):
           min_len = min(len(img_probs), len(vit_probs))
           img_probs = img_probs[:min_len]
           vit_probs = vit_probs[:min_len]

        final_probs = (img_weight * img_probs) + (vit_weight * vit_probs)
        

        final_index = np.argmax(final_probs)
        diagnosis = conditions[final_index]
        confidence = float(final_probs[final_index])

        return diagnosis, confidence

    def diagnose(self, image_tensor, vitals_list):
        img_probs = self.predict_image(image_tensor)
        vit_probs = self.predict_vitals(vitals_list)

        diagnosis, confidence = self.final_diagnosis(img_probs, vit_probs)

        return {
            "diagnosis": diagnosis,
            "confidence": round(confidence * 100, 2)
        }