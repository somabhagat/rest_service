"""
Transaction API endpoints.
Provides operations for creating and tracking money transfers with ACID guarantees.
"""
from datetime import datetime
from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.core.database import get_db
from app.models.account import Account
from app.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate, TransactionResponse

router = APIRouter(prefix="/transactions", tags=["Transactions"])


@router.post("/", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
def create_transaction(transaction_data: TransactionCreate, db: Session = Depends(get_db)):
    """
    Execute a money transfer between accounts with ACID transaction guarantees.
    
    2026 Feature: Instant Payments with status tracking
    
    ACID Transaction Flow:
    1. Begin database transaction
    2. Lock source account (SELECT FOR UPDATE)
    3. Validate sufficient balance
    4. Deduct from source account
    5. Credit destination account
    6. Create transaction record with status="Completed"
    7. Commit all changes atomically
    8. On any failure: rollback entire transaction, set status="Failed"
    """
    # Validate source and destination are different
    if transaction_data.from_account_id == transaction_data.to_account_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Source and destination accounts must be different"
        )
    
    try:
        # Begin transaction (automatic with SQLAlchemy session)
        # Step 1: Lock source account row to prevent race conditions
        from_account = db.query(Account).filter(
            Account.id == transaction_data.from_account_id
        ).with_for_update().first()
        
        if not from_account:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Source account {transaction_data.from_account_id} not found"
            )
        
        # Step 2: Validate destination account exists
        to_account = db.query(Account).filter(
            Account.id == transaction_data.to_account_id
        ).with_for_update().first()
        
        if not to_account:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Destination account {transaction_data.to_account_id} not found"
            )
        
        # Step 3: Check sufficient balance
        if from_account.balance < transaction_data.amount:
            # Create failed transaction record
            failed_transaction = Transaction(
                from_account_id=transaction_data.from_account_id,
                to_account_id=transaction_data.to_account_id,
                amount=transaction_data.amount,
                description=transaction_data.description,
                status="Failed",
                completed_at=datetime.utcnow()
            )
            db.add(failed_transaction)
            db.commit()
            db.refresh(failed_transaction)
            
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Insufficient balance. Available: {from_account.balance}, Required: {transaction_data.amount}"
            )
        
        # Step 4: Deduct from source account
        from_account.balance -= transaction_data.amount
        
        # Step 5: Credit destination account
        to_account.balance += transaction_data.amount
        
        # Step 6: Create transaction record with "Completed" status
        new_transaction = Transaction(
            from_account_id=transaction_data.from_account_id,
            to_account_id=transaction_data.to_account_id,
            amount=transaction_data.amount,
            description=transaction_data.description,
            status="Completed",
            completed_at=datetime.utcnow()
        )
        db.add(new_transaction)
        
        # Step 7: Commit all changes atomically
        db.commit()
        db.refresh(new_transaction)
        
        return new_transaction
        
    except HTTPException:
        # Re-raise HTTP exceptions (validation errors)
        raise
    except SQLAlchemyError as e:
        # Database error - rollback transaction
        db.rollback()
        
        # Try to create failed transaction record
        try:
            failed_transaction = Transaction(
                from_account_id=transaction_data.from_account_id,
                to_account_id=transaction_data.to_account_id,
                amount=transaction_data.amount,
                description=transaction_data.description,
                status="Failed",
                completed_at=datetime.utcnow()
            )
            db.add(failed_transaction)
            db.commit()
        except:
            pass  # If we can't log the failure, continue with error response
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Transaction failed due to database error: {str(e)}"
        )


@router.get("/{transaction_id}", response_model=TransactionResponse)
def get_transaction(transaction_id: UUID, db: Session = Depends(get_db)):
    """
    Retrieve transaction details by ID.
    """
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Transaction with ID {transaction_id} not found"
        )
    return transaction


@router.get("/account/{account_id}", response_model=List[TransactionResponse])
def list_account_transactions(account_id: UUID, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    List all transactions for a specific account (sent or received).
    """
    # Validate account exists
    account = db.query(Account).filter(Account.id == account_id).first()
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Account with ID {account_id} not found"
        )
    
    transactions = db.query(Transaction).filter(
        (Transaction.from_account_id == account_id) | (Transaction.to_account_id == account_id)
    ).offset(skip).limit(limit).all()
    
    return transactions
