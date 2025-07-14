import factory
from factory import LazyAttribute
from faker import Faker
from .models import Client, Parking
fake = Faker()  # Создаем один экземпляр Faker
class ClientFactory(factory.Factory):
    class Meta:
        model = Client
    name = LazyAttribute(lambda _: fake.first_name())
    surname = LazyAttribute(lambda _: fake.last_name())
    credit_card = LazyAttribute(lambda _: None if fake.boolean() else fake.credit_card_number())
    car_number = LazyAttribute(lambda _: fake.license_plate())

class ParkingFactory(factory.Factory):
    class Meta:
        model = Parking

    address = LazyAttribute(lambda _: fake.address())
    opened = LazyAttribute(lambda _: fake.boolean())
    count_places = LazyAttribute(lambda _: fake.random_int(min=1, max=100))
    count_available_places = LazyAttribute(lambda obj: obj.count_places)

