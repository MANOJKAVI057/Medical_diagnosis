from pydantic import BaseModel
from typing import Optional

class Patient(BaseModel):
    name: str
    age: int
    gender: str
    bloodgroup: str
    mobile: str
    address: str

class LoginInput(BaseModel):
    username: str
    password: str
class VitalInput(BaseModel):
    patient_name: str
    age: int
    heart_rate: float
    systolic_bp: float
    diastolic_bp: float
    spo2: float
    temperature: float