## Money Exchange System Activity Diagrams

### Number of diagrams

3 activity diagrams is the best number for for the current Money Exchange System. The project allows a system operator to manage customers, currencies, exchange rates, and currency exchange transactions.

The diagrams are:

1. Exchange currency: shows how the operator creates a currency exchange transaction
2. Manage customers, currencies, and exchange rates: shows the shared process for adding or removing the main system data
3. View data and remove a transaction: shows how the operator reviews stored data and, when needed, deletes a transaction

### Diagram 1. Exchange currency

This diagram shows the main exchange process. The operator enters the customer, currencies, and amount. The system checks the information, finds the latest direct or reverse rate, calculates the result, and saves the transaction. If any required information or rate is missing, the operator sees an error.

```mermaid
swimlane-beta TB
  accTitle: Exchange currency activity

  subgraph operator [System Operator]
    ex_start([Start])
    ex_enter[Enter customer, currencies, and amount]
    ex_result[View converted amount and rate]
    ex_error[View error message]
    ex_end([End])
  end

  subgraph system [Money Exchange System]
    ex_validate[Validate the entered values]
    ex_valid{Are the values valid?}
    ex_records{Do the customer and currencies exist?}
    ex_rate{Is a direct or reverse rate available?}
    ex_calculate[Calculate the converted amount]
  end

  subgraph database [Database]
    ex_check[Look up customer and currencies]
    ex_find_rate[Find the latest exchange rate]
    ex_save[Save the transaction]
  end

  ex_start --> ex_enter -->|Exchange request| ex_validate --> ex_valid
  ex_valid -->|No| ex_error --> ex_end
  ex_valid -->|Yes| ex_check -->|Lookup result| ex_records
  ex_records -->|No| ex_error
  ex_records -->|Yes| ex_find_rate -->|Rate lookup result| ex_rate
  ex_rate -->|No| ex_error
  ex_rate -->|Yes| ex_calculate -->|Transaction details| ex_save
  ex_save -->|Saved transaction| ex_result --> ex_end
```

### Diagram 2. Manage customers, currencies, and exchange rates

This diagram represents the common maintenance process for customers, currencies, and exchange rates. The operator chooses the type of data and then chooses to add or remove it. New information must be valid before it is saved. 

```mermaid
swimlane-beta TB
  accTitle: Manage reference data activity

  subgraph operator [System Operator]
    mg_start([Start])
    mg_choose[Choose customer, currency, or exchange rate]
    mg_action{Add or remove?}
    mg_details[Enter new item details]
    mg_id[Enter item identifier]
    mg_success[View success]
    mg_error[View error message]
    mg_end([End])
  end

  subgraph system [Money Exchange System]
    mg_validate[Validate and normalise details]
    mg_valid{Are the details valid?}
    mg_can_remove{Does the item exist and can it be removed?}
  end

  subgraph database [Database]
    mg_save[Save the new item]
    mg_check[Find the existing item and related records]
    mg_delete[Delete the item]
  end

  mg_start --> mg_choose --> mg_action
  mg_action -->|Add| mg_details -->|New details| mg_validate --> mg_valid
  mg_valid -->|No| mg_error --> mg_end
  mg_valid -->|Yes| mg_save -->|Item saved| mg_success --> mg_end
  mg_action -->|Remove| mg_id -->|Item identifier| mg_check
  mg_check -->|Check result| mg_can_remove
  mg_can_remove -->|No| mg_error
  mg_can_remove -->|Yes| mg_delete -->|Item deleted| mg_success
```

### Diagram 3. View data and remove a transaction

This diagram shows the transaction review process. The operator can view all customers, currencies, rates, and transactions. After reviewing the information, the operator may finish or enter a transaction ID to remove a transaction. 

```mermaid
swimlane-beta TB
  accTitle: View data and remove a transaction activity

  subgraph operator [System Operator]
    tx_start([Start])
    tx_request[Choose Show all data]
    tx_view[View customers, currencies, rates, and transactions]
    tx_remove{Remove a transaction?}
    tx_id[Enter transaction ID]
    tx_success[View success]
    tx_error[View error message]
    tx_end([End])
  end

  subgraph system [Money Exchange System]
    tx_get[Request all stored data]
    tx_format[Prepare data for display]
    tx_exists{Does the transaction exist?}
  end

  subgraph database [Database]
    tx_read[Read all four data tables]
    tx_find[Find the transaction]
    tx_delete[Delete the transaction]
  end

  tx_start --> tx_request -->|Data request| tx_get --> tx_read
  tx_read -->|Stored records| tx_format -->|Display data| tx_view
  tx_view --> tx_remove
  tx_remove -->|No| tx_end
  tx_remove -->|Yes| tx_id -->|Transaction ID| tx_find
  tx_find -->|Lookup result| tx_exists
  tx_exists -->|No| tx_error --> tx_end
  tx_exists -->|Yes| tx_delete -->|Transaction deleted| tx_success --> tx_end
```
