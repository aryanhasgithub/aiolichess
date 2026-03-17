"""Exceptions for aiolichess."""


class AioLichessError(Exception):
    """Base exception for all aiolichess errors."""


class AuthError(AioLichessError):
    """Raised on 401 — invalid or missing API token."""


class RateLimitError(AioLichessError):
    """Raised on 429 — rate limit hit. Wait 60 seconds before retrying."""


class LichessServerError(AioLichessError):
    """Raised on 5xx — server side error from Lichess."""