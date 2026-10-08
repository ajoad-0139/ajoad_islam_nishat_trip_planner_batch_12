import logging
from typing import Dict
from flask import jsonify
from pydantic import ValidationError
from werkzeug.exceptions import HTTPException

logger = logging.getLogger(__name__)

# custorm errors
class OperationalException(Exception):

    def __init__(self, message: str = None):
        super(OperationalException, self).__init__(message)


class ClientException(Exception):

    def __init__(self, message: str = None):
        super(ClientException, self).__init__(message)


class ApiException(Exception):
    code = "API_ERROR"
    status_code = 400
    default_message = "The request could not be processed."

    def __init__(self, message: str = None):
        self.message = message or self.default_message
        super(ApiException, self).__init__(self.message)

class ValidationException(ApiException):
    code = "VALIDATION_ERROR"
    status_code = 400
    default_message = "The request data is invalid."
 
class InvalidJsonException(ValidationException):
    code = "INVALID_JSON"
    default_message = "Request body must be valid JSON."

class NotFoundException(ApiException):
    code = "NOT_FOUND"
    status_code = 404
    default_message = "Resource not found."
 
 
class TripNotFoundException(NotFoundException):
    code = "TRIP_NOT_FOUND"
    default_message = "Trip not found."

class TravelerNotFoundException(NotFoundException):
    code = "TRAVELER_NOT_FOUND"
    default_message = "Traveler not found."

class TravelerNotInTripException(NotFoundException):
    code = "TRAVELER_NOT_IN_TRIP"
    default_message = "The traveler is not part of this trip."

class CustomException(Exception) :
    def __init__(self, code:str="custom error", default_message:str="custom error message", status_code = 400):
        self.code = code, self.default_message=default_message
 
class InvalidTripUpdateException(ValidationException):
    code = "INVALID_TRIP_UPDATE"
    default_message = "The trip update is not allowed."
    status_code =409

class TravelerCreationException(ApiException) :
    def __init__(self, code:str="TRAVELER_CREATION_ERROR", default_message:str="traveler creation errror message", status_code = 409):
        self.code = code, self.default_message=default_message

class ConflictException(ApiException):
    code = "CONFLICT"
    status_code = 409
    default_message = "The request conflicts with the current state."

class TripLockedException(ConflictException):
    code = "TRIP_LOCKED"
    default_message = "Completed or cancelled trips cannot be modified."

class TripNotAcceptingExpensesException(ConflictException):
    code = "TRIP_NOT_ACCEPTING_EXPENSES"
    default_message = "Expenses can only be added while the trip is PLANNED or ONGOING."

class NotAValidStatusException(ConflictException) :
    code = "INVALID_STATUS"
    default_message = "Invalid status update request, please provide a valid status"

class BudgetExceededException(ConflictException):
    code = "BUDGET_EXCEEDED"
    default_message = "The expense exceeds the remaining trip budget."

class DuplicateTravelerException(ConflictException):
    code = "DUPLICATE_TRAVELER"
    default_message = "The traveler is already part of this trip."

class TripFullException(ConflictException):
    code = "TRIP_FULL"
    default_message = "The trip has reached its maximum traveler capacity."

class TripNotPlannedException(ConflictException):
    code = "TRIP_NOT_PLANNED"
    default_message = "Travelers can only be added while the trip is PLANNED."

class TravelerOverlapException(ConflictException):
    code = "TRAVELER_TRIP_OVERLAP"
    default_message = "The traveler already has a trip overlapping these dates."

# error response formater
def error_response(error_title, error_message, status_code: int = 400):

        # Remove the default 404 not found message if it exists
        if not isinstance(error_message, Dict):
            error_message = error_message.replace("404 Not Found: ", '')

        response = jsonify({"error":error_title,"message": error_message})
        response.status_code = status_code
        return response


def format_pydantic_errors(error: ValidationError) -> str:
    messages = []
    for item in error.errors():
        field = ".".join(str(part) for part in item["loc"])
        text = item["msg"].removeprefix("Value error, ")
        messages.append(f"{field}: {text}" if field else text)
    return "; ".join(messages)


def error_handler(error):
        logger.error("exception of type {} occurred".format(type(error)))
        logger.exception(error)

        if isinstance(error, ValidationError):
            if error.errors()[0]["type"] == "json_invalid":
                code, message = InvalidJsonException.code, InvalidJsonException.default_message
            else:
                code, message = ValidationException.code, format_pydantic_errors(error)
            return error_response(code, message, 400)
    

        if isinstance(error, HTTPException):
            return error_response("http-error",str(error), error.code)
        elif isinstance(error, ClientException):
            return error_response(
                "Bad-request",
                "Currently a dependent service is not available, "
                "please try again later", 503
            )
        elif isinstance(error, ApiException):
            logger.warning("%s (%s): %s", error.code, error.status_code, error.message)
            return error_response(error.code, error.message, error.status_code)
        else:
            # Internal error happened that was unknown
            return error_response("INTERNAL_SERVER_ERROR", "Internal server error", 500)

def setup_error_handler(app) :

    app.errorhandler(Exception)(error_handler)
    return app