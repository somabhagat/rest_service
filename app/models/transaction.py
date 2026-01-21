"""
Transaction SQLAlchemy model.
Tracks money movements between accounts with status support for Instant Payments.
"""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, Numeric, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.core.database import Base


class Transaction(Base):
    """
    Transaction model for tracking money transfers between accounts.
    
    2026 Trend: Instant Payments
    - status field supports real-time payment status tracking
    - Status values: "Pending", "Completed", "Failed"
    """
    __tablename__ = "transactions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    from_account_id = Column(UUID(as_uuid=True), ForeignKey("accounts.id"), nullable=False, index=True)
    to_account_id = Column(UUID(as_uuid=True), ForeignKey("accounts.id"), nullable=False, index=True)
    amount = Column(Numeric(precision=12, scale=2), nullable=False)
    status = Column(String(20), nullable=False, default="Pending")  # Pending, Completed, Failed
    description = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    completed_at = Column(DateTime, nullable=True)
    
    # Relationships
    from_account = relationship(
        "Account",
        foreign_keys=[from_account_id],
        back_populates="transactions_sent"
    )
    to_account = relationship(
        "Account",
        foreign_keys=[to_account_id],
        back_populates="transactions_received"
    )
    
    def __repr__(self):
        return f"<Transaction(id={self.id}, amount={self.amount}, status={self.status})>"
