"""
Payment Method SQLAlchemy model.
Stores tokenized payment methods (Network Tokenization).
"""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.core.database import Base


class PaymentMethod(Base):
    """
    Payment Method model for storing tokenized payment information.
    
    2026 Trend: Network Tokenization
    - token_id stores merchant-specific tokens instead of raw card numbers
    - method_type supports various payment types (Apple Pay, Stablecoin, etc.)
    """
    __tablename__ = "payment_methods"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    account_id = Column(UUID(as_uuid=True), ForeignKey("accounts.id"), nullable=False, index=True)
    method_type = Column(String(100), nullable=False)  # e.g., "Apple Pay", "Stablecoin", "Card Token"
    token_id = Column(String(255), unique=True, nullable=False, index=True)  # Network token
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    account = relationship("Account", back_populates="payment_methods")
    
    def __repr__(self):
        return f"<PaymentMethod(id={self.id}, method_type={self.method_type}, active={self.is_active})>"
