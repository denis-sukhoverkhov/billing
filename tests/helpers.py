import random
import string

from app.domain.entities import UserCreate

from app.domain.entities.wallet import WalletCreate
from app.infrastructure.sqlalchemy import models
from app.service_layer import crud
from sqlalchemy.orm import Session


def random_lower_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=32))


def random_email() -> str:
    return f"{random_lower_string()}@{random_lower_string()}.com"


def create_random_user(db: Session) -> models.User:
    email = random_email()
    user_in = UserCreate(email=email, )
    user = crud.user.create(db=db, obj_in=user_in)
    return user


def create_random_user_with_wallet(db: Session, *, balance: int = 0) -> (models.User, models.Wallet):
    random_user = create_random_user(db)
    wallet_in = WalletCreate(user_id=random_user.id, balance=balance)
    wallet = crud.wallet.create(db, obj_in=wallet_in)
    db.commit()

    return random_user, wallet
