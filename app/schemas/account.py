"""
Pydantic schemas for Account model.
Used for request validation and response serialization.
"""
from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field


class AccountBase(BaseModel):
    """Base schema with common account fields."""
    name: str = Field(..., min_length=1, max_length=255, description="Account holder name")
    email: EmailStr = Field(..., description="Unique email address")


class AccountCreate(AccountBase):
    """Schema for creating a new account."""
    is_agent: bool = Field(default=False, description="Whether this is an AI agent account (Agentic Commerce)")
    initial_balance: Decimal = Field(default=Decimal("0.00"), ge=0, description="Initial account balance")


class AccountUpdate(BaseModel):
    """Schema for updating an existing account."""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    email: Optional[EmailStr] = None


class AccountResponse(AccountBase):
    """Schema for account responses."""
    id: UUID
    balance: Decimal
    is_agent: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True  # Pydantic v2 (was orm_mode in v1)
