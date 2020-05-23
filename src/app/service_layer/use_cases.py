from app import crud
from app.domain.entities.user import UserCreate
from app.domain.entities.wallet import WalletCreate
from sqlalchemy.orm import Session


def create_user_with_wallet(db: Session, user_in: UserCreate):
    # with db.begin(subtransactions=True) as conn:
    # db.begin(subtransactions=True)
    user = crud.user.create(db, obj_in=user_in)
    wallet = crud.wallet.create(db, obj_in=WalletCreate(user_id=user.id))
    db.commit()
    # db.refresh(user)

    return user
