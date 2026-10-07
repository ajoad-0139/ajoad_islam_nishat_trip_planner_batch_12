from app.repositories.trip import TripRepository
from app.errors import TripNotFoundException, TravelerNotFoundException , InvalidTripUpdateException , TripLockedException, TripNotAcceptingExpensesException
from app.errors import TripNotPlannedException, TripFullException , DuplicateTravelerException, TravelerOverlapException, TravelerNotInTripException,BudgetExceededException, NotAValidStatusException
from app.utils import has_overlapping_trip

class TripService:
    def __init__(self, trip_repository: TripRepository):
        self.trip_repository = trip_repository

    def create_a_trip(self,data):
        return self.trip_repository.create(data)

    def get_all_trips(self) :
            return self.trip_repository.get_all()
    
    def get_a_trip(self, trip_id) :
        trip = self.trip_repository.get(trip_id)
        if trip is None:
            raise TripNotFoundException()
        return trip

    def update_a_trip(self, updated_trip_data, old_trip_data, trip_id):
        if updated_trip_data.max_travelers < old_trip_data.traveler_count:
            raise InvalidTripUpdateException(
                "max_travelers cannot be lower than the current traveler count."
            )
        return self.trip_repository.update(trip_id=trip_id, data=updated_trip_data)

    def delete_a_trip(self, trip_id) :
        return self.trip_repository.delete(trip_id)


    def create_a_trip_traveler(self, trip_id, data):
        trip = self.trip_repository.get(trip_id=trip_id)  
        if trip is None:
            raise TripNotFoundException()
        
        email = data.email.strip().lower()                
        traveler = self.trip_repository.get_traveler_by_email(email)

        if trip.status != "PLANNED":                     
            raise TripNotPlannedException()
        if traveler is not None and traveler in trip.travelers:  
            raise DuplicateTravelerException()
        if trip.available_seats <= 0:                     
            raise TripFullException()
        if traveler is not None and has_overlapping_trip(traveler, trip):
            raise TravelerOverlapException()

        if traveler is None:
            traveler = self.trip_repository.create_traveler(data, email)
        self.trip_repository.add_traveler_to_trip(trip, traveler)
        return {"trip": {**trip.to_dict(), **trip.to_summary_dict()}, "traveler": traveler.to_dict()}

    def remove_a_traveler_from_a_trip(self, trip_id, traveler_id) :
        trip = self.trip_repository.get(trip_id=trip_id)
        if trip is None:
            raise TripNotFoundException()
        if trip.status in ("COMPLETED", "CANCELLED") :
            raise TripLockedException()
        traveler = self.trip_repository.get_traveler_by_id(traveler_id=traveler_id)
        if traveler is None:
            raise TravelerNotFoundException()
        if traveler not in trip.travelers:
            raise TravelerNotInTripException()
        return self.trip_repository.remove_a_traveler_from_a_trip(trip=trip, traveler=traveler)

    def create_a_expense_to_a_trip(self, trip_id, expense_data):
        trip = self.trip_repository.get(trip_id=trip_id)
        if trip is None:
            raise TripNotFoundException()

        if trip.status not in ("PLANNED", "ONGOING") :
            raise TripNotAcceptingExpensesException()

        if trip.remaining_budget<expense_data.amount:
            raise BudgetExceededException()

        return self.trip_repository.create_expense(trip_id=trip_id, expense_data=expense_data)

    def update_trip_status(self, trip_id, validated_status):
        ALLOWED_TRANSITIONS = {"PLANNED": {"ONGOING", "CANCELLED"},"ONGOING": {"COMPLETED", "CANCELLED"}, "COMPLETED": set(), "CANCELLED": set()}
        trip = self.trip_repository.get(trip_id=trip_id)
        if trip is None:
            raise TripNotFoundException()
        if validated_status.status not in ALLOWED_TRANSITIONS[trip.status] :
            raise NotAValidStatusException()
        return self.trip_repository.update_trip_status(trip, validated_status.status)
