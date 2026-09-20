from abc import ABC, abstractmethod

class PaymentService:
    @abstractmethod
    def pay(self, amount):
        pass

class OldPaymentSystem:
    def make_payment(self, amount):
        print(f"Payment of ${amount} made using Old Payment System.")

class PaymentAdapter(PaymentService):
    def __init__(self, old_payment_system):
        self.old_payment_system = old_payment_system

    def pay(self, amount):
        self.old_payment_system.make_payment(amount)

class InheritancePaymentAdapter(PaymentService, OldPaymentSystem):
    def pay(self, amount):
        self.make_payment(amount)


def main():
    # Composition example
    old_system = OldPaymentSystem()
    adapter = PaymentAdapter(old_system)
    adapter.pay(500)

    # Multiple inheritance example
    inheritance_adapter = InheritancePaymentAdapter()
    inheritance_adapter.pay(500)


if __name__ == "__main__":
    main()
