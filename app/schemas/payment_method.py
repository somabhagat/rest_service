"""
Pydantic schemas for PaymentMethod model.
Used for request validation and response serialization.
"""
from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field


class PaymentMethodBase(BaseModel):
    """Base schema with common payment method fields."""
    method_type: str = Field(..., min_length=1, max_length=100, description="Payment type (e.g., Apple Pay, Stablecoin)")
    token_id: str = Field(..., min_length=1, max_length=255, description="Network tokenization ID (not raw card number)")


class PaymentMethodCreate(PaymentMethodBase):
    """Schema for adding a new payment method."""
    account_id: UUID = Field(..., description="Account ID this payment method belongs to")


class PaymentMethodResponse(PaymentMethodBase):
    """Schema for payment method responses."""
    id: UUID
    account_id: UUID
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True
