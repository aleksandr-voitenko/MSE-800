from dataclasses import dataclass

# Structures here repeat and extend (when necessary) DB tables

@dataclass(frozen=True)
class Customer:
    customer_id: int
    first_name: str
    last_name: str
    national_id: str


@dataclass(frozen=True)
class Currency:
    code: str
    name: str
    symbol: str


@dataclass(frozen=True)
class ExchangeRate:
    exchange_rate_id: int
    currency_code_from: str
    currency_code_to: str
    rate: float
    effective_at: str


@dataclass(frozen=True)
class Transaction:
    transaction_id: int
    customer_id: int
    exchange_rate_id: int
    currency_code_from: str
    currency_code_to: str
    amount_from: float
    amount_to: float
    rate_used: float
    date_time: str
