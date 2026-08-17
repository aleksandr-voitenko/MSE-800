from datetime import datetime

from .database import MoneyExchangeDatabase
from .errors import ExchangeRateNotAvailableError, MoneyExchangeError
from .models import Customer, Currency, ExchangeRate, Transaction

# The main class that represents the money exchange system.
# It hides the underlyting data layer.
class MoneyExchangeSystem:
    """
    Public interface to the money exchange application.

    Users of this class work with domain objects and do not need to know that
    the data is stored in SQLite or that raw SQL is used internally.
    """

    # ISO-8601 date format string
    __DATE_FORMAT = "%Y-%m-%d %H:%M:%S.%f"

    def __init__(self, database_file: str) -> None:
        self.__database = MoneyExchangeDatabase(database_file)

    def close(self) -> None:
        self.__database.close()

    # ---------- Customers ----------

    def add_customer(
        self,
        first_name: str,
        last_name: str,
        national_id: str,
    ) -> Customer:
        first_name = first_name.strip()
        last_name = last_name.strip()
        national_id = national_id.strip()

        if not first_name or not last_name or not national_id:
            raise MoneyExchangeError("All customer fields are required.")

        return self.__database.add_customer(
            first_name,
            last_name,
            national_id,
        )

    def remove_customer(self, customer_id: int) -> None:
        self.__database.remove_customer(customer_id)

    def list_customers(self) -> list[Customer]:
        return self.__database.list_customers()

    # ---------- Currencies ----------

    def add_currency(self, code: str, name: str, symbol: str) -> Currency:
        code = code.strip().upper()
        name = name.strip()
        symbol = symbol.strip()

        if not code or not name or not symbol:
            raise MoneyExchangeError("All currency fields are required.")

        return self.__database.add_currency(code, name, symbol)

    def remove_currency(self, code: str) -> None:
        code = code.strip().upper()
        self.__database.remove_currency(code)

    def list_currencies(self) -> list[Currency]:
        return self.__database.list_currencies()

    # ---------- Exchange rates ----------

    def add_exchange_rate(
        self,
        currency_code_from: str,
        currency_code_to: str,
        rate: float,
        effective_at: str | None = None,
    ) -> ExchangeRate:
        code_from = currency_code_from.strip().upper()
        code_to = currency_code_to.strip().upper()

        if code_from == code_to:
            raise MoneyExchangeError(
                "Source and target currencies must be different."
            )

        if rate <= 0:
            raise MoneyExchangeError("Exchange rate must be positive.")

        self.__require_currency(code_from)
        self.__require_currency(code_to)

        date_time = self.__normalise_date_time(effective_at)

        return self.__database.add_exchange_rate(
            code_from,
            code_to,
            rate,
            date_time,
        )

    def remove_exchange_rate(self, exchange_rate_id: int) -> None:
        self.__database.remove_exchange_rate(exchange_rate_id)

    def list_exchange_rates(self) -> list[ExchangeRate]:
        return self.__database.list_exchange_rates()

    # ---------- Transactions ----------

    def exchange(
        self,
        customer_id: int,
        currency_code_from: str,
        currency_code_to: str,
        amount_from: float,
    ) -> Transaction:
        code_from = currency_code_from.strip().upper()
        code_to = currency_code_to.strip().upper()

        if code_from == code_to:
            raise MoneyExchangeError(
                "Source and target currencies must be different."
            )

        if amount_from <= 0:
            raise MoneyExchangeError("Amount must be positive.")

        self.__require_customer(customer_id)
        self.__require_currency(code_from)
        self.__require_currency(code_to)

        # Only the latest exchange rate for a pair is valid
        exchange_rate = self.__database.find_latest_exchange_rate(
            code_from,
            code_to,
        )

        if exchange_rate is None:
            # We do not try to convert through a third currency.
            raise ExchangeRateNotAvailableError(
                f"Exchange rate is not available for "
                f"{code_from} -> {code_to}."
            )

        rate_reversed = (
            exchange_rate.currency_code_from == code_to
            and exchange_rate.currency_code_to == code_from
        )

        # If only the opposite direction is stored, use its reciprocal.
        rate_used = (
            1.0 / exchange_rate.rate
            if rate_reversed
            else exchange_rate.rate
        )

        amount_to = round(amount_from * rate_used, 2)
        date_time = self.__now_text()

        return self.__database.add_transaction(
            customer_id=customer_id,
            exchange_rate_id=exchange_rate.exchange_rate_id,
            currency_code_from=code_from,
            currency_code_to=code_to,
            amount_from=amount_from,
            amount_to=amount_to,
            rate_used=rate_used,
            rate_reversed=rate_reversed,
            date_time=date_time,
        )

    def remove_transaction(self, transaction_id: int) -> None:
        self.__database.remove_transaction(transaction_id)

    def list_transactions(self) -> list[Transaction]:
        return self.__database.list_transactions()

    # ---------- Internal helpers ----------

    def __require_customer(self, customer_id: int) -> None:
        if not self.__database.customer_exists(customer_id):
            raise MoneyExchangeError(
                f"Customer {customer_id} does not exist."
            )

    def __require_currency(self, code: str) -> None:
        if not self.__database.currency_exists(code):
            raise MoneyExchangeError(
                f"Currency {code} does not exist."
            )

    @classmethod
    def __now_text(cls) -> str:
        return datetime.now().strftime(cls.__DATE_FORMAT)[:-3]

    @classmethod
    def __normalise_date_time(cls, value: str | None) -> str:
        if not value:
            return cls.__now_text()

        try:
            date_time = datetime.strptime(value, cls.__DATE_FORMAT)
        except ValueError as exc:
            raise MoneyExchangeError(
                "Date/time must use YYYY-MM-DD HH:MM:SS.SSS"
            ) from exc

        # Store exactly three digits for milliseconds.
        return date_time.strftime(cls.__DATE_FORMAT)[:-3]
