
class NotFoundException(Exception):
    message = 'not found'
    status_code = 404


class ParamsException(Exception):
    message = 'params miss'
    status_code = 400