from abc import ABC, abstractmethod

class ATM(ABC):
    @abstractmethod
    def insert_card(self):
        pass

    @abstractmethod
    def enter_pin(self):
        pass

    @abstractmethod
    def balance(self):
        pass

    @abstractmethod
    def withdraw(self, amount):
        pass


class BankATM(ATM):
    def __init__(self, pin, balance):
        self._pin = pin
        self._balance = balance
        self._card_inserted = False
        self._authenticated = False

    def insert_card(self):
        self._card_inserted = True
        self._authenticated = False
        print("Card inserted.")

    def enter_pin(self):
        if not self._card_inserted:
            print("Please insert your card first.")
            return
        pin = input("Enter your PIN: ")
        self._authenticated = pin == self._pin
        if self._authenticated:
            print("PIN accepted.")
        else:
            print("Incorrect PIN.")

    def balance(self):
        if not self._authenticated:
            print("Please enter a valid PIN first.")
            return
        print(f"Balance: ${self._balance:,.2f}")

    def withdraw(self, amount):
        if not self._authenticated:
            print("Please enter a valid PIN first.")
            return
        if amount <= 0:
            print("Withdrawal amount must be positive.")
            return
        if amount > self._balance:
            print("Insufficient funds.")
            return
        self._balance -= amount
        print(f"Withdrawn: ${amount:,.2f}")


def main():
    atm: ATM = BankATM(pin="1234", balance=1000)
    print("ATM demonstration (sample PIN: 1234)")
    atm.insert_card()
    atm.enter_pin()
    atm.balance()
    atm.withdraw(200)
    atm.balance()


if __name__ == "__main__":
    main()
