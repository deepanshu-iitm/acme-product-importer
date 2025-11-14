from sqlalchemy import Column, Integer, String, Boolean, Numeric, DateTime, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Product(Base):
    __tablename__ = "products"

    __table_args__ = {'implicit_returning': True}

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)

    sku = Column(String, nullable=False)
    sku_norm = Column(String, nullable=False, unique=True, index=True)  

    name = Column(String, nullable=False)
    description = Column(String)
    price = Column(Numeric(12, 2))

    active = Column(Boolean, default=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    __mapper_args__ = {
        "confirm_deleted_rows": False
    }
