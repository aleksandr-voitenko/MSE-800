class MoneyExchangeError(Exception):
    """Base error raised by the money exchange system."""


class ExchangeRateNotAvailableError(MoneyExchangeError):
    """Raised when neither a direct nor a reverse exchange rate exists."""
