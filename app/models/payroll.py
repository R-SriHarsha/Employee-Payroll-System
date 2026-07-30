from sqlalchemy import Column, Integer, Float, ForeignKey, UniqueConstraint
from app.database import Base

class Payroll(Base):
    __tablename__ = "payroll"

    id = Column(Integer, primary_key=True,index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"))
    month = Column(Integer)
    year = Column(Integer)
    net_salary = Column(Float)
    basic_salary = Column(Float)
    hra = Column(Float)
    da = Column(Float)
    pf = Column(Float)
    tax = Column(Float)
    gross_salary = Column(Float)

    __table_args__ = (
        UniqueConstraint('employee_id', 'month', 'year', name='unique_payroll'),
    )