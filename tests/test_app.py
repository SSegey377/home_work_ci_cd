import pytest
from app import create_app, db as _db
from app.factories import ClientFactory, ParkingFactory


@pytest.fixture(scope='module')
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"
    })
    with app.app_context():
        _db.create_all()
    yield app
    with app.app_context():
        _db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


def test_create_client(client):
    # Используем ClientFactory для создания клиента
    client_data = ClientFactory()
    response = client.post('/clients', json={
        'name': client_data.name,
        'surname': client_data.surname,
        'credit_card': client_data.credit_card,
        'car_number': client_data.car_number
    })
    assert response.status_code == 201
    assert 'id' in response.get_json()


def test_create_parking(client):
    # Используем ParkingFactory для создания парковки
    parking_data = ParkingFactory()
    response = client.post('/parkings', json={
        'address': parking_data.address,
        'opened': parking_data.opened,
        'count_places': parking_data.count_places
    })
    assert response.status_code == 201
    assert 'id' in response.get_json()
