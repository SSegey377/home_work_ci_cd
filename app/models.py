from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
# from datetime import datetime
# from typing import Optional

# СОЗДАЁМ ЭКЗЕМПЛЯР db ЗДЕСЬ, чтобы избежать проблем с импортом
db = SQLAlchemy()


class Client(db.Model):
    __tablename__ = "client"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    surname = Column(String(50), nullable=False)
    credit_card = Column(String(50), nullable=True)
    car_number = Column(String(10), nullable=True)

    def __repr__(self) -> str:
        return f"<Client {self.name} {self.surname}>"


class Parking(db.Model):
    __tablename__ = "parking"

    id = Column(Integer, primary_key=True)
    address = Column(String(100), nullable=False)
    opened = Column(Boolean, nullable=True)
    count_places = Column(Integer, nullable=False)
    count_available_places = Column(Integer, nullable=False)

    def __repr__(self) -> str:
        return f"<Parking {self.address}>"


class ClientParking(db.Model):
    __tablename__ = "client_parking"

    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey("client.id"), nullable=False)
    parking_id = Column(Integer, ForeignKey("parking.id"), nullable=False)
    time_in = Column(DateTime, nullable=False)
    time_out = Column(DateTime, nullable=True)

    # Relationships
    client = relationship("Client", backref="client_parking")
    parking = relationship("Parking", backref="client_parking")

    __table_args__ = (
        UniqueConstraint("client_id", "parking_id", name="unique_client_parking"),
    )

    def __repr__(self) -> str:
        return (
            f"<ClientParking ClientID: {self.client_id}, ParkingID: {self.parking_id}>"
        )
