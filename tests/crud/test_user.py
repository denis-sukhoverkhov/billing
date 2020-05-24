from app.domain.entities import UserCreate
from app.service_layer import crud
from sqlalchemy.orm import Session

# from app import crud
from tests.helpers import random_email


def test_create_user(db: Session) -> None:
    email = random_email()
    user_in = UserCreate(email=email, )
    user = crud.user.create(db, obj_in=user_in)
    assert user.email == email
    assert user.is_active is True
    assert user.created_at is not None
    assert hasattr(user, "id")
