class NegativeValueError(ValueError):
    pass


class NotFoundOrNoAccessException(Exception):
    detail: str

    def __init__(self, detail: str):
        self.detail = detail

