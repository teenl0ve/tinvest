from .schemas import Error

__all__ = (
    'TinvestError',
    'BadRequestError',
    'TooManyRequestsError',
    'UnexpectedError',
    'SubscriptionElreadyExists',
)


class TinvestError(Exception):
    pass


class BadRequestError(TinvestError):
    def __init__(self, raw: str):
        super().__init__(raw)
        self.response = Error.parse_raw(raw)


class TooManyRequestsError(TinvestError):
    pass


class UnexpectedError(TinvestError):
    def __init__(self, status: int, text: str):
        super().__init__(f'{status} {text}')
        self.status = status
        self.text = text


class SubscriptionElreadyExists(TinvestError):
    pass
