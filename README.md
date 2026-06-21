## Status

Stage 4 (Orders System) completed and validated via Swagger.
Stage 3 (Cart System) completed and merged into `main`.
Stage 2 (Products API) completed and merged into `main`.
Stage 1 (FastAPI Base Setup) completed and merged into `main`.

## Context

FastAPI-based ecommerce microservice using SQLite and SQLAlchemy.

### Current features

- Product CRUD API implemented

- Shopping Cart API implemented
  - Add items to cart with stock validation
  - Merge duplicate cart items
  - View cart contents with product details
  - Remove individual cart items
  - Clear entire cart

- Orders API implemented
  - Create orders from cart items
  - Validate stock availability during checkout
  - Generate order items
  - Persist order history
  - Decrement product inventory after purchase
  - Clear cart after successful checkout
  - Retrieve all orders
  - Retrieve a single order with nested product details
  - Stable nested serialization using eager loading

- Database integration (SQLite)
- Pydantic validation layer
- Seed data initialization
- Swagger/OpenAPI available via `/docs`

## Last Updated

2026-06-21 – completed Orders System (Stage 4), validated via Swagger and prepared for merge
2026-06-20 – completed Cart System (Stage 3) and merged into `main`
2026-06-19 – completed Products API (Stage 2) and merged into `main`
2026-06-18 – completed FastAPI base setup with database and health check (Stage 1)

