"""
FastAPI Payment REST Service
Main application entry point.

2026 Payment Trends:
- Agentic Commerce: AI agents making autonomous purchases
- Network Tokenization: Storing tokens instead of raw card numbers
- Instant Payments: Real-time transaction status tracking
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import engine, Base
from app.api import accounts_router, payment_methods_router, transactions_router

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI application
app = FastAPI(
    title="Payment REST Service",
    description="Modern payment API supporting Agentic Commerce and Network Tokenization",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API routers
app.include_router(accounts_router)
app.include_router(payment_methods_router)
app.include_router(transactions_router)


@app.get("/", tags=["Health"])
def health_check():
    """
    Health check endpoint to verify the service is running.
    """
    return {
        "status": "healthy",
        "service": "Payment REST Service",
        "version": "1.0.0",
        "features": [
            "Agentic Commerce (AI Agent Accounts)",
            "Network Tokenization",
            "ACID Transaction Guarantees"
        ]
    }


@app.on_event("startup")
async def startup_event():
    """
    Startup event handler.
    Database tables are created automatically via Base.metadata.create_all()
    """
    print("🚀 Payment REST Service starting...")
    print("📊 Database tables created/verified")
    print("🔗 API documentation available at: http://localhost:8000/docs")


@app.on_event("shutdown")
async def shutdown_event():
    """
    Shutdown event handler.
    """
    print("👋 Payment REST Service shutting down...")
