"""
Payment Method API endpoints.
Provides operations for managing tokenized payment methods.
"""
from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.core.database import get_db
from app.models.account import Account
from app.models.payment_method import PaymentMethod
from app.schemas.payment_method import PaymentMethodCreate, PaymentMethodResponse

router = APIRouter(prefix="/methods", tags=["Payment Methods"])


@router.post("/", response_model=PaymentMethodResponse, status_code=status.HTTP_201_CREATED)
def create_payment_method(method_data: PaymentMethodCreate, db: Session = Depends(get_db)):
    """
    Add a new tokenized payment method.
    
    2026 Feature: Network Tokenization
    - Store token_id instead of raw card numbers
    - Supports various method types (Apple Pay, Stablecoin, etc.)
    """
    # Validate account exists
    account = db.query(Account).filter(Account.id == method_data.account_id).first()
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Account with ID {method_data.account_id} not found"
        )
    
    try:
        new_method = PaymentMethod(
            account_id=method_data.account_id,
            method_type=method_data.method_type,
            token_id=method_data.token_id
        )
        db.add(new_method)
        db.commit()
        db.refresh(new_method)
        return new_method
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Payment method with this token_id already exists"
        )


@router.get("/{method_id}", response_model=PaymentMethodResponse)
def get_payment_method(method_id: UUID, db: Session = Depends(get_db)):
    """
    Retrieve a payment method by ID.
    """
    method = db.query(PaymentMethod).filter(PaymentMethod.id == method_id).first()
    if not method:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Payment method with ID {method_id} not found"
        )
    return method


@router.get("/account/{account_id}", response_model=List[PaymentMethodResponse])
def list_account_payment_methods(account_id: UUID, db: Session = Depends(get_db)):
    """
    List all payment methods for a specific account.
    """
    # Validate account exists
    account = db.query(Account).filter(Account.id == account_id).first()
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Account with ID {account_id} not found"
        )
    
    methods = db.query(PaymentMethod).filter(PaymentMethod.account_id == account_id).all()
    return methods
