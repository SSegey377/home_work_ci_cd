
import pytest

from app import create_app, db as _db
from app.models import Client, Parking, ClientParking
from datetime import datetime, timedelta

@pytest.fixture(scope='module')
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"
    })
    with app.app_context():
        _db.create_all()
        # Создание тестовых объектов
        client = Client(name="Test", surname="User ", credit_card="1234-5678-9012-3456", car_number="ABC123")
        parking = Parking(address="Test Address", opened=True, count_places=10, count_available_places=9)
        _db.session.add(client)
        _db.session.add(parking)
        _db.session.commit()
        # Создать запись о въезде и выезде с парковки (time_in 2 часа назад, time_out 1 час назад)
        log = ClientParking(client_id=client.id, parking_id=parking.id,
                            time_in=datetime.utcnow() - timedelta(hours=2),
                            time_out=datetime.utcnow() - timedelta(hours=1))
        _db.session.add(log)
        _db.session.commit()
        yield app
        # Очистка базы данных
        with app.app_context():
            _db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def db(app):
    return _db


