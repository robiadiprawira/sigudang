from sqlalchemy import Column, Integer, String, Float, Date, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    nama = Column(String, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, default="staff")  # 'superadmin' atau 'staff'
    is_active = Column(Boolean, default=True)

class Obat(Base):
    __tablename__ = "obat"

    id = Column(Integer, primary_key=True, index=True)
    kode_obat = Column(String, unique=True, index=True, nullable=False)
    nama_obat = Column(String, index=True, nullable=False)
    satuan = Column(String, nullable=False)  # Box, Strip, Botol, Tablet
    harga_jual = Column(Float, default=0)
    stok_minimal = Column(Integer, default=10)
    total_stok = Column(Integer, default=0)  # Otomatis update dari transaksi

    batches = relationship("ObatBatch", back_populates="obat")

class ObatBatch(Base):
    __tablename__ = "obat_batch"

    id = Column(Integer, primary_key=True, index=True)
    obat_id = Column(Integer, ForeignKey("obat.id"), nullable=False)
    nomor_batch = Column(String, nullable=False)
    expired_date = Column(Date, nullable=False)
    stok_tersedia = Column(Integer, default=0)

    obat = relationship("Obat", back_populates="batches")

class TransaksiMasuk(Base):
    __tablename__ = "transaksi_masuk"

    id = Column(Integer, primary_key=True, index=True)
    kode_transaksi = Column(String, unique=True, index=True)
    tanggal = Column(DateTime, default=datetime.utcnow)
    supplier = Column(String, nullable=False)
    keterangan = Column(String, nullable=True)

    details = relationship("DetailMasuk", back_populates="transaksi")

class DetailMasuk(Base):
    __tablename__ = "detail_masuk"

    id = Column(Integer, primary_key=True, index=True)
    transaksi_masuk_id = Column(Integer, ForeignKey("transaksi_masuk.id"))
    obat_id = Column(Integer, ForeignKey("obat.id"))
    nomor_batch = Column(String, nullable=False)
    expired_date = Column(Date, nullable=False)
    jumlah = Column(Integer, nullable=False)

    transaksi = relationship("TransaksiMasuk", back_populates="details")

class TransaksiKeluar(Base):
    __tablename__ = "transaksi_keluar"

    id = Column(Integer, primary_key=True, index=True)
    kode_transaksi = Column(String, unique=True, index=True)
    tanggal = Column(DateTime, default=datetime.utcnow)
    tujuan_atau_pembeli = Column(String, nullable=False)
    total_harga = Column(Float, default=0)

    details = relationship("DetailKeluar", back_populates="transaksi")

class DetailKeluar(Base):
    __tablename__ = "detail_keluar"

    id = Column(Integer, primary_key=True, index=True)
    transaksi_keluar_id = Column(Integer, ForeignKey("transaksi_keluar.id"))
    obat_id = Column(Integer, ForeignKey("obat.id"))
    batch_id = Column(Integer, ForeignKey("obat_batch.id"))
    jumlah = Column(Integer, nullable=False)
    harga_satuan = Column(Float, nullable=False)
    subtotal = Column(Float, nullable=False)

    transaksi = relationship("TransaksiKeluar", back_populates="details")