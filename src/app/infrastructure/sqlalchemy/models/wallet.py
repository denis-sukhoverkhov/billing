from datetime import datetime

from app.infrastructure.sqlalchemy.db.base_class import Base
from sqlalchemy import Boolean, Column, DateTime, Integer, text, BigInteger, ForeignKey
from sqlalchemy.orm import relationship


class Wallet(Base):
    id = Column(Integer, primary_key=True)
    balance = Column(BigInteger, nullable=False, default=0, comment='in cents')
    user_id = Column(Integer, ForeignKey("user.id"))
    # user = relationship("User", back_populates="wallets")
    is_active = Column(Boolean(), default=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow, server_default=text("timezone('utc', now())"))
    updated_at = Column(DateTime, nullable=True)


class WalletHistory(Base):
    id = Column(Integer, primary_key=True)
    balance = Column(BigInteger)
    user_id = Column(Integer)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow, server_default=text("timezone('utc', now())"))
