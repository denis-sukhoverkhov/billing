from typing import Any

from app.domain import entities
from app.service_layer.use_cases import create_user_with_wallet
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.service_layer import crud
from app.service_layer.api import deps
from starlette import status

router = APIRouter()


@router.post("/", response_model=entities.User, status_code=status.HTTP_201_CREATED)
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
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user with this email already exists in the system.",
        )
    user = create_user_with_wallet(db, user_in=user_in)
    return user
