from flask import Blueprint, jsonify, request
from app.schemas import TripCreate
from app.services.trip import TripService
from app.repositories.trip import TripRepository

blueprint = Blueprint("trips", __name__) 

trip_repository = TripRepository()
trip_service = TripService(trip_repository)


@blueprint.get("/")
def get_all_trips():
    trips = trip_service.get_all_trips()
    return jsonify([trip.to_dict() for trip in trips]), 200

@blueprint.post("/")
def create_a_trip():
    validated_data = TripCreate.model_validate_json(request.get_data())
    trip = trip_service.create_a_trip(validated_data)
    return jsonify(trip.to_dict()), 201

@blueprint.get("/<int:trip_id>")
def get_a_trip(trip_id):
    trip = trip_service.get_a_trip(trip_id)
    return jsonify(trip.to_dict()), 200

# @blueprint.put("/<int:trip_id>")
# def update_a_trip():
#     return None

# @blueprint.delete("<int:trip_id>")
# def delete_a_trip():
#     return None