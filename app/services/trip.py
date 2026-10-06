from app.repositories.trip import TripRepository
from app.errors import TripNotFoundException, CustomException

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
        