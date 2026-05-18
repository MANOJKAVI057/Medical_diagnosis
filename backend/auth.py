from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

SECRET = "medical_secret_key"
pwd = CryptContext(schemes=["bcrypt"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def hash_password(password):
    return pwd.hash(password)

def verify_password(password, hashed):
    return pwd.verify(password, hashed)

def create_token(username):
    payload = {
        "sub": username,
        "exp": datetime.utcnow() + timedelta(days=10)
    }
    return jwt.encode(payload, SECRET, algorithm="HS256")

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET, algorithms=["HS256"])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")