# Kohyli E-Commerce Platform - Architecture Documentation

## Overview
Kohyli is a full-stack e-commerce bookstore application with a Python/FastAPI backend and TypeScript/React frontend.

## Backend Architecture

### Technology Stack
- **Framework**: FastAPI (Python 3.11+)
- **Database**: SQLite with SQLModel ORM (async via aiosqlite)
- **Authentication**: JWT tokens with bcrypt password hashing
- **Caching/Queue**: Redis (for token blacklist and background tasks)
- **Background Jobs**: arq (Redis-based async task queue)
- **Email**: aiosmtplib for SMTP email sending
- **Testing**: pytest with pytest-asyncio
- **Package Manager**: uv

### Project Structure
```
backend/
├── app/
│   ├── api/                  # API layer
│   │   ├── routers/         # Route handlers
│   │   └── schemas/         # Pydantic DTOs
│   ├── core/                # Core utilities (security)
│   ├── database/            # Database models and session management
│   │   ├── models.py       # SQLModel table definitions
│   │   ├── session.py      # Async database session
│   │   └── redis.py        # Redis connection for token blacklist
│   ├── services/           # Business logic layer
│   │   ├── authors.py
│   │   ├── books.py
│   │   ├── orders.py
│   │   ├── users.py
│   │   ├── email.py        # Email template generation
│   │   └── tasks.py        # Background task definitions
│   ├── migrations/         # Alembic database migrations
│   └── tests/              # Test suite
├── worker.py               # Background worker process
└── pyproject.toml          # Dependencies and project metadata
```

### Key Design Patterns

#### Service Layer Pattern
Business logic is encapsulated in service classes (e.g., `OrdersService`, `UsersService`):
- Services receive database session via dependency injection
- Each service handles CRUD operations and domain logic for its entity
- Services are injected into route handlers using FastAPI's `Depends()`

Example:
```python
class OrdersService:
    def __init__(self, session: SessionDep):
        self._session = session
    
    async def create(self, user_id: int, elements: List[dict]) -> Order:
        # Business logic here
        pass

# Dependency injection
OrdersServiceDep = Annotated[OrdersService, Depends(get_orders_service)]
```

#### Async/Await Throughout
- All database operations are async
- Email sending is async
- Background tasks use async workers

#### Background Task Processing
- **Pattern**: Enqueue tasks to avoid blocking HTTP requests
- **Implementation**: arq with Redis as message broker
- **Use Case**: Order confirmation emails sent asynchronously after order creation
- **Graceful Degradation**: Email failures don't block order creation

### Database Models

Key entities:
- **User**: Customer accounts with email authentication
- **Author**: Book authors with biography
- **Book**: Products with pricing, stock, ISBN
- **Order**: Customer purchases with status tracking
- **OrderItem**: Junction table for order line items (with price snapshot)
- **Review**: Book reviews with ratings

### Configuration Management
- Uses `pydantic-settings` for environment-based configuration
- Settings classes: `JWTSettings`, `DatabaseSettings`, `EmailSettings`
- Loads from `.env` file with sensible defaults

### Testing Strategy
- **Unit Tests**: Service layer logic in isolation
- **Integration Tests**: Full workflow tests with in-memory SQLite
- **Fixtures**: Pytest async fixtures for database setup
- **Mocking**: Used for external dependencies (email sending, Redis)

### Common Commands
```bash
# Development
just run-dev              # Start FastAPI with hot-reload
python worker.py          # Start background task worker

# Database
just migration-gen <name> # Generate new migration
just migration-up-head    # Apply migrations

# Testing
just test                 # Run pytest suite
just test-api            # Run hurl API tests

# Code Quality
just format              # Format with ruff
```

## Frontend Architecture

### Technology Stack
- **Framework**: React with TypeScript
- **Build Tool**: Vite
- **Styling**: Tailwind CSS
- **Package Manager**: npm

### Integration Points
- Frontend makes API calls to backend at `http://localhost:8000`
- CORS configured to allow `localhost:5173` (dev) and `localhost:4173` (preview)

## Key Implementation Notes

### Order Creation Flow
1. Client sends order request with book IDs and quantities
2. Backend validates user exists and books are in stock
3. Stock quantities are decremented atomically
4. Order and OrderItems are created in transaction
5. Email confirmation task is enqueued (non-blocking)
6. Order response returned to client
7. Background worker processes email task asynchronously

### Email System
- **SMTP Configuration**: Via environment variables
- **Template Format**: HTML + plain text multipart emails
- **Graceful Handling**: Missing SMTP credentials log warning but don't fail orders
- **Testing**: Can use MailHog or Mailtrap for local testing

### Authentication
- JWT tokens stored in cookies
- Token blacklist in Redis for logout functionality
- Passwords hashed with bcrypt

### Stock Management
- Stock decremented during order creation
- Insufficient stock returns 400 error
- Stock changes are part of order transaction (atomic)

## Development Workflow

1. **Database Changes**: Generate migration → Review → Apply
2. **New Features**: Write tests first → Implement service logic → Add routes
3. **Code Style**: Auto-format with `uv format` before commit
4. **Testing**: Run relevant test subset during development, full suite before PR

## Dependencies Management

### Critical Version Constraints
- `redis[hiredis]>=4.2.0,<6.0.0` (arq requires <6)
- `arq>=0.26.0` (background task queue)
- Python 3.11+ required

### Adding Dependencies
1. Add to `pyproject.toml`
2. Run `uv sync`
3. Check for security vulnerabilities
4. Update lock file committed to git

## Future Considerations

### Potential Improvements
- [ ] Add email retry logic with exponential backoff
- [ ] Implement email delivery status tracking
- [ ] Add order status change notifications
- [ ] Support multiple email templates (shipping, cancellation)
- [ ] Add email preferences to user model
- [ ] Implement rate limiting for email sending
- [ ] Add monitoring/metrics for background tasks

### Scaling Considerations
- Redis already in place for distributed caching/queuing
- Service layer ready for extraction to microservices
- Async architecture supports high concurrency
- Consider PostgreSQL for production (already using async SQLModel)
