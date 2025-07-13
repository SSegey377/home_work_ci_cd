from flask import Blueprint, jsonify, request
from datetime import datetime
from .models import db, Client, Parking, ClientParking

bp = Blueprint('main', __name__)



@bp.route('/clients', methods=['GET'])
def get_clients():
    clients = Client.query.all()
    return jsonify([{'id': client.id, 'name': client.name, 'surname': client.surname} for client in clients])


@bp.route('/clients/<int:client_id>', methods=['GET'])
def get_client(client_id):
    client = Client.query.get_or_404(client_id)
    return jsonify({
        'id': client.id,
        'name': client.name,
        'surname': client.surname,
        'credit_card': client.credit_card,
        'car_number': client.car_number
    })


@bp.route('/clients', methods=['POST'])
def create_client():
    data = request.get_json()
    if not data or 'name' not in data or 'surname' not in data:
        return jsonify({'error': 'Name and surname are required'}), 400
    new_client = Client(
        name=data['name'],
        surname=data['surname'],
        credit_card=data.get('credit_card'),
        car_number=data.get('car_number')
    )
    db.session.add(new_client)
    db.session.commit()
    return jsonify({'id': new_client.id}), 201

#print
@bp.route('/parkings', methods=['POST'])
def create_parking():
    data = request.get_json()
    if not data or 'address' not in data or 'count_places' not in data:
        return jsonify({'error': 'Address and count_places are required'}), 400
    count_places = data['count_places']
    if not isinstance(count_places, int) or count_places < 0:
        return jsonify({'error': 'count_places must be a non-negative integer'}), 400
    new_parking = Parking(
        address=data['address'],
        opened=data.get('opened', True),
        count_places=count_places,
        count_available_places=count_places
    )
    db.session.add(new_parking)
    db.session.commit()
    return jsonify({'id': new_parking.id}), 201


@bp.route('/client_parkings', methods=['POST'])
def client_parking_in():
    data = request.get_json()
    if not data or 'client_id' not in data or 'parking_id' not in data:
        return jsonify({'error': 'client_id and parking_id required'}), 400
    client_id = data['client_id']
    parking_id = data['parking_id']
    parking = Parking.query.get_or_404(parking_id)
    client = Client.query.get_or_404(client_id)
    if not parking.opened:
        return jsonify({'error': 'Parking is closed'}), 400
    if parking.count_available_places <= 0:
        return jsonify({'error': 'No available places'}), 400
    if not client.credit_card:
        return jsonify({'error': 'Client must have a credit card to park'}), 400
        # Check if client already parked here without exit
    existing_park = ClientParking.query.filter_by(client_id=client_id, parking_id=parking_id, time_out=None).first()
    if existing_park:
        return jsonify({'error': 'Client already parked here and did not exit'}), 400
    new_client_parking = ClientParking(
        client_id=client_id,
        parking_id=parking_id,
        time_in=datetime.utcnow()
    )
    db.session.add(new_client_parking)
    parking.count_available_places -= 1
    db.session.commit()
    return jsonify({'id': new_client_parking.id}), 201

@bp.route('/client_parkings', methods=['DELETE'])
def client_parking_out():
    data = request.get_json()
    if not data or 'client_id' not in data or 'parking_id' not in data:
        return jsonify({'error': 'client_id and parking_id required'}), 400
    client_id = data['client_id']
    parking_id = data['parking_id']
    client_parking = ClientParking.query.filter_by(client_id=client_id, parking_id=parking_id,
                                                   time_out=None).first()
    if not client_parking:
        return jsonify({'error': 'No active parking record found for this client at the specified parking'}), 404

    client_parking.time_out = datetime.utcnow()
    parking = Parking.query.get_or_404(parking_id)
    parking.count_available_places += 1
    db.session.commit()

    return jsonify({'message': 'Client has left the parking'}), 200
