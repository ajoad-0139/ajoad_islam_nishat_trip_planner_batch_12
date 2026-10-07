import logging
from sqlalchemy.exc import SQLAlchemyError
from app.errors import ApiException, TripNotFoundException
from setup_sqlalchemy import sqlalchemy_db as db
from app.models import Trip , Traveler , trip_traveler, Expense


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
                    raise ApiException("Error getting A trip")

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

    def get_traveler_by_email(self, email):
        try:
            stmt = db.select(Traveler).filter_by(email=email)
            return db.session.execute(stmt).scalar_one_or_none()
        except SQLAlchemyError as e:
            logger.error(e)
            db.session.rollback()
            raise ApiException("Error getting a traveler")
        
    def get_traveler_by_id(self, traveler_id) :
        try:
            stmt = db.select(Traveler).filter_by(id=traveler_id)
            return db.session.execute(stmt).scalar_one_or_none() 
        except SQLAlchemyError as e:
            logger.error(e)
            db.session.rollback()
            raise ApiException("Error deleting traveler to trip")

    def create_traveler(self, data, email):
        try:
            traveler = Traveler(name=data.name, email=email)
            db.session.add(traveler)
            db.session.commit()
            return traveler
        except SQLAlchemyError as e:
            logger.error(e)
            db.session.rollback()
            raise ApiException("Error creating a traveler")

    def add_traveler_to_trip(self, trip, traveler):
        try:
            trip.travelers.append(traveler)
            db.session.commit()
        except SQLAlchemyError as e:
            logger.error(e)
            db.session.rollback()
            raise ApiException("Error adding traveler to trip")

    def remove_a_traveler_from_a_trip(self, trip, traveler) :
        try :
            trip.travelers.remove(traveler)
            db.session.commit() 
        except SQLAlchemyError as e:
            logger.error(e)
            db.session.rollback()
            raise ApiException("Error deleting traveler to trip")

    def create_expense(self, trip_id, expense_data) :
        try :
            created_expense = Expense(trip_id=trip_id,**expense_data.model_dump())
            db.session.add(created_expense)
            db.session.commit()
            return created_expense
        except SQLAlchemyError as e:
            logger.error(e)
            db.session.rollback()
            raise ApiException("Error creating a expense to a trip")