"""
Account API endpoints.
Provides CRUD operations for user and AI agent accounts.
"""
from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.core.database import get_db
from app.models.account import Account
from app.schemas.account import AccountCreate, AccountUpdate, AccountResponse

router = APIRouter(prefix="/accounts", tags=["Accounts"])


@router.post("/", response_model=AccountResponse, status_code=status.HTTP_201_CREATED)
def create_account(account_data: AccountCreate, db: Session = Depends(get_db)):
    """
    Create a new account (user or AI agent).
    
    2026 Feature: Agentic Commerce
    - Set is_agent=true to create an AI agent account
    """
    try:
        new_account = Account(
            name=account_data.name,
            email=account_data.email,
            balance=account_data.initial_balance,
            is_agent=account_data.is_agent
        )
        db.add(new_account)
        db.commit()
        db.refresh(new_account)
        return new_account
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Account with this email already exists"
        )


@router.get("/{account_id}", response_model=AccountResponse)
def get_account(account_id: UUID, db: Session = Depends(get_db)):
    """
    Retrieve an account by ID.
    Returns account details including current balance.
    """
    account = db.query(Account).filter(Account.id == account_id).first()
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Account with ID {account_id} not found"
        )
    return account


@router.get("/", response_model=List[AccountResponse])
def list_accounts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    List all accounts with pagination.
    """
    accounts = db.query(Account).offset(skip).limit(limit).all()
    return accounts


@router.patch("/{account_id}", response_model=AccountResponse)
def update_account(account_id: UUID, account_data: AccountUpdate, db: Session = Depends(get_db)):
    """
    Update account details (name or email).
    Note: Balance cannot be updated directly - use transactions instead.
    """
    account = db.query(Account).filter(Account.id == account_id).first()
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Account with ID {account_id} not found"
        )
    
    try:
        if account_data.name is not None:
            account.name = account_data.name
        if account_data.email is not None:
            account.email = account_data.email
        
        db.commit()
        db.refresh(account)
        return account
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists"
        )
