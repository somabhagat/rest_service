"""
Account SQLAlchemy model.
Supports both regular users and AI agents (Agentic Commerce).
"""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, Numeric, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.core.database import Base


class Account(Base):
    """
    Account model representing user or AI agent profiles.
    
    2026 Trend: Agentic Commerce
    - is_agent field identifies AI agents that make autonomous purchases
    """
    __tablename__ = "accounts"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    balance = Column(Numeric(precision=12, scale=2), nullable=False, default=0.00)
    is_agent = Column(Boolean, default=False, nullable=False)  # Agentic Commerce flag
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    payment_methods = relationship("PaymentMethod", back_populates="account", cascade="all, delete-orphan")
    transactions_sent = relationship(
        "Transaction",
        foreign_keys="Transaction.from_account_id",
        back_populates="from_account"
    )
    transactions_received = relationship(
        "Transaction",
        foreign_keys="Transaction.to_account_id",
        back_populates="to_account"
    )
    
    def __repr__(self):
        return f"<Account(id={self.id}, email={self.email}, is_agent={self.is_agent})>"
