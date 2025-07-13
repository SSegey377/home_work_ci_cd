import factory
from factory import Faker, LazyAttribute
from .models import Client, Parking


class ClientFactory(factory.Factory):
    class Meta:
        model = Client

    name = Faker('first_name')
    surname = Faker('last_name')
    credit_card = LazyAttribute(
        lambda x: None if factory.Faker('boolean').generate() else factory.Faker('credit_card_number').generate())
    car_number = Faker('license_plate')


class ParkingFactory(factory.Factory):
    class Meta:
        model = Parking

    address = Faker('address')
    opened = Faker('boolean')
    count_places = Faker('random_int', min=1, max=100)
    count_available_places = LazyAttribute(lambda obj: obj.count_places)
