from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import models
from database import engine

# Buat semua tabel di SQLite secara otomatis jika belum ada
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="API Sistem Pergudangan Obat")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5175"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/ping")
def ping():
    return {"status": "ok", "message": "Backend FastAPI & Database Siap!"}