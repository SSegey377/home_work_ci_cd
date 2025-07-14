# from app import create_app
#
# app = create_app()
#
# if __name__ == '__main__':
#     app.run(debug=True)

from app import create_app, db
from app.factories import ClientFactory, ParkingFactory

app = create_app()

with app.app_context():
    # Создание тестовых данных
    for _ in range(100):  # Создание 10 клиентов
        client = ClientFactory()
        db.session.add(client)
    for _ in range(100):  # Создание 5 парковок
        parking = ParkingFactory()
        db.session.add(parking)
    db.session.commit()  # Сохранение изменений в базе данных


if __name__ == '__main__':
    app.run(debug=True)
