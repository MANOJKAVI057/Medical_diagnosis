from pymongo import MongoClient
from bson.objectid import ObjectId
import os

client = MongoClient("mongodb://localhost:27017")
db = client["medical_ai"]

users = db["users"]
records = db["records"]
results = db["results"]
patients_collection = db["patients"]