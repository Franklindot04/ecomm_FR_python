## Status

Stage 3 (Cart System) completed and merged into `main`.  
Stage 2 (Products API) completed.

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
- Database integration (SQLite)
- Pydantic validation layer
- Seed data initialization
- Swagger/OpenAPI available via `/docs`

## Last Updated

2026-06-20 – completed Cart System (Stage 3) and merged into `main`
2026-06-18 – completed Products API (Stage 2) and pushed to feature branch + main merge