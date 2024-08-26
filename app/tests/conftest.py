import os
from typing import Any, Generator

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.product import Product
from app.models.info_resource import (
    InfoResource,
    ResourceState
)
from app.config.database import get_db, Base
from app.main import app

SQLALCHEMY_DATABASE_URL = os.getenv('TEST_DATABASE_URL', 'sqlite://')

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={'check_same_thread': False}
)

Session = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


@pytest.fixture(autouse=True)
def setup_db() -> Generator[FastAPI, Any, None]:
    """
    Create a fresh database on each test case.
    """
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


@pytest.fixture
def db_session() -> Generator[Session, Any, None]:
    """
    Creates a fresh SQLAlchemy session for each test that operates in a
    transaction. The transaction is rolled back at the end of each test ensuring
    a clean state.
    """
    connection = engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture()
def client(db_session: Session) -> Generator[TestClient, Any, None]:
    """
    Create a new FastAPI TestClient that uses the `db_session` fixture to override
    the `get_db` dependency that is injected into routes.
    """
    def _get_test_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = _get_test_db
    with TestClient(app) as client:
        yield client


@pytest.fixture
def test_product(db_session: Session) -> Product:
    """
    Fixture to create a test product in the database.
    """
    product = Product(name='Test Product')
    db_session.add(product)
    db_session.commit()
    db_session.refresh(product)
    return product


@pytest.fixture
def test_resource(
    db_session: Session,
    test_product: Product
) -> InfoResource:
    """
    Fixture to create a test info resource linked
    to the test product in the database.
    """
    resource = InfoResource(
        url='https://example.com',
        state=ResourceState.ACTIVE,
        name='Test Resource',
        product_id=test_product.id
    )
    db_session.add(resource)
    db_session.commit()
    db_session.refresh(resource)
    return resource
