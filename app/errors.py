import logging
from typing import Dict
from flask import jsonify
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

    def __init__(self, message: str = None, status_code: int = 400):
        super(ApiException, self).__init__(message)
        self._message = message
        self._status_code = status_code




def error_response(error_message, status_code: int = 400):

        # Remove the default 404 not found message if it exists
        if not isinstance(error_message, Dict):
            error_message = error_message.replace("404 Not Found: ", '')

        response = jsonify({"error_message": error_message})
        response.status_code = status_code
        return response


def error_handler(error):
        logger.error("exception of type {} occurred".format(type(error)))
        logger.exception(error)

        if isinstance(error, HTTPException):
            return error_response(str(error), error.code)
        elif isinstance(error, ClientException):
            return error_response(
                "Currently a dependent service is not available, "
                "please try again later", 503
            )
        elif isinstance(error, ApiException):
            return error_response(
                error.error_message, error.status_code
            )
        else:
            # Internal error happened that was unknown
            return "Internal server error", 500

def setup_error_handler(app) :

    app.errorhandler(Exception)(error_handler)
    return app