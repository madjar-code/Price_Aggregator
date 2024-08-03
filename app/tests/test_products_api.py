import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from uuid import uuid4
from app.models.category import Category
from app.models.product import Product

BASE_URL = "/api/v1/products"


def test_create_product(client: TestClient, db_session: Session):
    category = Category(id=uuid4(), name="Test Category")
    db_session.add(category)
    db_session.commit()
    db_session.refresh(category)
    product_data = {
        'name': 'Test Product',
        'description': 'Test Description',
        'category_id': str(category.id)
    }
    response = client.post(f'{BASE_URL}/', json=product_data)
    assert response.status_code == 200
    assert response.json()['name'] == product_data['name']
    assert 'id' in response.json()


def test_create_product_invalid_category(client: TestClient):
    product_data = {
        'name': 'Test Product',
        'description': 'Test Description',
        'category_id': str(uuid4()),
    }
    response = client.post(f'{BASE_URL}/', json=product_data)
    assert response.status_code == 404
    assert response.json() == {'detail': 'Category not found'}


def test_create_product_empty_body_invalid(client: TestClient):
    product_data = dict()
    response = client.post(f'{BASE_URL}/', json=product_data)
    assert response.status_code == 422


def test_create_product_too_long_name_invalid(client: TestClient, db_session: Session):
    category = Category(id=uuid4(), name="Test Category")
    db_session.add(category)
    db_session.commit()
    db_session.refresh(category)

    product_data = {
        'name': 'a' * 51,
        'description': 'Test Description',
        'category_id': str(category.id)
    }

    response = client.post(f'{BASE_URL}/', json=product_data)
    assert response.status_code == 422


def test_read_product(client: TestClient, db_session: Session):
    category = Category(id=uuid4(), name="Test Category")
    product = Product(
        id=uuid4(),
        name='Test Product',
        description='Test Description',
        category_id=category.id
    )
    db_session.add_all([category, product])
    db_session.commit()
    db_session.refresh(product)

    response = client.get(f'{BASE_URL}/{product.id}')
    assert response.status_code == 200
    assert response.json()['name'] == product.name


def test_read_product_not_found(client: TestClient):
    response = client.get(f'{BASE_URL}/{uuid4()}')
    assert response.status_code == 404
    assert response.json() == {'detail': 'Product not found'}


def test_read_product_incorrect_id_invalid(client: TestClient):
    incorrect_id: str = str(uuid4())[:-2]
    response = client.get(f'{BASE_URL}/{incorrect_id}')
    assert response.status_code == 422
    assert type(response.json()) == dict


def test_read_products(client: TestClient, db_session: Session):
    products = [
        Product(name='Test Product 1'),
        Product(name='Test Product 2'),
    ]
    db_session.add_all(products)
    db_session.commit()

    response = client.get(BASE_URL)
    assert response.status_code == 200
    assert len(response.json()) == len(products)
    assert response.json()[1]['name'] == products[1].name
    assert response.json()[0]['description'] == products[0].description
