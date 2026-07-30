from sqlalchemy import Column, Integer, ForeignKey
from app.database import Base

class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey("employees.id"))
    month = Column(Integer)
    year = Column(Integer)
    present_days = Column(Integer)
    leaves = Column(Integer)
