from typing import Optional
from sqlalchemy.orm import Session
from app.repositories.base_repository import BaseRepository
from app.models.all_models import User, PasswordResetToken

class UserRepository(BaseRepository[User]):
    def __init__(self):
        super().__init__(User)

    def get_by_email(self, db: Session, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email, User.deleted_at.is_(None)).first()

    def get_by_mobile(self, db: Session, mobile_number: str) -> Optional[User]:
        return db.query(User).filter(User.mobile_number == mobile_number, User.deleted_at.is_(None)).first()

    def create_reset_token(self, db: Session, user_id: int, token_hash: str, expires_at) -> PasswordResetToken:
        reset_token = PasswordResetToken(
            user_id=user_id,
            token_hash=token_hash,
            expires_at=expires_at,
            is_used=False
        )
        db.add(reset_token)
        db.commit()
        db.refresh(reset_token)
        return reset_token

    def get_valid_reset_token(self, db: Session, token_hash: str) -> Optional[PasswordResetToken]:
        import datetime
        return db.query(PasswordResetToken).filter(
            PasswordResetToken.token_hash == token_hash,
            PasswordResetToken.is_used.is_(False),
            PasswordResetToken.expires_at > datetime.datetime.utcnow()
        ).first()

user_repository = UserRepository()
