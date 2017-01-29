class InvalidDatabaseURL(Exception):
    def __init__(self, message):
        super(InvalidDatabaseURL).__init__(message)
