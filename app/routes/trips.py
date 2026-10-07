from flask import Blueprint, jsonify, request
from app.schemas import TripCreate, TripUpdate, TravelerCreate, ExpenseCreate, StatusUpdate
from app.services.trip import TripService
from app.repositories.trip import TripRepository
from app.errors import InvalidJsonException , InvalidTripUpdateException, TripNotFoundException

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
    if trip.status  in ("COMPLETED" , "CANCELLED"):
        raise InvalidTripUpdateException("this trip is already completed or canceled, can't update")
    merged = {**trip.to_dict(), **update_data}
    merged.pop("id", None)
    validated = TripUpdate.model_validate(merged)
    updated_trip = trip_service.update_a_trip(validated, trip, trip_id)
    return jsonify(updated_trip.to_dict()), 200

@blueprint.delete("/<int:trip_id>")
def delete_a_trip(trip_id):
    trip_service.delete_a_trip(trip_id=trip_id)
    return jsonify({"message": "Trip deleted successfully"}), 200



#trips-travelers routes 
@blueprint.post("/<int:trip_id>/travelers")
def create_a_trip_traveler(trip_id) :
    validated_traveler = TravelerCreate.model_validate_json(request.get_data())
    trip_traveler = trip_service.create_a_trip_traveler(trip_id=trip_id, data=validated_traveler)
    return jsonify(trip_traveler), 201

@blueprint.delete("/<int:trip_id>/travelers/<int:traveler_id>/")
def remove_a_traveler_from_a_trip(trip_id, traveler_id) :
    trip_service.remove_a_traveler_from_a_trip(trip_id=trip_id, traveler_id=traveler_id)
    return jsonify({"message": "Traveler deleted successfully"}), 200


#trip-summary routes 
@blueprint.get("/<int:trip_id>/summary")
def get_trip_summary(trip_id) :
    trip = trip_service.get_a_trip(trip_id=trip_id)
    if trip is None :
        raise TripNotFoundException()
    return jsonify(trip.to_summary_dict()), 200


#trip-expenses routes 
@blueprint.post("/<int:trip_id>/expenses")
def create_a_expense_to_a_trip(trip_id):
    validated_expense = ExpenseCreate.model_validate_json(request.get_data())
    expense = trip_service.create_a_expense_to_a_trip(trip_id, validated_expense)
    return jsonify(expense.to_dict()), 201


#trip-status route
@blueprint.patch("/<int:trip_id>/status")
def change_trip_status(trip_id):
    validated_status = StatusUpdate.model_validate_json(request.get_data())
    updated_trip = trip_service.update_trip_status(trip_id, validated_status)
    return jsonify(updated_trip.to_dict()),200