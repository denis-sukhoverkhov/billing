from datetime import datetime

from app.infrastructure.sqlalchemy.db.base_class import Base
from sqlalchemy import Boolean, Column, DateTime, Integer, text, BigInteger, ForeignKey


class Wallet(Base):
    id = Column(Integer, primary_key=True)
    balance = Column(BigInteger, nullable=False, default=0, comment='in cents')
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    is_active = Column(Boolean(), default=True)
    created_at = Column(
        DateTime, nullable=False, default=datetime.utcnow, server_default=text("timezone('utc', now())"))
    updated_at = Column(DateTime, nullable=True)


class WalletHistory(Base):
    id = Column(Integer, primary_key=True)
    wallet_id = Column(ForeignKey("wallet.id"), nullable=False)
    balance = Column(BigInteger, nullable=False)
    user_id = Column(Integer, nullable=False)
    created_at = Column(
        DateTime, nullable=False, default=datetime.utcnow, server_default=text("timezone('utc', now())"))
