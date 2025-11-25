# Home Budget Tracker

A comprehensive household budget tracking web application with debt payoff planning, account management, and financial goal tracking.

## Features

### Account Management
- **Bank Accounts**: Track checking, savings, and money market accounts
- **Credit Cards**: Monitor balances with credit utilization indicators
- **Retirement Accounts**: Track IRA and 401(k) balances
- **Investment Accounts**: Monitor brokerage and investment holdings
- **Other Accounts**: HSA, CDs, and other financial accounts

### Budget Tracking
- Set monthly budgets by category
- Track spending against budgets
- Visual budget vs actual comparisons

### Income & Expense Tracking
- Record income from multiple sources
- Categorize expenses (Housing, Utilities, Food, Transportation, etc.)
- View spending history and trends

### Debt Management
- Track multiple debts (credit cards, student loans, mortgages, auto loans, etc.)
- Record payments and track progress
- **Debt Payoff Calculator** with two strategies:
  - **Avalanche Method**: Pay highest interest rate first (saves the most money)
  - **Snowball Method**: Pay smallest balance first (quick wins for motivation)
- See how extra payments can accelerate your debt-free date

### Savings Goals
- Create savings goals with target amounts and deadlines
- Track contributions and progress
- Visual progress indicators

### Dashboard
- **Net Worth Tracking**: See total assets vs liabilities
- Monthly income/expense summary
- Account balance overview
- Expense breakdown by category
- Budget comparison charts

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python app.py
   ```

4. Open your browser to `http://localhost:5000`

## Requirements

- Python 3.8+
- Flask 3.0.0
- Flask-SQLAlchemy 3.1.1
- Flask-CORS 4.0.0
- python-dateutil 2.8.2

## Usage

### Adding Accounts
1. Navigate to the "Accounts" tab
2. Fill in account details (name, type, institution, balance)
3. Click "Add Account"
4. Update balances periodically using the "Update" button

### Tracking Debt
1. Navigate to the "Debts" tab
2. Add your debts with principal, current balance, interest rate, and minimum payment
3. Use the "Debt Payoff" tab to calculate payoff strategies
4. Record payments as you make them

### Using the Debt Payoff Calculator
1. Add all your debts in the "Debts" tab
2. Go to the "Debt Payoff" tab
3. Select a strategy (Avalanche or Snowball)
4. Enter any extra monthly payment amount
5. Click "Calculate Payoff Plan" to see:
   - Debt-free date
   - Total interest paid
   - Money/time saved compared to minimum payments only
   - Recommended payoff order

### Setting Budgets
1. Navigate to the "Budgets" tab
2. Select a category, enter the budget amount
3. Choose the month and year
4. Click "Set Budget"
5. View budget vs actual spending on the Dashboard

## Database Schema

The application uses SQLite with the following tables:
- `account`: Track all financial accounts (bank, credit cards, retirement, investments)
- `account_transaction`: Track transactions for accounts
- `income`: Track income entries
- `expense`: Track expense entries
- `debt`: Track debt accounts
- `debt_payment`: Track payments made on debts
- `savings_goal`: Track savings goals
- `savings_contribution`: Track contributions to goals
- `budget`: Monthly budget allocations by category

## Tech Stack

- **Backend**: Flask (Python)
- **Database**: SQLite with SQLAlchemy ORM
- **Frontend**: Vanilla JavaScript, HTML5, CSS3
- **Charts**: Chart.js

## License

MIT License
