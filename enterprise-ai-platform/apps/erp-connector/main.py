from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from datetime import datetime
import os
import httpx

# ===== CONFIGURACIÓN =====
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://admin:secure_password_123@localhost:5432/enterprise")

app = FastAPI(title="ERP Connector", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===== BASE DE DATOS =====
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    sku = Column(String, unique=True, index=True)
    price = Column(Float)
    stock = Column(Integer)
    category = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)

# ===== SCHEMAS =====
class ProductCreate(BaseModel):
    name: str
    sku: str
    price: float
    stock: int
    category: str

class ProductResponse(BaseModel):
    id: int
    name: str
    sku: str
    price: float
    stock: int
    category: str

# ===== DEPENDENCIAS =====
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ===== ENDPOINTS ERP =====
@app.get("/api/erp/products", response_model=list[ProductResponse])
def get_products(db: Session = Depends(get_db)):
    return db.query(Product).all()

@app.post("/api/erp/products", response_model=ProductResponse)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@app.get("/api/erp/dashboard")
def get_dashboard_stats(db: Session = Depends(get_db)):
    total_products = db.query(Product).count()
    total_stock = db.query(Product).with_entities(Product.stock).all()
    total_value = sum(p.price * p.stock for p in db.query(Product).all())
    return {
        "total_products": total_products,
        "total_stock": sum(s[0] for s in total_stock),
        "inventory_value": total_value
    }

@app.get("/api/erp/health")
def health_check():
    return {"status": "operational", "service": "ERP Connector"}
