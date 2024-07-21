from app.database import init_db, SessionLocal
from app.models import Product, Category


def init_sample_data():
    db = SessionLocal()
    category = Category(name="Sample Category")
    db.add(category)
    db.commit()
    db.refresh(category)

    product = Product(
        name="Sample Product",
        price=10.0,
        category_id=category.id
    )
    db.add(product)
    db.commit()
    db.refresh(product)

    db.close()


if __name__ == "__main__":
    init_db()
    init_sample_data()
