from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
import hashlib

import models
from database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="API Gudang Obat")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

# Otomatis buat akun superadmin default jika tabel users masih kosong
@app.on_event("startup")
def seed_default_user():
    db = SessionLocal()
    try:
        existing_user = db.query(models.User).first()
        if not existing_user:
            admin_user = models.User(
                nama="Admin Gudang",
                username="admin",
                password=hash_password("admin123"),
                role="superadmin",
                is_active=True
            )
            db.add(admin_user)
            db.commit()
    finally:
        db.close()

class LoginRequest(BaseModel):
    username: str
    password: str

@app.get("/api/ping")
def ping():
    return {"status": "ok", "message": "Backend FastAPI & Database Siap!"}

@app.post("/api/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == data.username).first()
    if not user or user.password != hash_password(data.password):
        raise HTTPException(status_code=401, detail="Username atau password salah")
    
    if not user.is_active:
        raise HTTPException(status_code=403, detail="Akun Anda tidak aktif. Hubungi Superadmin.")
    
    return {
        "status": "ok",
        "user": {
            "id": user.id,
            "nama": user.nama,
            "username": user.username,
            "role": user.role
        }
    }