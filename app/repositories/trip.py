import logging
from sqlalchemy.exc import SQLAlchemyError
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