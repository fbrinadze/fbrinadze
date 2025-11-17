# Home Budget Tracker

A comprehensive budget tracking application to help decrease debt and save money.

## Features

- **Income & Expense Tracking**: Track all your income sources and expenses with categorization
- **Budget Management**: Set monthly budgets by category and track spending against them
- **Debt Tracking**: Monitor multiple debts with principal, interest rates, and payment schedules
- **Savings Goals**: Set and track progress toward savings goals
- **Visualizations**: Charts and graphs to visualize spending patterns, debt payoff progress, and savings
- **Dashboard**: Overview of your financial health at a glance

## Technology Stack

- **Backend**: Python Flask
- **Database**: SQLite
- **Frontend**: HTML5, CSS3, JavaScript
- **Charts**: Chart.js for data visualization

## Installation

1. Clone the repository
2. Install Python 3.8 or higher
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

1. Start the Flask server:
   ```bash
   python app.py
   ```

2. Open your browser and navigate to:
   ```
   http://localhost:5000
   ```

## Usage

### Dashboard
View your overall financial summary including:
- Total monthly income vs expenses
- Current debt balances
- Savings progress
- Budget category spending

### Expenses
- Add new expenses with amount, category, date, and description
- View expense history
- Filter by date range and category

### Income
- Track income sources
- View income history

### Debts
- Add debts with name, principal, interest rate, and minimum payment
- Track payment progress
- View debt payoff projections

### Savings Goals
- Create savings goals with target amounts and deadlines
- Track contributions
- Monitor progress

### Budgets
- Set monthly budgets for different categories
- View spending vs budget comparisons
- Get alerts when approaching budget limits

## Database Schema

The application uses SQLite with the following tables:
- `income`: Track income entries
- `expenses`: Track expense entries
- `debts`: Track debt accounts
- `debt_payments`: Track payments made on debts
- `savings_goals`: Track savings goals
- `savings_contributions`: Track contributions to goals
- `budgets`: Monthly budget allocations by category

## License

MIT License
