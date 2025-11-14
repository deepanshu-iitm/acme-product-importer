from sqlalchemy import Column, Integer, String, Boolean, Numeric, DateTime, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)

    sku = Column(String, nullable=False)
    sku_norm = Column(String, nullable=False, unique=True, index=True)  # lower(sku)

    name = Column(String, nullable=False)
    description = Column(String)
    price = Column(Numeric(12, 2))

    active = Column(Boolean, default=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
