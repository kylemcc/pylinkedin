class LinkedInException(Exception):
    def __init__(self, cause=None, status_code=None, response=None):
        self.cause = cause
        self.status_code = status_code
        self.response = response
