class BankAccount:
    def __init__(self, account_number, customer_name, balance):
        self._account_number = account_number
        self._customer_name = customer_name
        self._balance = balance


    def balance(self):
        return self._balance

    def balance_str(self):
        return f"Balance: ${self._balance:,.2f}"

    def display_details(self):
        print(f"Account number: {self._account_number}")
        print(f"Customer name: {self._customer_name}")
        print(self.balance_str())

    def deposit(self, amount):
        if amount <= 0:
            print("Deposit amount must be positive.")
            return
        self._balance += amount
        print(f"Deposited: ${amount:,.2f}. {self.balance_str()}")

    def withdraw(self, amount):
        if amount <= 0:
            print("Withdrawal amount must be positive.")
            return
        if amount > self._balance:
            print("Withdrawal declined: insufficient funds.")
            return
        self._balance -= amount
        print(f"Withdrew: ${amount:,.2f}. {self.balance_str()}")


class SavingsAccount(BankAccount):
    def __init__(self, account_number, customer_name, balance, interest_rate):
        super().__init__(account_number, customer_name, balance)
        # The interest rate is a percentage, so 5 means 5%.
        self._interest_rate = interest_rate

    def display_details(self):
        print("Account type: Savings Account")
        super().display_details()

    def interest_rate(self):
        return self._interest_rate

    def calculate_interest(self):
        return self._balance * self._interest_rate / 100


def main():
    account = SavingsAccount("SA1001", "John Doe", 5000, 5)
    account.display_details()

    print("\nExecuting transactions:")
    account.deposit(1000)
    account.withdraw(500)

    print("\nInterest:")
    print(f"Interest at {account.interest_rate()}%: ${account.calculate_interest():,.2f}")

    print("\nAttempting to withdraw $6,000:")
    account.withdraw(6000)

    print("\nFinal balance:", account.balance_str())


if __name__ == "__main__":
    main()
