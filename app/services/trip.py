from app.repositories.trip import TripRepository
from app.errors import TripNotFoundException, InvalidTripUpdateException

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
         

        