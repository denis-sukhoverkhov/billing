from typing import Any

from app.domain import entities
from app.service_layer.use_cases import create_user_with_wallet
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.service_layer import crud
from src.app.api import deps

router = APIRouter()


@router.post("/", response_model=entities.User)
def create_user(
    *,
    db: Session = Depends(deps.get_db),
    user_in: entities.UserCreate,
) -> Any:
    """
    Create new user.
    """
    user = crud.user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )
    user = create_user_with_wallet(db, user_in=user_in)
    return user
