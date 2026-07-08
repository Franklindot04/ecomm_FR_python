# Ecommerce Microservice API

A learning-oriented ecommerce microservice built with FastAPI, SQLite, and SQLAlchemy.

The project is being developed incrementally through milestone-based stages, gradually evolving from a simple MVP into a more realistic ecommerce backend while keeping the codebase clean, documented, and easy to extend.

---

## Features

### Products API
- Create products.
- Retrieve all products.
- Retrieve a single product.
- Pydantic validation.
- Seeded demo inventory.

### Shopping Cart API
- Add products to cart.
- Merge duplicate cart items.
- View cart contents.
- Remove individual items.
- Clear entire cart.
- Validate stock availability.

### Orders API
- Checkout cart items.
- Validate stock during checkout.
- Create order records and order items.
- Persist order history.
- Decrement inventory.
- Clear cart after purchase.
- Retrieve all orders.
- Retrieve individual orders.
- Nested serialization using eager loading.

### Order Lifecycle API
- Order status support.
- Status transitions.
- Order cancellation rules.
- State-machine style workflow validation.
- Swagger-visible status fields.

### Authentication API
- User registration.
- User login.
- JWT access tokens.
- Password hashing with bcrypt.
- Protected user route.
- Swagger OAuth2 password flow.

### Multi-user Ecommerce API
- User-owned cart items.
- User-owned orders.
- User-scoped cart access.
- User-scoped order access.
- Per-user checkout flow.
- Ownership protection for order retrieval and updates.
- Protected cart and order endpoints.

### Architecture Improvements
- Service-layer extraction for cart logic.
- Service-layer extraction for order logic.
- Thinner route handlers.
- Cleaner separation of concerns.
- Improved maintainability for future scaling.
- Preserved existing API behavior after refactor.

### Infrastructure
- SQLite database.
- SQLAlchemy ORM.
- Pydantic schemas.
- Dependency injection.
- Seed initialization.
- Swagger/OpenAPI documentation.

Swagger UI available at:

```text
/docs
```

---

## Status

### Completed Milestones

✅ Stage 1 — FastAPI Base Setup  
Completed: 2026-06-18

Implemented:
- FastAPI application.
- SQLite database.
- SQLAlchemy setup.
- Database session dependency.
- Health endpoint.
- Seed mechanism.
- Swagger documentation.

---

✅ Stage 2 — Products API  
Completed: 2026-06-19

Implemented:
- Product model.
- CRUD operations.
- Validation schemas.
- Seeded demo products.

---

✅ Stage 3 — Cart System  
Completed: 2026-06-20

Implemented:
- Add to cart.
- Merge duplicate items.
- View cart.
- Remove item.
- Clear cart.
- Stock validation.

---

✅ Stage 4 — Orders System and Router Refactor  
Completed: 2026-06-26

Implemented:
- Checkout endpoint.
- Order creation.
- Order items.
- Inventory decrement.
- Empty cart after checkout.
- Nested serialization.
- Eager loading.
- Router modularization.
- Products router.
- Cart router.
- Orders router.
- Reduced `main.py` complexity.
- Preserved existing API behavior.
- Preserved OpenAPI compatibility.

---

✅ Stage 5 — Order Lifecycle Management  
Completed: 2026-06-29

Implemented:
- Order status support.
- `PENDING`, `PAID`, `PROCESSING`, `SHIPPED`, `DELIVERED`, `CANCELLED` statuses.
- `PATCH /orders/{id}/status`.
- `POST /orders/{id}/cancel`.
- Transition validation.
- Cancellation rules.
- Swagger verification of order status workflow.

---

✅ Stage 6 — Authentication  
Completed: 2026-07-03

Implemented:
- User model.
- User registration.
- User login.
- Password hashing.
- JWT token generation.
- OAuth2 password flow in Swagger.
- Protected route: `GET /auth/me`.
- Token-based user lookup.

---

✅ Stage 7 — Multi-user Ecommerce  
Completed: 2026-07-07

Implemented:
- User ownership for cart items.
- User ownership for orders.
- Authenticated cart endpoints.
- Authenticated order endpoints.
- User-scoped cart queries.
- User-scoped order queries.
- Per-user checkout behavior.
- Ownership checks for order access and modification.
- Swagger-documented 404 responses for inaccessible orders.

---

✅ Stage 8 — Architecture Refactor  
Completed: 2026-07-08

Implemented:
- Service-layer extraction for cart logic.
- Service-layer extraction for order logic.
- `app/services/cart_service.py`.
- `app/services/order_service.py`.
- Thinner API route handlers.
- Cleaner separation between routing and business logic.
- Preserved Swagger behavior.
- Preserved multi-user ownership isolation.
- Improved maintainability and extensibility.

---

## Current Architecture

### Application

```text
app/
├── api/                    # API route handlers
│   ├── __init__.py
│   ├── auth.py             # Authentication endpoints
│   ├── products.py         # Product endpoints
│   ├── cart.py             # User-scoped cart endpoints
│   └── orders.py           # User-scoped order endpoints
├── services/               # Business logic layer
│   ├── __init__.py
│   ├── cart_service.py     # Cart business logic
│   └── order_service.py    # Order business logic
├── auth_utils.py           # Password hashing, JWT, auth dependency
├── database.py             # Database connection/session setup
├── main.py                 # FastAPI application entry point
├── models.py               # SQLAlchemy models
├── schemas.py              # Pydantic schemas
└── seed.py                 # Seed initial product data
```

### Root Files

```text
requirements.txt        # Python dependencies
ecommerce.db            # SQLite database (dev only)
README.md               # Project documentation
```

The router modularization was introduced after Stage 4, and the service layer was added in Stage 8 to further improve maintainability, separation of concerns, and future scalability [web:617][web:612].

---

## Development Roadmap

| Stage | Description | Status |
| --- | --- | --- |
| 1 | FastAPI Setup | ✅ |
| 2 | Products API | ✅ |
| 3 | Cart System | ✅ |
| 4 | Orders System and Router Refactor | ✅ |
| 5 | Order Lifecycle Management | ✅ |
| 6 | Authentication | ✅ |
| 7 | Multi-user Ecommerce | ✅ |
| 8 | Architecture Refactor | ✅ |
| 9 | Alembic | 🚧 |
| 10 | Testing | 🚧 |
| 11 | Docker | 🚧 |
| 12 | Caching | 🚧 |
| 13 | Background Tasks | 🚧 |
| 14 | Mock Payments | 🚧 |
| 15 | Production Readiness | 🚧 |

---

## Next Milestone

### Stage 9 — Alembic

Planned focus:
- Introduce database migrations.
- Replace manual schema evolution.
- Track model changes safely.
- Improve developer workflow for database updates.
- Prepare the project for more realistic schema changes.

Skills expected:
- Alembic migrations.
- SQLAlchemy schema evolution.
- Migration workflow management.
- Database version control.

---

## Last Updated

2026-07-08 – completed architecture refactor (Stage 8)

2026-07-07 – completed multi-user ecommerce (Stage 7)

2026-07-03 – completed Authentication (Stage 6)

2026-06-30 – completed order lifecycle management (Stage 5)

2026-06-26 – completed orders system and router refactor (Stage 4)

2026-06-20 – completed Cart System (Stage 3)

2026-06-19 – completed Products API (Stage 2)

2026-06-18 – completed FastAPI Base Setup (Stage 1)

---

## Tech Stack

- Python.
- FastAPI.
- SQLite.
- SQLAlchemy.
- Pydantic.
- Dependency injection.
- JWT.
- OAuth2 password flow.
- Password hashing.
- Swagger/OpenAPI.
- Service-layer architecture.