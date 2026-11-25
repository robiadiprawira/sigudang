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
        if not db.query(models.Kategori).first():
            default_kategori = [
                models.Kategori(nama_kategori="Obat Bebas"),
                models.Kategori(nama_kategori="Obat Bebas Terbatas"),
                models.Kategori(nama_kategori="Obat Keras"),
                models.Kategori(nama_kategori="Obat Luar"),
                models.Kategori(nama_kategori="Suplemen & Vitamin"),
                ]
            db.add_all(default_kategori)
        if not db.query(models.Satuan).first():
            default_satuan = [
                models.Satuan(nama_satuan="Strip / Lembar"),
                models.Satuan(nama_satuan="Botol"),
                models.Satuan(nama_satuan="Box"),
                models.Satuan(nama_satuan="Tube"),
                                models.Satuan(nama_satuan="Tablet / Kapsul"),
                ]
            db.add_all(default_satuan)

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


class KategoriRequest(BaseModel):
    nama_kategori: str

class SatuanRequest(BaseModel):
    nama_satuan: str

@app.get("/api/kategori")
def get_all_kategori(db: Session = Depends(get_db)):
    return db.query(models.Kategori).order_by(models.Kategori.id.asc()).all()

@app.post("/api/kategori")
def create_kategori(data: KategoriRequest, db: Session = Depends(get_db)):
    nama = data.nama_kategori.strip()
    if not nama:
        raise HTTPException(status_code=400, detail="Nama kategori tidak boleh kosong")
    existing = db.query(models.Kategori).filter(models.Kategori.nama_kategori.ilike(nama)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Kategori tersebut sudah ada")
    baru = models.Kategori(nama_kategori=nama)
    db.add(baru)
    db.commit()
    db.refresh(baru)
    return baru

@app.delete("/api/kategori/{kategori_id}")
def delete_kategori(kategori_id: int, db: Session = Depends(get_db)):
    item = db.query(models.Kategori).filter(models.Kategori.id == kategori_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Kategori tidak ditemukan")
    db.delete(item)
    db.commit()
    return {"status": "ok"}

@app.get("/api/satuan")
def get_all_satuan(db: Session = Depends(get_db)):
    return db.query(models.Satuan).order_by(models.Satuan.id.asc()).all()

@app.post("/api/satuan")
def create_satuan(data: SatuanRequest, db: Session = Depends(get_db)):
    nama = data.nama_satuan.strip()
    if not nama:
        raise HTTPException(status_code=400, detail="Nama satuan tidak boleh kosong")
    existing = db.query(models.Satuan).filter(models.Satuan.nama_satuan.ilike(nama)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Satuan tersebut sudah ada")
    baru = models.Satuan(nama_satuan=nama)
    db.add(baru)
    db.commit()
    db.refresh(baru)
    return baru

@app.delete("/api/satuan/{satuan_id}")
def delete_satuan(satuan_id: int, db: Session = Depends(get_db)):
    item = db.query(models.Satuan).filter(models.Satuan.id == satuan_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Satuan tidak ditemukan")
    db.delete(item)
    db.commit()
    return {"status": "ok"}


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