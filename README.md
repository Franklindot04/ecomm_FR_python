# Ecommerce Microservice API

A learning-oriented ecommerce microservice built with FastAPI, SQLite, and SQLAlchemy.

The project is being developed incrementally through milestone-based stages, gradually evolving from a simple MVP into a more realistic ecommerce backend while maintaining clean Git history and documented progression.

---

## Features

Current implementation includes:

### Products API

* Create products
* Retrieve all products
* Retrieve a single product
* Pydantic validation
* Seeded demo inventory

### Shopping Cart API

* Add products to cart
* Merge duplicate cart items
* View cart contents
* Remove individual items
* Clear entire cart
* Validate stock availability

### Orders API

* Checkout cart items
* Validate stock during checkout
* Create order records
* Create order items
* Persist order history
* Decrement inventory
* Clear cart after purchase
* Retrieve all orders
* Retrieve individual orders
* Nested serialization using eager loading

### Infrastructure

* SQLite database
* SQLAlchemy ORM
* Pydantic schemas
* Dependency injection
* Seed initialization
* Swagger/OpenAPI documentation

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

* FastAPI application
* SQLite database
* SQLAlchemy setup
* Database session dependency
* Health endpoint
* Seed mechanism
* Swagger documentation

---

✅ Stage 2 — Products API

Completed: 2026-06-19

Implemented:

* Product model
* CRUD operations
* Validation schemas
* Seeded demo products

---

✅ Stage 3 — Cart System

Completed: 2026-06-20

Implemented:

* Add to cart
* Merge duplicate items
* View cart
* Remove item
* Clear cart
* Stock validation

---

✅ Stage 4 — Orders System

Completed: 2026-06-21

Implemented:

* Checkout endpoint
* Order creation
* Order items
* Inventory decrement
* Empty cart after checkout
* Nested serialization
* Eager loading

---

✅ Post-Stage 4 Refactor

Completed: 2026-06-26

Implemented:

* Router modularization
* Products router
* Cart router
* Orders router
* Reduced `main.py` complexity
* Preserved existing API behavior
* Preserved OpenAPI compatibility

---

## Current Architecture

### Application

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

### Root Files

requirements.txt        # Python dependencies
ecommerce.db            # SQLite database (dev only)
README.md               # Project documentation

The router modularization was introduced after Stage 4 to improve maintainability and prepare for future architectural improvements.

---

## Development Roadmap

| Stage        | Description                | Status |
| ------------ | -------------------------- | ------ |
| 1            | FastAPI Setup              | ✅      |
| 2            | Products API               | ✅      |
| 3            | Cart System                | ✅      |
| 4            | Orders System              | ✅      |
| Post-Stage 4 | Router Modularization      | ✅      |
| 5            | Order Lifecycle Management | 🚧     |
| 6            | Authentication             | 🚧     |
| 7            | Multi-user Ecommerce       | 🚧     |
| 8            | Architecture Refactor      | 🚧     |
| 9            | Alembic                    | 🚧     |
| 10           | Testing                    | 🚧     |
| 11           | Docker                     | 🚧     |
| 12           | Caching                    | 🚧     |
| 13           | Background Tasks           | 🚧     |
| 14           | Mock Payments              | 🚧     |
| 15           | Production Readiness       | 🚧     |

---

## Next Milestone

### Stage 5 — Order Lifecycle Management

Planned order statuses

```text
PENDING
PAID
PROCESSING
SHIPPED
DELIVERED
CANCELLED
```

Planned endpoints

```text
GET    /orders
GET    /orders/{id}
PATCH  /orders/{id}/status
POST   /orders/{id}/cancel
```

Business rules

* Cannot ship cancelled orders
* Cannot cancel delivered orders
* Enforce valid state transitions
* Introduce order workflow management

Skills expected

* Enums
* State machines
* Workflow design
* Domain modeling

---

## Last Updated

```text
2026-06-26 – completed router modularization after Stage 4

2026-06-21 – completed Orders System (Stage 4)

2026-06-20 – completed Cart System (Stage 3)

2026-06-19 – completed Products API (Stage 2)

2026-06-18 – completed FastAPI Base Setup (Stage 1)
```

---

## Tech Stack

* Python
* FastAPI
* SQLite
* SQLAlchemy
* Pydantic

---

## License

Licensed under the MIT License.
