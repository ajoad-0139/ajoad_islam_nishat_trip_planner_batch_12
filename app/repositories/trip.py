import logging
from sqlalchemy.exc import SQLAlchemyError
from app.errors import ApiException, TripNotFoundException
from setup_sqlalchemy import sqlalchemy_db as db
from app.models import Trip


logger = logging.getLogger(__name__)

class TripRepository:

    def get_all(self):
        try :
            return Trip.query.all()
        except SQLAlchemyError as e:
                    logger.error(e)
                    db.session.rollback()
                    raise ApiException("Error fetching trips")

    def create(self, data):
        try :
            created_trip = Trip(**data.model_dump())
            db.session.add(created_trip)
            db.session.commit()
            return created_trip
        except SQLAlchemyError as e:
            logger.error(e)
            db.session.rollback()
            raise ApiException("Error creating trip")

    def get(self, trip_id) :
        try :
            return db.session.get(Trip, trip_id)
        except SQLAlchemyError as e:
                    logger.error(e)
                    db.session.rollback()
                    raise ApiException("Error creating A trip")

    def update(self, trip_id, data):
        trip = self.get(trip_id)
        try:
            for field, value in data.model_dump().items():
                if hasattr(Trip, field):
                    setattr(trip, field, value)
            db.session.commit()
            return trip
        except SQLAlchemyError as e:
            logger.error(e)
            db.session.rollback()
            raise ApiException("Error updating a trip")

    def delete(self, trip_id) :
         trip = self.get(trip_id)
         if trip is None :
            raise TripNotFoundException
         try :
            db.session.delete(trip)
            db.session.commit()
         except SQLAlchemyError as e:
            logger.error(e)
            db.session.rollback()
            raise ApiException("Error deleting a trip")