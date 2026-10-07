def has_overlapping_trip( traveler, trip):
        for other in traveler.trips:

            if other.status == "CANCELLED":
                continue

            if other.start_date <= trip.end_date and other.end_date >= trip.start_date:
                return True

        return False