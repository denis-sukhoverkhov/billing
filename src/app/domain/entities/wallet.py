from typing import Optional

from pydantic import BaseModel


class WalletBase(BaseModel):
    balance: int = 0
    user_id: int


class WalletCreate(WalletBase):
    pass


class WalletUpdate(WalletBase):
    # email: EmailStr
    # password: str
    pass


class WalletInDBBase(WalletBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class Wallet(WalletInDBBase):
    pass


class WalletNotFound(Exception):
    pass


class InsufficientFundsInTheAccount(Exception):
    pass
