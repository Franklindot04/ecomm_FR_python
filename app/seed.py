from app.database import SessionLocal
from app.models import Product


def seed_products():
    db = SessionLocal()

    if db.query(Product).count() > 0:
        db.close()
        return

    products = [
        Product(name="Keyboard", description="Mechanical keyboard", price=50, stock=10),
        Product(name="Mouse", description="Wireless mouse", price=25, stock=20),
        Product(name="Monitor", description="24 inch display", price=150, stock=5),
    ]

    db.add_all(products)
    db.commit()
    db.close()