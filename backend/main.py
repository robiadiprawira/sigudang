from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
import hashlib
from typing import Optional, Literal

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
        if not db.query(models.Pelanggan).first():
            default_pelanggan = [
                models.Pelanggan(
                    kode_pelanggan="PLG-001",
                    nama_pelanggan="Amy Siti Kusdiyanti",
                    tipe="BPJS",
                    telepon="Ext. 101",
                    alamat="Lantai 1 Gedung Utama"
                ),
                models.Pelanggan(
                    kode_pelanggan="PLG-002",
                    nama_pelanggan="Wulan Anggraeni",
                    tipe="Umum",
                    telepon="Ext. 102",
                    alamat="Lantai 1 Sayap Kanan"
                ),
                models.Pelanggan(
                    kode_pelanggan="PLG-003",
                    nama_pelanggan="Elia Siti Fatonah",
                    tipe="BPJS",
                    telepon="Ext. 103",
                    alamat="Lantai 1 Sayap Kiri"
                ),
            ]
            db.add_all(default_pelanggan)
    
        if not db.query(models.Supplier).first():
            default_supplier = [
                models.Supplier(
                    kode_supplier="SUP-001",
                    nama_supplier="PT Kimia Farma Trading & Distribution",
                    telepon="021-3847709",
                    alamat="Jl. Budi Utomo No. 1, Jakarta Pusat"
                ),
                models.Supplier(
                    kode_supplier="SUP-002",
                    nama_supplier="PT Enseval Putera Megatrading Tbk",
                    telepon="021-46822422",
                    alamat="Jl. Pulo Lentut No. 10, Kawasan Industri Pulogadung"
                ),
                models.Supplier(
                    kode_supplier="SUP-003",
                    nama_supplier="PT Anugrah Argon Medica",
                    telepon="021-7454222",
                    alamat="Titan Center Lt. 3, Bintaro Jaya"
                ),
            ]
            db.add_all(default_supplier)
    
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

class ObatRequest(BaseModel):
    kode_obat: str
    nama_obat: str
    kategori: str
    satuan: str
    stok_minimal: int = 10

@app.post("/api/obat")
def create_obat(data: ObatRequest, db: Session = Depends(get_db)):
    kode = data.kode_obat.strip().upper()
    nama = data.nama_obat.strip()
    if not kode or not nama:
        raise HTTPException(status_code=400, detail="Kode dan nama obat wajib diisi")
    
    existing = db.query(models.Obat).filter(models.Obat.kode_obat == kode).first()
    if existing:
        raise HTTPException(status_code=400, detail=f"Kode obat '{kode}' sudah terdaftar")
    
    obat_baru = models.Obat(
        kode_obat=kode,
        nama_obat=nama,
        kategori=data.kategori,
        satuan=data.satuan,
        stok=0,
        stok_minimal=data.stok_minimal
    )
    db.add(obat_baru)
    db.commit()
    db.refresh(obat_baru)
    return obat_baru

@app.put("/api/obat/{obat_id}")
def update_obat(obat_id: int, data: ObatRequest, db: Session = Depends(get_db)):
    obat = db.query(models.Obat).filter(models.Obat.id == obat_id).first()
    if not obat:
        raise HTTPException(status_code=404, detail="Data obat tidak ditemukan")
    
    kode = data.kode_obat.strip().upper()
    # Cek duplikasi kode jika kode diubah
    if kode != obat.kode_obat:
        cek_kode = db.query(models.Obat).filter(models.Obat.kode_obat == kode).first()
        if cek_kode:
            raise HTTPException(status_code=400, detail=f"Kode obat '{kode}' sudah dipakai obat lain")
    
    obat.kode_obat = kode
    obat.nama_obat = data.nama_obat.strip()
    obat.kategori = data.kategori
    obat.satuan = data.satuan
    obat.stok_minimal = data.stok_minimal
    
    db.commit()
    db.refresh(obat)
    return obat

@app.delete("/api/obat/{obat_id}")
def delete_obat(obat_id: int, db: Session = Depends(get_db)):
    obat = db.query(models.Obat).filter(models.Obat.id == obat_id).first()
    if not obat:
        raise HTTPException(status_code=404, detail="Data obat tidak ditemukan")
    db.delete(obat)
    db.commit()
    return {"status": "ok"}

class SupplierRequest(BaseModel):
    kode_supplier: str
    nama_supplier: str
    telepon: Optional[str] = ""
    alamat: Optional[str] = ""

@app.get("/api/supplier")
def get_all_supplier(db: Session = Depends(get_db)):
    return db.query(models.Supplier).order_by(models.Supplier.id.asc()).all()

@app.post("/api/supplier")
def create_supplier(data: SupplierRequest, db: Session = Depends(get_db)):
    kode = data.kode_supplier.strip().upper()
    nama = data.nama_supplier.strip()
    if not kode or not nama:
        raise HTTPException(status_code=400, detail="Kode dan nama supplier wajib diisi")
    
    existing = db.query(models.Supplier).filter(models.Supplier.kode_supplier == kode).first()
    if existing:
        raise HTTPException(status_code=400, detail=f"Kode supplier '{kode}' sudah terdaftar")
    
    supplier_baru = models.Supplier(
        kode_supplier=kode,
        nama_supplier=nama,
        telepon=data.telepon.strip() if data.telepon else "",
        alamat=data.alamat.strip() if data.alamat else "",
    )
    db.add(supplier_baru)
    db.commit()
    db.refresh(supplier_baru)
    return supplier_baru

@app.put("/api/supplier/{supplier_id}")
def update_supplier(supplier_id: int, data: SupplierRequest, db: Session = Depends(get_db)):
    supplier = db.query(models.Supplier).filter(models.Supplier.id == supplier_id).first()
    if not supplier:
        raise HTTPException(status_code=404, detail="Data supplier tidak ditemukan")
    
    kode = data.kode_supplier.strip().upper()
    if kode != supplier.kode_supplier:
        cek_kode = db.query(models.Supplier).filter(models.Supplier.kode_supplier == kode).first()
        if cek_kode:
            raise HTTPException(status_code=400, detail=f"Kode supplier '{kode}' sudah dipakai")
    
    supplier.kode_supplier = kode
    supplier.nama_supplier = data.nama_supplier.strip()
    supplier.telepon = data.telepon.strip() if data.telepon else ""
    supplier.alamat = data.alamat.strip() if data.alamat else ""
    
    db.commit()
    db.refresh(supplier)
    return supplier

@app.delete("/api/supplier/{supplier_id}")
def delete_supplier(supplier_id: int, db: Session = Depends(get_db)):
    supplier = db.query(models.Supplier).filter(models.Supplier.id == supplier_id).first()
    if not supplier:
        raise HTTPException(status_code=404, detail="Data supplier tidak ditemukan")
    db.delete(supplier)
    db.commit()
    return {"status": "ok"}

class PelangganRequest(BaseModel):
    kode_pelanggan: str
    nama_pelanggan: str
    tipe: Literal["Umum", "BPJS"] = "Umum"
    telepon: Optional[str] = ""
    alamat: Optional[str] = ""

PelangganRequest.model_rebuild()

@app.get("/api/pelanggan")
def get_all_pelanggan(db: Session = Depends(get_db)):
    return db.query(models.Pelanggan).order_by(models.Pelanggan.id.asc()).all()

@app.post("/api/pelanggan")
def create_pelanggan(data: PelangganRequest, db: Session = Depends(get_db)):
    kode = data.kode_pelanggan.strip().upper()
    nama = data.nama_pelanggan.strip()
    if not kode or not nama:
        raise HTTPException(status_code=400, detail="Kode dan nama pelanggan wajib diisi")
    
    existing = db.query(models.Pelanggan).filter(models.Pelanggan.kode_pelanggan == kode).first()
    if existing:
        raise HTTPException(status_code=400, detail=f"Kode pelanggan '{kode}' sudah terdaftar")
    
    pelanggan_baru = models.Pelanggan(
        kode_pelanggan=kode,
        nama_pelanggan=nama,
        tipe=data.tipe.strip() if data.tipe else "Poli / Internal",
        telepon=data.telepon.strip() if data.telepon else "",
        alamat=data.alamat.strip() if data.alamat else "",
    )
    db.add(pelanggan_baru)
    db.commit()
    db.refresh(pelanggan_baru)
    return pelanggan_baru

@app.put("/api/pelanggan/{pelanggan_id}")
def update_pelanggan(pelanggan_id: int, data: PelangganRequest, db: Session = Depends(get_db)):
    pelanggan = db.query(models.Pelanggan).filter(models.Pelanggan.id == pelanggan_id).first()
    if not pelanggan:
        raise HTTPException(status_code=404, detail="Data pelanggan tidak ditemukan")

    kode = data.kode_pelanggan.strip().upper()
    if kode != pelanggan.kode_pelanggan:
        cek_kode = db.query(models.Pelanggan).filter(models.Pelanggan.kode_pelanggan == kode).first()
        if cek_kode:
            raise HTTPException(status_code=400, detail=f"Kode pelanggan '{kode}' sudah dipakai")

    pelanggan.kode_pelanggan = kode
    pelanggan.nama_pelanggan = data.nama_pelanggan.strip()
    pelanggan.tipe = data.tipe
    pelanggan.telepon = (data.telepon or "").strip()
    pelanggan.alamat = (data.alamat or "").strip()

    db.commit()
    db.refresh(pelanggan)
    return pelanggan

@app.delete("/api/pelanggan/{pelanggan_id}")
def delete_pelanggan(pelanggan_id: int, db: Session = Depends(get_db)):
    pelanggan = db.query(models.Pelanggan).filter(models.Pelanggan.id == pelanggan_id).first()
    if not pelanggan:
        raise HTTPException(status_code=404, detail="Data pelanggan tidak ditemukan")
    db.delete(pelanggan)
    db.commit()
    return {"status": "ok"}

    

