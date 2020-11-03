import pytest

from database_crud import *
from models import Product, Producer


@pytest.fixture
def app():
    # This database URI specifies sqlite in memory database that will be discarded
    # Once we are done with testing
    app = create_app("sqlite://")
    db.create_all(app=app)
    return app


@pytest.fixture
def client(app):
    with app.test_client() as client:
        yield client


def populate_db():
    producer = Producer(id=1, name="Dell")
    db.session.add(Producer(id=2, name="Lenovo"))
    db.session.add(Product(id=1, name="Legion 7i", producer_id=2, quantity=5, description="gaming laptop", price=5000))
    db.session.add(Product(id=2, name="Vostro 3490 14''", quantity=2, producer=producer,
                           price=3000, description='to work'))


def test_add_producer_endpoint_returns_status_code_200_ok(client):
    response = client.post("/add_producer", json={"id": 3, "name": "HP"})
    assert response.status_code == 200
