from fastapi import FastAPI, Form, UploadFile, File, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
import shutil
import uuid
import os
from datetime import datetime
from bson.objectid import ObjectId

from database import users, results, patients_collection
from schemas import LoginInput, Patient
from image_processing import preprocess_image
from vitals_processing import prepare_vitals
from risk import calculate_risk
from report import generate_report
from gradcam import fake_heatmap
from auth import hash_password, verify_password, create_token
from ml_engine import MedicalDiagnosisSystem

# =========================================================
# CONFIG
# =========================================================

SECRET = "medical_secret_key"
security = HTTPBearer()

app = FastAPI(title="AI Multi-Condition Diagnosis System")

# Load ML system once
diagnosis_system = MedicalDiagnosisSystem()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs("temp", exist_ok=True)
os.makedirs("reports", exist_ok=True)

# =========================================================
# AUTH
# =========================================================

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET, algorithms=["HS256"])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.post("/register")
def register(username: str = Form(...), password: str = Form(...)):
    if users.find_one({"username": username}):
        raise HTTPException(status_code=400, detail="User already exists")

    users.insert_one({
        "username": username,
        "password": hash_password(password)
    })
    return {"message": "Doctor registered successfully"}

@app.post("/login")
def login(data: LoginInput):
    user = users.find_one({"username": data.username})
    if not user or not verify_password(data.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_token(data.username)
    return {"token": token}

# =========================================================
# DIAGNOSIS
# =========================================================

@app.post("/diagnose/")
async def diagnose(
    patient_name: str = Form(...),
    age: int = Form(...),
    heart_rate: int = Form(...),
    systolic_bp: int = Form(...),
    diastolic_bp: int = Form(...),
    spo2: int = Form(...),
    temperature: float = Form(...),
    image: UploadFile = File(...),
    current_user: str = Depends(get_current_user)
):

    try:
        vitals_dict = {
            "age": age,
            "heart_rate": heart_rate,
            "systolic_bp": systolic_bp,
            "diastolic_bp": diastolic_bp,
            "spo2": spo2,
            "temperature": temperature
        }

        file_path = f"temp/{uuid.uuid4()}.png"
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)

        img_tensor = preprocess_image(file_path)
        vitals_list = prepare_vitals(vitals_dict)

        result = diagnosis_system.diagnose(img_tensor, vitals_list)

        diagnosis = result["diagnosis"]
        confidence = result["confidence"]

        risk = calculate_risk(vitals_dict, diagnosis)

        heatmap_path = fake_heatmap(file_path)

        record = {
            "doctor": current_user,
            "patient_name": patient_name,
            "vitals": vitals_dict,
            "diagnosis": diagnosis,
            "confidence": confidence,
            "risk_level": risk,
            "heatmap": heatmap_path,
            "image_path": file_path,
            "date": datetime.now()
        }

        results.insert_one(record)

        pdf_path = generate_report(record)

        return {
            "patient_name": patient_name,
            "diagnosis": diagnosis,
            "confidence_percent": confidence,
            "risk_level": risk,
            "heatmap": heatmap_path,
            "report": pdf_path
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# =========================================================
# HISTORY
# =========================================================

@app.get("/history")
def get_history(current_user: str = Depends(get_current_user)):
    data = list(results.find({"doctor": current_user}, {"_id": 0}))
    return data

# =========================================================
# PATIENT CRUD
# =========================================================

@app.post("/patients")
async def create_patient(patient: Patient):
    patient_dict = patient.dict()
    result = patients_collection.insert_one(patient_dict)
    return {
        "message": "Patient created successfully",
        "patient_id": str(result.inserted_id)
    }

@app.get("/patients")
async def get_patients():
    patients = []
    for patient in patients_collection.find():
        patient["_id"] = str(patient["_id"])
        patients.append(patient)
    return patients

@app.get("/patients/{patient_id}")
async def get_patient(patient_id: str):
    patient = patients_collection.find_one({"_id": ObjectId(patient_id)})

    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    patient["_id"] = str(patient["_id"])
    return patient

@app.get("/analytics")
def analytics(current_user: str = Depends(get_current_user)):
    pipeline = [
        {"$match": {"doctor": current_user}},  # Filter by logged doctor
        {"$group": {"_id": "$diagnosis", "count": {"$sum": 1}}}
    ]

    raw_data = list(results.aggregate(pipeline))

    distribution = {}
    for item in raw_data:
        distribution[item["_id"]] = item["count"]

    return {
        "diagnosis_distribution": distribution
    }
@app.get("/")
def root():
    return {"message": "Medical Diagnosis API Running"}