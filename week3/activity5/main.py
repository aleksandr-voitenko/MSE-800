from pathlib import Path

from console_ui import ConsoleApplication
from money_exchange.system import MoneyExchangeSystem

DB_PATH = Path(__file__).with_name("money_exchange.db")

# Application's entry point
def main() -> None:
    system = MoneyExchangeSystem(DB_PATH)

    try:
        ConsoleApplication(system).run()
    finally:
        system.close()

if __name__ == "__main__":
    main()
