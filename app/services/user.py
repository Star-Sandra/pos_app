import datetime
from decimal import Decimal
from sqlalchemy.orm import Session
from app.models.user import User, CashierSession

class UserService:
    @staticmethod
    def register_staff_user(db: Session, user_name: str, password_plain: str, first_name: str, last_name: str, role_id: int) -> User:
        """Saves a new supermarket employee profile into the database."""
        new_user = User(
            user_name=user_name,
            password_hash=password_plain,  # Explicitly storing plain text as requested for now
            first_name=first_name,
            last_name=last_name,
            role_id=role_id,
            is_active=True
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

    @staticmethod
    def open_shift_session(db: Session, user_id: int, counter_number: int, opening_balance: Decimal) -> CashierSession:
        """Registers a new active counter checkout lane session for a cashier."""
        new_session = CashierSession(
            user_id=user_id,
            counter_number=counter_number,
            opening_balance=opening_balance,
            opened_at=datetime.datetime.utcnow()
        )
        db.add(new_session)
        db.commit()
        db.refresh(new_session)
        return new_session

    @staticmethod
    def close_shift_session(db: Session, session_id: int, closing_balance: Decimal) -> CashierSession:
        """Closes out a cashier's session window and reconciles final cash register drawer drops."""
        session = db.query(CashierSession).filter(CashierSession.session_id == session_id).first()
        if not session:
            raise ValueError("Target cashier shift session not found.")
            
        session.closed_at = datetime.datetime.utcnow()
        session.closing_balance = closing_balance
        db.commit()
        db.refresh(session)
        return session
