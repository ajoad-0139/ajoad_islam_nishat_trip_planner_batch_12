def has_overlapping_trip( traveler, trip ,start_date=None, end_date=None):
        new_start = start_date or trip.start_date
        new_end = end_date or trip.end_date

        for other in traveler.trips:
            if other.id == trip.id :
                continue
            if other.status == "CANCELLED":
                continue
            if other.start_date <= new_end and other.end_date >= new_start:
                return True
        return False