# resale_profit_manager
**resale_profit_manager** - it's an application that allows you to account your resales, for example: digital goods, stocks, bonds, cryptocurrencies, other goods.
## How does this work?
1. Login or Register
2. Add ticket on Home page
3. You can add ticket with or without field `Sold`
4. If `Sold` field filled then ticket is complete
5. If `Sold` field not filled then your ticket will be in `Waiting` filter
6. You can edit ticket by clicking on it
7. Profit calculated after `Sold` field filled
## Commands
Commands for committing into models constants for tickets filters and user settings

```cd backend```

```python manage.py command_filter_query```

```python manage.py command_settings_query```