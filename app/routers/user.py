import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.user import User, CashierSession
from app.schemas.user import UserCreateSchema

router = APIRouter(prefix="/users", tags=["Employee & Shift Management"])

@router.post("/register", status_code=status.HTTP_201_CREATED)
def add_new_employee(employee: UserCreateSchema, db: Session = Depends(get_db)):
    """Registers a new supermarket staff profile into the database core."""
    existing = db.query(User).filter(User.user_name == employee.user_name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username is already taken.")
        
    new_user = User(
        user_name=employee.user_name,
        password_hash=employee.password,  # Storing plain text temporarily as requested
        first_name=employee.first_name,
        last_name=employee.last_name,
        role_id=employee.role_id,
        is_active=True
    )
    db.add(new_user)
    db.commit()
    return {"message": "Staff member created successfully!", "user_id": new_user.user_id}


@router.post("/sessions/open", status_code=status.HTTP_201_CREATED)
def open_cashier_shift(user_id: int, counter_number: int, opening_balance: float, db: Session = Depends(get_db)):
    """Opens a physical drawer register shift for multi-checkout lanes."""
    # Verify user exists
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Staff user not found.")
        
    new_session = CashierSession(
        user_id=user_id,
        counter_number=counter_number,
        opening_balance=opening_balance,
        opened_at=datetime.datetime.utcnow()
    )
    db.add(new_session)
    db.commit()
    db.refresh(new_session)
    return {"message": "Shift opened successfully!", "session_id": new_session.session_id}



@router.get("/sessions/active")
def list_active_lane_shifts(db: Session = Depends(get_db)):
    """
    ACCESS CONTROL: Pulls all recorded desk shift logs so management can audit 
    which cashier was operating which register counter number.
    """
    # Returns a list of all registers and their open/close balances
    sessions = db.query(CashierSession).all()
    return [
        {
            "session_id": s.session_id,
            "user_id": s.user_id,
            "counter_number": s.counter_number,
            "opened_at": s.opened_at,
            "is_closed": s.closed_at is not None,
            "opening_balance": float(s.opening_balance),
            "closing_balance": float(s.closing_balance) if s.closing_balance else None
        }
        for s in sessions
    ]
