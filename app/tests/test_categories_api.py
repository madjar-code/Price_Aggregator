from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from uuid import uuid4

from app.models.category import Category

BASE_URL = "/api/v1/categories"


def test_create_category(client: TestClient):
    category_data = {
        'name': 'Test Category'
    }
    response = client.post(f'{BASE_URL}/', json=category_data)
    assert response.status_code == 200
    assert response.json()['name'] == category_data['name']
    assert 'id' in response.json()


def test_create_category_empty_body_invalid(client: TestClient):
    category_data = dict()
    response = client.post(f'{BASE_URL}/', json=category_data)
    assert response.status_code == 422


def test_create_category_empty_name_invalid(client: TestClient):
    category_data = {
        'name': ''
    }
    response = client.post(f'{BASE_URL}/', json=category_data)
    assert response.status_code == 422


def test_read_category(client: TestClient, db_session: Session):
    category = Category(id=uuid4(), name='Test Category')
    db_session.add(category)
    db_session.commit()
    db_session.refresh(category)

    response = client.get(f'{BASE_URL}/{category.id}')
    assert response.status_code == 200
    assert response.json()['name'] == category.name


def test_read_category_not_found_invalid(client: TestClient):
    response = client.get(f'{BASE_URL}/{uuid4()}')
    assert response.status_code == 404
    assert response.json() == {'detail': 'Category not found'}


def test_read_category_incorrect_id_invalid(client: TestClient):
    incorrect_id: str = str(uuid4())[:-2]
    response = client.get(f'{BASE_URL}/{incorrect_id}')
    assert response.status_code == 422
    assert type(response.json()) == dict


def test_read_categories(client: TestClient, db_session: Session):
    categories = [
        Category(id=uuid4(), name='Test Category 1'),
        Category(id=uuid4(), name='Test Category 2'),
    ]
    db_session.add_all(categories)
    db_session.commit()

    response = client.get(BASE_URL)
    assert response.status_code == 200
    assert len(response.json()) == len(categories)
    assert response.json()[0]['name'] == categories[0].name
    assert response.json()[1]['name'] == categories[1].name
