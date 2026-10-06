from decimal import Decimal

from setup_sqpalchemy import sqlalchemy_db as db 

trip_traveler = db.Table(
    "trip_traveler",
    db.Column("trip_id", db.Integer, db.ForeignKey("trips.id"), primary_key=True),
    db.Column("traveler_id", db.Integer, db.ForeignKey("travelers.id"), primary_key=True),
)


class Trip(db.Model):
    __tablename__ = "trips"

    id = db.Column(db.Integer, primary_key=True)
    destination = db.Column(db.String(200), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    budget = db.Column(db.Numeric(12, 2), nullable=False)
    max_travelers = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), nullable=False, default="PLANNED")

    travelers = db.relationship("Traveler", secondary=trip_traveler, back_populates="trips")
    expenses = db.relationship("Expense", backref="trip", cascade="all, delete-orphan")

    @property
    def traveler_count(self):
        return len(self.travelers)

    @property
    def available_seats(self):
        return self.max_travelers - self.traveler_count

    @property
    def total_expense(self):
        return sum((expense.amount for expense in self.expenses), Decimal("0.00"))

    @property
    def remaining_budget(self):
        return self.budget - self.total_expense

    def to_dict(self):
        return {
            "id": self.id,
            "destination": self.destination,
            "start_date": self.start_date.isoformat(),
            "end_date": self.end_date.isoformat(),
            "budget": float(self.budget),
            "max_travelers": self.max_travelers,
            "status": self.status,
        }

    def to_summary_dict(self):
        return {
            "trip_id": self.id,
            "status": self.status,
            "traveler_count": self.traveler_count,
            "available_seats": self.available_seats,
            "total_expense": float(self.total_expense),
            "remaining_budget": float(self.remaining_budget),
        }


class Traveler(db.Model):
    __tablename__ = "travelers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True) 

    trips = db.relationship("Trip", secondary=trip_traveler, back_populates="travelers")

    def to_dict(self):
        return {"id": self.id, "name": self.name, "email": self.email}


class Expense(db.Model):
    __tablename__ = "expenses"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    amount = db.Column(db.Numeric(12, 2), nullable=False)
    trip_id = db.Column(db.Integer, db.ForeignKey("trips.id"), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "trip_id": self.trip_id,
            "title": self.title,
            "amount": float(self.amount),
        }