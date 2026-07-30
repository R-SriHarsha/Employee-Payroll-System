from sqlalchemy import Column, Integer, String, Float
from app.database import Base

class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    department = Column(String(100))
    designation = Column(String(100))
    base_salary = Column(Float)
    email = Column(String(150), unique=True, nullable=True)
