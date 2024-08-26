from uuid import uuid4
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.models.product import Product
from app.models.info_resource import InfoResource, ResourceState

BASE_URL = 'api/v1/resources'

EXAMPLE_URL = 'https://example.com/'


def test_create_resource(
    client: TestClient,
    # db_session: Session,
    test_product: Product
):
    # product = Product(name='Test Product')
    # db_session.add(product)
    # db_session.commit()
    # db_session.refresh(product)
    resource_data = {
        'url': EXAMPLE_URL,
        'state': ResourceState.ACTIVE.value,
        'name': 'Resource Name',
        'product_id': str(test_product.id),
    }
    response = client.post(f'{BASE_URL}', json=resource_data)
    assert response.status_code == 200
    assert response.json()['url'] == resource_data['url']
    assert 'id' in response.json()


def test_create_resource_empty_name(
    client: TestClient,
    test_product: Product,
    # db_session: Session
):
    # product = Product(name='Test Product')
    # db_session.add(product)
    # db_session.commit()
    # db_session.refresh(product)
    resource_data = {
        'url': EXAMPLE_URL,
        'state': ResourceState.ACTIVE.value,
        'name': '',
        'product_id': str(test_product.id),
    }
    response = client.post(f'{BASE_URL}', json=resource_data)
    assert response.status_code == 200
    assert response.json()['url'] == resource_data['url']
    assert 'id' in response.json()


def test_create_resource_no_product_id_invalid(client: TestClient):
    resource_data = {
        'url': EXAMPLE_URL,
        'state': ResourceState.ACTIVE.value,
        'name': 'Resource Name',
        # 'product_id': str(product.id),
    }
    response = client.post(f'{BASE_URL}', json=resource_data)
    assert response.status_code == 422


def test_create_resource_incorrect_state_invalid(
    client: TestClient,
    # db_session: Session
    test_product: Product,
):
    # product = Product(name='Test Product')
    # db_session.add(product)
    # db_session.commit()
    # db_session.refresh(product)
    resource_data = {
        'url': EXAMPLE_URL,
        'state': ResourceState.ACTIVE.value[:-2],
        'name': 'Resource Name',
        'product_id': str(test_product.id),
    }
    response = client.post(f'{BASE_URL}', json=resource_data)
    assert response.status_code == 422


def test_create_resource_incorrect_product_id_invalid(
    client: TestClient,
):
    resource_data = {
        'url': EXAMPLE_URL,
        'state': ResourceState.ACTIVE.value,
        'name': 'Resource Name',
        'product_id': str(uuid4()),
    }
    response = client.post(f'{BASE_URL}', json=resource_data)
    assert response.status_code == 404
    assert response.json() == {'detail': 'Product not found'}


def test_create_resource_incorrect_url_invalid(
    client: TestClient,
):
    # First of all, my validator notices format problems
    # And I able to use random UUID for product_id field
    resorce_data = {
        'url': EXAMPLE_URL[2:],
        'state': ResourceState.ACTIVE.value,
        'name': 'Resource Name',
        'product_id': str(uuid4())
    }
    response = client.post(f'{BASE_URL}', json=resorce_data)
    assert response.status_code == 422
