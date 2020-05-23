from typing import Optional

from app.service_layer.crud.base import CRUDBase
from app.domain.entities.user import UserCreate, UserUpdate
from app.infrastructure.sqlalchemy.models import User
from sqlalchemy.orm import Session


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        db.begin(subtransactions=True)
        db_obj = User(
            email=obj_in.email,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


user = CRUDUser(User)
