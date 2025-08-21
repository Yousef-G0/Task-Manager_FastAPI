import os
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any

from fastapi import Depends, HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
import jwt  # PyJWT
from passlib.context import CryptContext

from . import models
from .database import get_db

# ---- JWT / Password config ----
SECRET_KEY = os.getenv("SECRET_KEY", "change-me-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
auth_scheme = HTTPBearer(auto_error=False)

# ---- password helpers ----
def verify_password(plain: str, hashed: str) -> bool:
    return pwd.verify(plain, hashed)

def hash_password(plain: str) -> str:
    return pwd.hash(plain)

# ---- token helpers ----
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# ---- dependencies ----
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Security(auth_scheme),
    db: Session = Depends(get_db),
) -> models.User:
    if credentials is None:
        raise HTTPException(status_code=401, detail="Missing Authorization header")
    token = credentials.credentials
    try:
        payload: Dict[str, Any] = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload.get("sub"))
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user = db.get(models.User, user_id)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

def require_role(role: str):
    def checker(user: models.User = Depends(get_current_user)) -> models.User:
        if user.role != role:
            raise HTTPException(status_code=403, detail=f"Requires role '{role}'")
        return user
    return checker
