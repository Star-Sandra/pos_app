import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from ..database import base

class User(base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String(250), unique=True, nullable=False, index=True)
    password_hash = Column(String(250), nullable=False)
    first_name = Column(String(250), nullable=False)
    last_name = Column(String(250), nullable=False)
    role_id = Column(Integer, nullable=False)  # Map to role permissions
    is_active = Column(Boolean, default=True, nullable=False)

    
    sessions = relationship("CashierSession", back_populates="user")


class CashierSession(base):
    __tablename__ = "cashier_sessions"

    session_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    counter_number = Column(Integer, nullable=False)
    opened_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    closed_at = Column(DateTime, nullable=True)
    opening_balance = Column(Numeric(10, 2), nullable=False)
    closing_balance = Column(Numeric(10, 2), nullable=True)

    
    user = relationship("User", back_populates="sessions")
    sales = relationship("Sale", back_populates="session")
