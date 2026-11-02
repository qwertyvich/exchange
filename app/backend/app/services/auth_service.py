import logging

from sqlalchemy.orm import Session

from app.core.security import get_password_hash, verify_password
from app.models.user import User, UserRole

logger = logging.getLogger(__name__)


def bootstrap_admin(db: Session) -> None:
    if db.query(User).count() == 0:
        db.add(User(username="admin", hashed_password=get_password_hash("admin"), role=UserRole.admin))
        db.commit()
        logger.warning("Bootstrap admin created with username=admin password=admin. Change it immediately.")


def authenticate_user(db: Session, username: str, password: str) -> User | None:
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user
