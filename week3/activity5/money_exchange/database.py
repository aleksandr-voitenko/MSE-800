import sqlite3

from .errors import MoneyExchangeError
from .models import Customer, Currency, ExchangeRate, Transaction

# MoneyExchangeDatabase is a database management facade that encapsulates SQL queries
class MoneyExchangeDatabase:
    """
    Internal persistence class.

    The rest of the application uses methods of this class and does not need
    to work with sqlite3 connections or SQL rows directly.
    """

    def __init__(self, database_file: str) -> None:
        self.__connection = sqlite3.connect(database_file)

        # sqlite3 normally returns query results as tuples. sqlite3.Row lets the
        # rest of the application access columns by name, e.g. row["course_name"].
        self.__connection.row_factory = sqlite3.Row

        # SQLite foreign-key checks must be enabled for every connection.
        self.__connection.execute("PRAGMA foreign_keys = ON")
        self.__create_tables()

    def close(self) -> None:
        self.__connection.close()

    def __create_tables(self) -> None:
        self.__connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS customers (
                customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                national_id TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS currencies (
                code TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                symbol TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS exchange_rates (
                exchange_rate_id INTEGER PRIMARY KEY AUTOINCREMENT,
                currency_code_from TEXT NOT NULL,
                currency_code_to TEXT NOT NULL,
                rate REAL NOT NULL CHECK (rate > 0),
                effective_at TEXT NOT NULL,

                CHECK (currency_code_from <> currency_code_to),

                FOREIGN KEY (currency_code_from)
                    REFERENCES currencies(code)
                    ON UPDATE CASCADE
                    ON DELETE RESTRICT,

                FOREIGN KEY (currency_code_to)
                    REFERENCES currencies(code)
                    ON UPDATE CASCADE
                    ON DELETE RESTRICT
            );

            CREATE TABLE IF NOT EXISTS transactions (
                transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER NOT NULL,
                exchange_rate_id INTEGER NOT NULL,
                amount_from REAL NOT NULL CHECK (amount_from > 0),
                amount_to REAL NOT NULL CHECK (amount_to >= 0),

                -- This records whether the selected exchange rate was reversed.
                rate_reversed INTEGER NOT NULL
                    CHECK (rate_reversed IN (0, 1)),

                date_time TEXT NOT NULL,

                FOREIGN KEY (customer_id)
                    REFERENCES customers(customer_id)
                    ON UPDATE CASCADE
                    ON DELETE RESTRICT,

                FOREIGN KEY (exchange_rate_id)
                    REFERENCES exchange_rates(exchange_rate_id)
                    ON UPDATE CASCADE
                    ON DELETE RESTRICT
            );
            """
        )
        self.__connection.commit()

    # ---------- Customers ----------

    def add_customer(
        self,
        first_name: str,
        last_name: str,
        national_id: str,
    ) -> Customer:
        with self.__connection:
            cursor = self.__connection.execute(
                """
                INSERT INTO customers (first_name, last_name, national_id)
                VALUES (?, ?, ?)
                """,
                (first_name, last_name, national_id),
            )

        return Customer(
            customer_id=cursor.lastrowid,
            first_name=first_name,
            last_name=last_name,
            national_id=national_id,
        )

    def remove_customer(self, customer_id: int) -> None:
        self.__delete_by_id(
            table="customers",
            id_column="customer_id",
            value=customer_id,
            entity_name="Customer",
        )

    def list_customers(self) -> list[Customer]:
        rows = self.__connection.execute(
            """
            SELECT customer_id, first_name, last_name, national_id
            FROM customers
            ORDER BY customer_id
            """
        ).fetchall()

        return [Customer(**dict(row)) for row in rows]

    def customer_exists(self, customer_id: int) -> bool:
        row = self.__connection.execute(
            "SELECT 1 FROM customers WHERE customer_id = ?",
            (customer_id,),
        ).fetchone()

        return row is not None

    # ---------- Currencies ----------

    def add_currency(self, code: str, name: str, symbol: str) -> Currency:
        try:
            with self.__connection:
                self.__connection.execute(
                    """
                    INSERT INTO currencies (code, name, symbol)
                    VALUES (?, ?, ?)
                    """,
                    (code, name, symbol),
                )
        except sqlite3.IntegrityError as exc:
            raise MoneyExchangeError(
                f"Currency {code} already exists."
            ) from exc

        return Currency(code=code, name=name, symbol=symbol)

    def remove_currency(self, code: str) -> None:
        try:
            with self.__connection:
                cursor = self.__connection.execute(
                    "DELETE FROM currencies WHERE code = ?",
                    (code,),
                )

                if cursor.rowcount == 0:
                    raise MoneyExchangeError(
                        f"Currency {code} does not exist."
                    )
        except sqlite3.IntegrityError as exc:
            raise MoneyExchangeError(
                f"Currency {code} is in use and cannot be removed."
            ) from exc

    def list_currencies(self) -> list[Currency]:
        rows = self.__connection.execute(
            "SELECT code, name, symbol FROM currencies ORDER BY code"
        ).fetchall()

        return [Currency(**dict(row)) for row in rows]

    def currency_exists(self, code: str) -> bool:
        row = self.__connection.execute(
            "SELECT 1 FROM currencies WHERE code = ?",
            (code,),
        ).fetchone()

        return row is not None

    # ---------- Exchange rates ----------

    def add_exchange_rate(
        self,
        currency_code_from: str,
        currency_code_to: str,
        rate: float,
        effective_at: str,
    ) -> ExchangeRate:
        with self.__connection:
            cursor = self.__connection.execute(
                """
                INSERT INTO exchange_rates (
                    currency_code_from,
                    currency_code_to,
                    rate,
                    effective_at
                )
                VALUES (?, ?, ?, ?)
                """,
                (
                    currency_code_from,
                    currency_code_to,
                    rate,
                    effective_at,
                ),
            )

        return ExchangeRate(
            exchange_rate_id=cursor.lastrowid,
            currency_code_from=currency_code_from,
            currency_code_to=currency_code_to,
            rate=rate,
            effective_at=effective_at,
        )

    def remove_exchange_rate(self, exchange_rate_id: int) -> None:
        self.__delete_by_id(
            table="exchange_rates",
            id_column="exchange_rate_id",
            value=exchange_rate_id,
            entity_name="Exchange rate",
        )

    def list_exchange_rates(self) -> list[ExchangeRate]:
        rows = self.__connection.execute(
            """
            SELECT
                exchange_rate_id,
                currency_code_from,
                currency_code_to,
                rate,
                effective_at
            FROM exchange_rates
            ORDER BY effective_at DESC, exchange_rate_id DESC
            """
        ).fetchall()

        return [ExchangeRate(**dict(row)) for row in rows]

    def find_latest_exchange_rate(
        self,
        code_from: str,
        code_to: str,
    ) -> ExchangeRate | None:
        """
        Find the newest rate for this currency pair in either direction.

        No intermediate currency is considered, so cross-rate conversion is
        deliberately not supported.
        """
        row = self.__connection.execute(
            """
            SELECT
                exchange_rate_id,
                currency_code_from,
                currency_code_to,
                rate,
                effective_at
            FROM exchange_rates
            WHERE
                (currency_code_from = ? AND currency_code_to = ?)
                OR
                (currency_code_from = ? AND currency_code_to = ?)
            ORDER BY effective_at DESC, exchange_rate_id DESC
            LIMIT 1
            """,
            (code_from, code_to, code_to, code_from),
        ).fetchone()

        if row is None:
            return None

        return ExchangeRate(**dict(row))

    # ---------- Transactions ----------

    def add_transaction(
        self,
        customer_id: int,
        exchange_rate_id: int,
        currency_code_from: str,
        currency_code_to: str,
        amount_from: float,
        amount_to: float,
        rate_used: float,
        rate_reversed: bool,
        date_time: str,
    ) -> Transaction:
        with self.__connection:
            cursor = self.__connection.execute(
                """
                INSERT INTO transactions (
                    customer_id,
                    exchange_rate_id,
                    amount_from,
                    amount_to,
                    rate_reversed,
                    date_time
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    customer_id,
                    exchange_rate_id,
                    amount_from,
                    amount_to,
                    int(rate_reversed),
                    date_time,
                ),
            )

        return Transaction(
            transaction_id=cursor.lastrowid,
            customer_id=customer_id,
            exchange_rate_id=exchange_rate_id,
            currency_code_from=currency_code_from,
            currency_code_to=currency_code_to,
            amount_from=amount_from,
            amount_to=amount_to,
            rate_used=rate_used,
            date_time=date_time,
        )

    def remove_transaction(self, transaction_id: int) -> None:
        self.__delete_by_id(
            table="transactions",
            id_column="transaction_id",
            value=transaction_id,
            entity_name="Transaction",
        )

    def list_transactions(self) -> list[Transaction]:
        rows = self.__connection.execute(
            """
            SELECT
                t.transaction_id,
                t.customer_id,
                t.exchange_rate_id,
                t.amount_from,
                t.amount_to,
                t.rate_reversed,
                t.date_time,
                r.currency_code_from,
                r.currency_code_to,
                r.rate
            FROM transactions AS t
            JOIN exchange_rates AS r ON r.exchange_rate_id = t.exchange_rate_id
            ORDER BY t.transaction_id
            """
        ).fetchall()

        result: list[Transaction] = []

        for row in rows:
            if row["rate_reversed"]:
                code_from = row["currency_code_to"]
                code_to = row["currency_code_from"]
                rate_used = 1.0 / row["rate"]
            else:
                code_from = row["currency_code_from"]
                code_to = row["currency_code_to"]
                rate_used = row["rate"]

            result.append(
                Transaction(
                    transaction_id=row["transaction_id"],
                    customer_id=row["customer_id"],
                    exchange_rate_id=row["exchange_rate_id"],
                    currency_code_from=code_from,
                    currency_code_to=code_to,
                    amount_from=row["amount_from"],
                    amount_to=row["amount_to"],
                    rate_used=rate_used,
                    date_time=row["date_time"],
                )
            )

        return result

    # ---------- Internal helpers ----------

    def __delete_by_id(
        self,
        table: str,
        id_column: str,
        value: int,
        entity_name: str,
    ) -> None:
        # table and id_column are internal constants, not user input.
        try:
            with self.__connection:
                cursor = self.__connection.execute(
                    f"DELETE FROM {table} WHERE {id_column} = ?",
                    (value,),
                )

                if cursor.rowcount == 0:
                    raise MoneyExchangeError(
                        f"{entity_name} {value} does not exist."
                    )
        except sqlite3.IntegrityError as exc:
            raise MoneyExchangeError(
                f"{entity_name} {value} is in use and cannot be removed."
            ) from exc
