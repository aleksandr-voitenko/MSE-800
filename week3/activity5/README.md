Activity 5. Currency Exchange Project

Task:
> Design ER diagram and develop a database for the money exchange project (with at least three entities and OOP style). In a README file, clearly describe how many tables you have created and justify why each table is necessary.

Project scope:
> The Money Exchange System should allow a exchange business to manage customers, currencies, exchange rates, and currency exchange transactions

## ER model

```mermaid
erDiagram
    CUSTOMERS ||--o{ TRANSACTIONS : makes
    EXCHANGE_RATES ||--o{ TRANSACTIONS : "used by"
    CURRENCIES ||--o{ EXCHANGE_RATES : "source for"
    CURRENCIES ||--o{ EXCHANGE_RATES : "target for"

    CUSTOMERS {
        INTEGER customer_id PK
        TEXT first_name
        TEXT last_name
        TEXT national_id
    }

    TRANSACTIONS {
        INTEGER transaction_id PK
        INTEGER customer_id FK
        INTEGER exchange_rate_id FK
        REAL amount_from
        REAL amount_to
        TEXT date_time "(YYYY-MM-DD HH:MM:SS.SSS)"
    }

    EXCHANGE_RATES {
        INTEGER exchange_rate_id PK
        TEXT currency_code_from FK
        TEXT currency_code_to FK
        REAL rate
        TEXT effective_at "(YYYY-MM-DD HH:MM:SS.SSS)"
    }

    CURRENCIES {
        TEXT code PK
        TEXT name
        TEXT symbol
    }
```

## Tables Description

The database contains `4` `CUSTOMERS`, `CURRENCIES`, `EXCHANGE_RATES`, and `TRANSACTIONS`.

The `CUSTOMERS` table stores information about people who use the exchange service.  This table is necessary because the business needs to know who makes each exchange transaction. 

The `CURRENCIES` table stores the currencies supported by the exchange business, such as NZD, USD, EUR, and GBP. It contains information such as the currency code, name, and symbol.

This table is necessary because the system needs a single place to store information about each currency.

The `EXCHANGE_RATES` table stores the exchange rate between two currencies. Each record identifies the source currency, the target currency, and the rate used to convert one currency into another.

This table is necessary because exchange rates are an important part of every currency exchange. Storing them separately allows the system to manage different currency pairs and keep a record of the rates used by the business.

The `TRANSACTIONS` table stores each currency exchange made by a customer. It connects a customer with the exchange rate used for the transaction and stores the exchanged amount.

This table is necessary because the business needs to keep a history of completed exchanges. It allows the system to see which customer made a transaction, which currencies and exchange rate were involved, and how much money was exchanged.
