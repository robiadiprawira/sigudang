from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
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
def seed_initial_data():
    db = SessionLocal()
    try:
        if not db.query(models.User).first():
            admin_user = models.User(
                nama="Admin Gudang",
                username="admin",
                password=hash_password("admin123"),
                role="superadmin",
                is_active=True
            )
            db.add(admin_user)

        if not db.query(models.Obat).first():
            sample_obat = [
                models.Obat(kode_obat="OBT-001", nama_obat="Paracetamol 500mg", kategori="Obat Bebas", satuan="Strip / Lembar", stok=120, stok_minimal=20),
                models.Obat(kode_obat="OBT-002", nama_obat="OBH Combi Batuk Flu 100ml", kategori="Obat Bebas Terbatas", satuan="Botol", stok=35, stok_minimal=10),
                models.Obat(kode_obat="OBT-003", nama_obat="Amoxicillin 500mg", kategori="Obat Keras", satuan="Box", stok=8, stok_minimal=10),
                models.Obat(kode_obat="OBT-004", nama_obat="Betadine Salep Antiseptik 10g", kategori="Obat Luar", satuan="Tube", stok=0, stok_minimal=5),
                models.Obat(kode_obat="OBT-005", nama_obat="Vitamin C 500mg", kategori="Suplemen", satuan="Strip / Lembar", stok=50, stok_minimal=15),
            ]
            db.add_all(sample_obat)

        db.commit()
    finally:
        db.close()

# Schema untuk ubah jumlah stok obat
class UpdateStockRequest(BaseModel):
    stok: int

# 1. Ambil semua data obat & stok
@app.get("/api/stock")
def get_all_stock(db: Session = Depends(get_db)):
    return db.query(models.Obat).order_by(models.Obat.id.asc()).all()

# 2. Ubah jumlah stok obat saja
@app.patch("/api/stock/{obat_id}")
def update_stock_jumlah(obat_id: int, data: UpdateStockRequest, db: Session = Depends(get_db)):
    if data.stok < 0:
        raise HTTPException(status_code=400, detail="Jumlah stok tidak boleh kurang dari 0")
    
    obat = db.query(models.Obat).filter(models.Obat.id == obat_id).first()
    if not obat:
        raise HTTPException(status_code=404, detail="Data obat tidak ditemukan")
    
    obat.stok = data.stok
    db.commit()
    db.refresh(obat)
    return {"status": "ok", "message": "Jumlah stok berhasil diperbarui", "data": obat}

# 3. Hapus data obat
@app.delete("/api/stock/{obat_id}")
def delete_obat_stock(obat_id: int, db: Session = Depends(get_db)):
    obat = db.query(models.Obat).filter(models.Obat.id == obat_id).first()
    if not obat:
        raise HTTPException(status_code=404, detail="Data obat tidak ditemukan")
    
    db.delete(obat)
    db.commit()
    return {"status": "ok", "message": "Data obat berhasil dihapus"}

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