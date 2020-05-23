from datetime import datetime
from sqlalchemy import Boolean, Column, Integer, String, DateTime, text
from app.infrastructure.sqlalchemy.db.base_class import Base
from sqlalchemy.orm import relationship


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    is_active = Column(Boolean(), default=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow, server_default=text("timezone('utc', now())"))
    updated_at = Column(DateTime, nullable=True)
    wallet = relationship("Wallet")
