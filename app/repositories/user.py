from sqlalchemy.orm import Session
from app.models.user import User, CashierSession

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: int) -> User:
        """Finds a supermarket staff profile by primary key."""
        return self.db.query(User).filter(User.user_id == user_id).first()

    def get_by_username(self, user_name: str) -> User:
        """Finds a staff member by their unique username string."""
        return self.db.query(User).filter(User.user_name == user_name).first()

    def save_user(self, user: User) -> User:
        """Persists a new user record into the database."""
        self.db.add(user)
        self.db.commit()
        return user

    def get_active_session(self, session_id: int) -> CashierSession:
        """Finds a specific cashier counter shift session record."""
        return self.db.query(CashierSession).filter(CashierSession.session_id == session_id).first()

    def save_session(self, session: CashierSession) -> CashierSession:
        """Saves a new cashier shift session log entry."""
        self.db.add(session)
        self.db.commit()
        return session
