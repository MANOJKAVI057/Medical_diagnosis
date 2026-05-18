AI Multi-Condition Diagnosis System

    An intelligent medical diagnosis platform built using **FastAPI**, **Machine Learning**, and **Computer Vision** 
    to assist healthcare professionals in detecting multiple medical conditions using patient vitals and medical image analysis.

The system allows doctors to:

    * Register/Login securely using JWT authentication
    * Upload patient medical images
    * Enter vital signs
    * Generate AI-based disease predictions
    * View Grad-CAM style heatmaps
    * Calculate patient risk levels
    * Generate downloadable PDF reports
    * Manage patient records
    * View diagnosis analytics

Features

Authentication System
  * Doctor registration
  * Secure login with JWT tokens
  * Protected API endpoints

 AI Diagnosis Engine
  * Medical image preprocessing
  * Multi-condition disease prediction
  * Confidence score generation
  * Vitals-based risk assessment

Report Generation
  * Automated PDF medical reports
  * Diagnosis summary
  * Heatmap visualization

Patient Management
  * Create patient records
  * View all patients
  * Retrieve patient details

Analytics Dashboard
  * Diagnosis distribution statistics
  * Doctor-specific analytics

 Frontend
  * Responsive UI
  * Dark/Light theme support
  * Animated modern landing page

Tech Stack
Backend
  * FastAPI
  * Python
  * MongoDB
  * JWT Authentication
  * Pydantic

AI / ML
  * Custom MedicalDiagnosisSystem
  * Image preprocessing
  * Grad-CAM heatmap simulation

Project Structure

    project/
    │
    ├── main.py
    ├── database.py
    ├── schemas.py
    ├── auth.py
    ├── ml_engine.py
    ├── image_processing.py
    ├── vitals_processing.py
    ├── risk.py
    ├── report.py
    ├── gradcam.py
    │
    ├── temp/
    ├── reports/
    │
    ├── frontend/
    │   ├── index.html
    │   ├── login.html
    │
    └── requirements.txt


# Installation

1. Clone Repository
  	git clone 
    cd medical-ai-diagnosis

2. Create Virtual Environment
   python -m venv venv
   Activate Environment

  Windows

    venv\Scripts\activate
Linux / Mac

    source venv/bin/activate

3. Install Dependencies

       pip install -r requirements.txt

MongoDB Setup
    Ensure MongoDB is running locally or provide a cloud MongoDB URI.


Run the Application

    uvicorn main:app --reload

Server runs at:

    http://127.0.0.1:8000

Inputs

    * Patient Name
    * Age
    * Heart Rate
    * Blood Pressure
    * SpO2
    * Temperature
    * Medical Image

Output

    * Diagnosis
    * Confidence Score
    * Risk Level
    * Heatmap
    * PDF Report

Patient CRUD

Create Patient

    http
    POST /patients


Get All Patients

    http
    GET /patients


 Get Single Patient

    http
    GET /patients/{patient_id}

 History

    http
    GET /history

Analytics

    http
    GET /analytics

Returns diagnosis distribution for the logged-in.

 Security Features

    * JWT Authentication
    * Password hashing
    * Protected endpoints
    * CORS enabled

 Environment Variables
    Create a `.env` file:

    ```env
    SECRET_KEY=medical_secret_key
    MONGO_URI=mongodb://localhost:27017
    ```


 Requirements packages:

    txt
    fastapi
    uvicorn
    python-jose
    pymongo
    pydantic
    python-multipart
    bcrypt
    opencv-python
    torch
    numpy
    reportlab


 Author

Developed by MANOJKAVI057
