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