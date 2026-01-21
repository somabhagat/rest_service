"""
Pydantic schemas for Transaction model.
Used for request validation and response serialization.
"""
from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field


class TransactionBase(BaseModel):
    """Base schema with common transaction fields."""
    amount: Decimal = Field(..., gt=0, decimal_places=2, description="Transaction amount (must be positive)")
    description: Optional[str] = Field(None, max_length=500, description="Optional transaction description")


class TransactionCreate(TransactionBase):
    """Schema for creating a new transaction."""
    from_account_id: UUID = Field(..., description="Source account ID")
    to_account_id: UUID = Field(..., description="Destination account ID")


class TransactionResponse(TransactionBase):
    """Schema for transaction responses."""
    id: UUID
    from_account_id: UUID
    to_account_id: UUID
    status: str = Field(..., description="Transaction status: Pending, Completed, or Failed")
    created_at: datetime
    completed_at: Optional[datetime]
    
    class Config:
        from_attributes = True
