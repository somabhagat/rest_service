# Agentic Payment REST Service (2026 Strategy)
## Visual Overview (Swagger UI)
![Agentic Commerce API Documentation](./Screenshot_is_agent.png)

*The interactive API documentation showcasing the `is_agent` logic for autonomous commerce and tokenized payment methods.*
This project is a technical deep-dive into the infrastructure required for the next wave of fintech: **Agentic Commerce** and **Network Tokenization**.

### Strategic Objectives
* **Agentic Permissioning:** Implemented `is_agent` logic to distinguish between human-initiated and AI-autonomous transactions.
* **Security & Tokenization:** Architecture focused on storing merchant-specific `token_id`s rather than raw card data.
* **Reliability (ACID):** Using PostgreSQL transaction blocks to ensure atomic "all-or-nothing" money movement—critical for financial integrity.

### Tech Stack
* **FastAPI:** Modern, high-performance Python framework.
* **PostgreSQL:** Reliable relational storage with strict ACID compliance.
* **Docker:** Containerized environment for consistent deployment.

# Payment REST Service

A modern Python FastAPI REST service with PostgreSQL supporting **2026 payment trends**: Agentic Commerce and Network Tokenization.

## 🌟 Features

### 2026 Payment Trends
- **Agentic Commerce**: AI agents making autonomous purchases within pre-defined budgets
- **Network Tokenization**: Merchant-specific tokens replacing raw credit card numbers
- **Instant Payments**: Real-time transaction status tracking (Pending, Completed, Failed)

### Technical Features
- **ACID Transaction Guarantees**: Pessimistic locking ensures atomic money transfers
- **RESTful API**: Clean CRUD operations for accounts, payment methods, and transactions
- **Automatic Validation**: Pydantic schemas for type-safe request/response handling
- **Interactive Documentation**: Auto-generated Swagger UI and ReDoc

---

## 📋 Prerequisites

- **Python 3.11+**
- **Docker** (for PostgreSQL)
- **pip** (Python package manager)

---

## 🚀 Quick Start

### 1. Navigate to Project Directory

```powershell
cd c:\development_projects\git\rest_service
```

### 2. Set Up Environment Variables

The `.env` file is already created with default values. Update if needed:

```env
POSTGRES_USER=payment_user
POSTGRES_PASSWORD=your_secure_password_here
POSTGRES_DB=payment_db
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
DATABASE_URL=postgresql://payment_user:your_secure_password_here@localhost:5432/payment_db
```

### 3. Create Python Virtual Environment (One-time setup)

```powershell
py -3.11 -m venv .venv
```

This creates a `.venv` folder in your project for isolated dependencies.

### 4. Activate Virtual Environment (Every time you open a new terminal)

```powershell
.\.venv\Scripts\Activate.ps1
```

> [!TIP]
> You'll see `(.venv)` at the start of your prompt when activated.

### 5. Install Python Dependencies

```powershell
python -m pip install -r requirements.txt
```

### 6. Start PostgreSQL with Docker

```powershell
docker-compose up -d
```

Verify the container is running:

```powershell
docker-compose ps
```

### 7. Run the FastAPI Server

```powershell
python -m uvicorn app.main:app --reload
```

The server will start at: **http://localhost:8000**

---

## 📚 API Documentation

Once the server is running, access the interactive API documentation:

- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 🗄️ Database Schema

### Tables

```mermaid
erDiagram
    accounts ||--o{ payment_methods : has
    accounts ||--o{ transactions : sends
    accounts ||--o{ transactions : receives
    
    accounts {
        uuid id PK
        string name
        string email UK
        decimal balance
        boolean is_agent
        datetime created_at
        datetime updated_at
    }
    
    payment_methods {
        uuid id PK
        uuid account_id FK
        string method_type
        string token_id UK
        boolean is_active
        datetime created_at
    }
    
    transactions {
        uuid id PK
        uuid from_account_id FK
        uuid to_account_id FK
        decimal amount
        string status
        string description
        datetime created_at
        datetime completed_at
    }
```

---

## 🔌 API Endpoints

### Accounts

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/accounts` | Create a new account (user or AI agent) |
| `GET` | `/accounts/{id}` | Get account details including balance |
| `GET` | `/accounts` | List all accounts (with pagination) |
| `PATCH` | `/accounts/{id}` | Update account name or email |

### Payment Methods

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/methods` | Add a tokenized payment method |
| `GET` | `/methods/{id}` | Get payment method details |
| `GET` | `/methods/account/{account_id}` | List all methods for an account |

### Transactions

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/transactions` | Execute a money transfer (ACID-compliant) |
| `GET` | `/transactions/{id}` | Get transaction details |
| `GET` | `/transactions/account/{account_id}` | Get transaction history for an account |

---

## 💡 Usage Examples

### Create an AI Agent Account

```bash
curl -X POST "http://localhost:8000/accounts" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Shopping AI Agent",
    "email": "agent@example.com",
    "is_agent": true,
    "initial_balance": 1000.00
  }'
```

### Add a Tokenized Payment Method

```bash
curl -X POST "http://localhost:8000/methods" \
  -H "Content-Type: application/json" \
  -d '{
    "account_id": "<account_id_from_previous_step>",
    "method_type": "Apple Pay",
    "token_id": "tok_1234567890abcdef"
  }'
```

### Execute a Transaction (ACID-Compliant)

```bash
curl -X POST "http://localhost:8000/transactions" \
  -H "Content-Type: application/json" \
  -d '{
    "from_account_id": "<source_account_id>",
    "to_account_id": "<destination_account_id>",
    "amount": 50.00,
    "description": "Payment for services"
  }'
```

**ACID Guarantees:**
- If the source account has insufficient balance, the transaction fails and no changes are made
- Both accounts are locked during the transfer to prevent race conditions
- All changes (balance updates + transaction record) are committed atomically

---

## 🧪 Testing the ACID Transaction Logic

### Test 1: Insufficient Balance

1. Create two accounts:
   - Account A: $100 balance
   - Account B: $0 balance

2. Attempt to transfer $150 from A to B

**Expected Result:**
- Transaction status: `Failed`
- Account A balance: Still $100 (unchanged)
- Account B balance: Still $0 (unchanged)

### Test 2: Successful Transfer

1. Transfer $50 from Account A to Account B

**Expected Result:**
- Transaction status: `Completed`
- Account A balance: $50 (decreased)
- Account B balance: $50 (increased)

---

## 🏗️ Project Structure

```
c:\development_projects\git\rest_service\
├── .venv/                         # Virtual environment (gitignored)
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI application entry point
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py              # Environment configuration
│   │   └── database.py            # SQLAlchemy setup
│   ├── models/
│   │   ├── __init__.py
│   │   ├── account.py             # Account model (Agentic Commerce)
│   │   ├── payment_method.py      # PaymentMethod model (Tokenization)
│   │   └── transaction.py         # Transaction model (Instant Payments)
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── account.py             # Account Pydantic schemas
│   │   ├── payment_method.py      # PaymentMethod Pydantic schemas
│   │   └── transaction.py         # Transaction Pydantic schemas
│   └── api/
│       ├── __init__.py
│       ├── accounts.py            # Account endpoints
│       ├── payment_methods.py     # PaymentMethod endpoints
│       └── transactions.py        # Transaction endpoints (ACID logic)
├── .env                           # Environment variables (gitignored)
├── .gitignore
├── requirements.txt               # Python dependencies
├── docker-compose.yml             # PostgreSQL container
└── README.md
```

---

## 🔒 Security Notes

### Production Recommendations

1. **Environment Variables**:
   - Never commit `.env` to version control
   - Use strong passwords for PostgreSQL
   - Consider using environment-specific configs

2. **CORS**:
   - Update `allow_origins` in `main.py` to specific domains
   - Remove `"*"` wildcard in production

3. **Database**:
   - Enable SSL for PostgreSQL connections
   - Use connection pooling for better performance
   - Implement database backups

4. **API**:
   - Add authentication (OAuth2, JWT)
   - Implement rate limiting
   - Add request ID tracing

---

## 🛠️ Development

### Activating Virtual Environment

Remember to activate your virtual environment every time you open a new terminal:

```powershell
.\.venv\Scripts\Activate.ps1
```

### Running Tests

```powershell
# Install test dependencies (with venv activated)
python -m pip install pytest pytest-asyncio httpx

# Run tests (when implemented)
pytest
```

### Database Migrations

For production, consider using **Alembic** for schema migrations:

```powershell
python -m pip install alembic
alembic init migrations
```

### Stopping the Service

```powershell
# Stop FastAPI server: Ctrl+C in terminal

# Stop PostgreSQL container:
docker-compose down

# Stop and remove data:
docker-compose down -v
```

---

## 📖 2026 Payment Trends Explained

### Agentic Commerce
AI agents autonomously make purchases within pre-defined budgets. The `is_agent` field in the `accounts` table identifies these AI-driven accounts.

### Network Tokenization
Instead of storing raw credit card numbers, the system stores merchant-specific tokens (`token_id`). This enhances security and compliance with payment standards.

### Instant Payments
Real-time status tracking (`Pending`, `Completed`, `Failed`) enables immediate payment confirmation and supports modern instant payment rails.

---

## 📝 License

This project is for educational purposes.

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

---

## 📧 Support

For questions or issues, please open an issue on the repository.
