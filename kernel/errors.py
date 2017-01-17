class AppError(Exception):
    pass


class ValidationError(AppError):
    def __init__(self, description, **kwargs):
        self.description = description


class DataNotFound(AppError):
    pass
