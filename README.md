# Ecommerce Microservice API

A learning-oriented ecommerce microservice built with FastAPI, SQLite, and SQLAlchemy.

The project is being developed incrementally through milestone-based stages, gradually evolving from a simple MVP into a more realistic ecommerce backend while keeping the codebase clean, documented, and easy to extend [web:191][web:193].

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

✅ Stage 4 — Orders System  
Completed: 2026-06-21

Implemented:
- Checkout endpoint.
- Order creation.
- Order items.
- Inventory decrement.
- Empty cart after checkout.
- Nested serialization.
- Eager loading.

---

✅ Post-Stage 4 Refactor  
Completed: 2026-06-26

Implemented:
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

## Current Architecture

### Application

```text
app/
├── api/                # API route handlers
│   ├── __init__.py
│   ├── products.py     # Product endpoints
│   ├── cart.py         # Cart endpoints
│   └── orders.py       # Order endpoints
├── database.py         # Database connection/session setup
├── main.py             # FastAPI application entry point
├── models.py           # SQLAlchemy models
├── schemas.py          # Pydantic schemas
└── seed.py             # Seed initial product data
```

### Root Files

```text
requirements.txt        # Python dependencies
ecommerce.db            # SQLite database (dev only)
README.md               # Project documentation
```

The router modularization was introduced after Stage 4 to improve maintainability and prepare for future architectural improvements.

---

## Development Roadmap

| Stage | Description | Status |
| --- | --- | --- |
| 1 | FastAPI Setup | ✅ |
| 2 | Products API | ✅ |
| 3 | Cart System | ✅ |
| 4 | Orders System | ✅ |
| Post-Stage 4 | Router Modularization | ✅ |
| 5 | Order Lifecycle Management | ✅ |
| 6 | Authentication | 🚧 |
| 7 | Multi-user Ecommerce | 🚧 |
| 8 | Architecture Refactor | 🚧 |
| 9 | Alembic | 🚧 |
| 10 | Testing | 🚧 |
| 11 | Docker | 🚧 |
| 12 | Caching | 🚧 |
| 13 | Background Tasks | 🚧 |
| 14 | Mock Payments | 🚧 |
| 15 | Production Readiness | 🚧 |

---

## Next Milestone

### Stage 6 — Authentication

Planned focus:
- User accounts.
- Login and registration.
- Protected endpoints.
- Cart and order ownership.
- Foundation for multi-user support.

Skills expected:
- Authentication.
- Password hashing.
- Token-based access.
- User-scoped data access.

---

## Last Updated

```text
2026-06-30 – completed Stage 5 order lifecycle management

2026-06-26 – completed router modularization after Stage 4

2026-06-21 – completed Orders System (Stage 4)

2026-06-20 – completed Cart System (Stage 3)

2026-06-19 – completed Products API (Stage 2)

2026-06-18 – completed FastAPI Base Setup (Stage 1)
```

---

## Tech Stack

- Python.
- FastAPI.
- SQLite.
- SQLAlchemy.
- Pydantic.

---

## License

Licensed under the MIT License.