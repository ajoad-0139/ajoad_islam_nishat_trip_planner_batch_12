from flask import Blueprint, jsonify, request
from app.schemas import TripCreate, TripUpdate, TravelerCreate
from app.services.trip import TripService
from app.repositories.trip import TripRepository
from app.errors import InvalidJsonException

blueprint = Blueprint("trips", __name__) 

trip_repository = TripRepository()
trip_service = TripService(trip_repository)

#basic trip crud routes 
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

@blueprint.put("/<int:trip_id>")
def update_a_trip(trip_id):
    update_data = request.get_json(silent=True)
    if not isinstance(update_data, dict):
        raise InvalidJsonException("Body must be a JSON object.")
    trip = trip_service.get_a_trip(trip_id)
    merged = {**trip.to_dict(), **update_data}
    merged.pop("id", None)
    validated = TripUpdate.model_validate(merged)
    updated_trip = trip_service.update_a_trip(validated, trip, trip_id)
    return jsonify(updated_trip.to_dict()), 200

@blueprint.delete("/<int:trip_id>")
def delete_a_trip(trip_id):
    trip_service.delete_a_trip(trip_id=trip_id)
    return jsonify({"message": "Deleted successfully"}), 200



#trips-travelers routes 
@blueprint.post("/<int:trip_id>/travelers")
def create_a_trip_traveler(trip_id) :
    validated_traveler = TravelerCreate.model_validate_json(request.get_data())
    trip_traveler = trip_service.create_a_trip_traveler(trip_id=trip_id, data=validated_traveler)
    return jsonify(trip_traveler), 201