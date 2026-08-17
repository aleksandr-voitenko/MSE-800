from money_exchange import MoneyExchangeError
from money_exchange import MoneyExchangeSystem


class ConsoleApplication:
    """Simple console user interface."""

    def __init__(self, system: MoneyExchangeSystem) -> None:
        self.__system = system

    def run(self) -> None:
        actions = {
            "1": self.__exchange,
            "2": self.__remove_transaction,
            "3": self.__show_all,
            "4": self.__add_customer,
            "5": self.__remove_customer,
            "6": self.__add_currency,
            "7": self.__remove_currency,
            "8": self.__add_rate,
            "9": self.__remove_rate,
        }

        while True:
            print(
                """
1. Exchange currency
2. Remove transaction
3. Show all data
4. Add customer
5. Remove customer
6. Add currency
7. Remove currency
8. Add exchange rate
9. Remove exchange rate
0. Exit
"""
            )

            choice = input("Choose: ").strip()

            if choice == "0":
                return

            action = actions.get(choice)

            if action is None:
                print("Unknown option.")
                continue

            try:
                action()
            except (MoneyExchangeError, ValueError) as exc:
                print(f"Error: {exc}")

    def __add_customer(self) -> None:
        customer = self.__system.add_customer(
            input("First name: "),
            input("Last name: "),
            input("National ID: "),
        )
        print(f"Customer ID: {customer.customer_id}")

    def __remove_customer(self) -> None:
        self.__system.remove_customer(
            int(input("Customer ID: "))
        )

    def __add_currency(self) -> None:
        self.__system.add_currency(
            input("Code: "),
            input("Name: "),
            input("Symbol: "),
        )

    def __remove_currency(self) -> None:
        self.__system.remove_currency(
            input("Code: ")
        )

    def __add_rate(self) -> None:
        self.__system.add_exchange_rate(
            input("From: "),
            input("To: "),
            float(input("Rate: ")),
            input(
                "Effective at "
                "[YYYY-MM-DD HH:MM:SS.SSS, blank = now]: "
            ) or None,
        )

    def __remove_rate(self) -> None:
        self.__system.remove_exchange_rate(
            int(input("Exchange rate ID: "))
        )

    def __exchange(self) -> None:
        transaction = self.__system.exchange(
            int(input("Customer ID: ")),
            input("From: "),
            input("To: "),
            float(input("Amount: ")),
        )

        print(
            f"{transaction.amount_from:.2f} "
            f"{transaction.currency_code_from} -> "
            f"{transaction.amount_to:.2f} "
            f"{transaction.currency_code_to}"
        )
        print(f"Rate used: {transaction.rate_used:.8f}")

    def __remove_transaction(self) -> None:
        self.__system.remove_transaction(
            int(input("Transaction ID: "))
        )

    def __show_all(self) -> None:
        print("\nCustomers:")
        for item in self.__system.list_customers():
            print(item)

        print("\nCurrencies:")
        for item in self.__system.list_currencies():
            print(item)

        print("\nExchange rates:")
        for item in self.__system.list_exchange_rates():
            print(item)

        print("\nTransactions:")
        for item in self.__system.list_transactions():
            print(item)
