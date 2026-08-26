The Currency Exchange System is represented with **two class diagrams**. The domain model is separate from the implementation architecture so that the business relationships remain easy to read while the second diagram can show the application's technical layers and dependencies.

### Domain Model

Covers `Customer`, `Currency`, `ExchangeRate`, and `Transaction`, including multiplicities and source/target currency relationships.

`Customer` identifies the person making an
exchange. `Currency` defines a supported currency. `ExchangeRate` records a
dated rate from one currency to another. `Transaction` records the customer,
rate, input amount, calculated output amount, actual direction, effective rate,
and completion time.

<img width="600" alt="domain_model" src="https://github.com/user-attachments/assets/496475b0-eb66-4321-9c33-e09bb54e1c08" />

### Application Architecture

Shows how classes collaborate across the presentation, service, persistence, domain-model, and error-handling layers.

`ConsoleApplication` collects input and displays results. It provide UI and UX in the app. `MoneyExchangeSystem` is the public facade. It normalizes and validates data, chooses the latest direct or reverse rate, calculates the converted amount, and coordinates CRUD operations. `MoneyExchangeDatabase` encapsulates SQLite schema creation, queries, mapping, and referential-integrity errors. The four frozen dataclasses carry results between layers. `MoneyExchangeError` is the application's base exception, and `ExchangeRateNotAvailableError` specializes it for missing direct/reverse rates.


<img width="1581" height="1615" alt="architecture" src="https://github.com/user-attachments/assets/6395127b-9a8a-40ad-8afc-a5fc1d6af7fc" />
