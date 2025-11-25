"""
Budget Tracker Flask Application
"""
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from datetime import datetime, date
from models import db, Account, AccountTransaction, Income, Expense, Debt, DebtPayment, SavingsGoal, SavingsContribution, Budget
from sqlalchemy import extract, func
import os
import math

app = Flask(__name__)
CORS(app)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///budget_tracker.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Create database tables
with app.app_context():
    db.create_all()


# ========== Routes ==========

@app.route('/')
def index():
    """Serve the main dashboard"""
    return render_template('index.html')


# ========== Account Endpoints ==========

@app.route('/api/accounts', methods=['GET', 'POST'])
def handle_accounts():
    """Get all accounts or add new account"""
    if request.method == 'GET':
        account_type = request.args.get('type')
        if account_type:
            accounts = Account.query.filter_by(account_type=account_type).all()
        else:
            accounts = Account.query.all()
        return jsonify([account.to_dict() for account in accounts])

    elif request.method == 'POST':
        data = request.json
        # Determine if it's an asset or liability
        is_asset = data.get('account_type') not in ['credit_card']

        account = Account(
            name=data['name'],
            account_type=data['account_type'],
            institution=data.get('institution', ''),
            balance=data.get('balance', 0),
            credit_limit=data.get('credit_limit'),
            interest_rate=data.get('interest_rate'),
            account_number_last4=data.get('account_number_last4'),
            is_asset=is_asset,
            notes=data.get('notes', '')
        )
        db.session.add(account)
        db.session.commit()
        return jsonify(account.to_dict()), 201


@app.route('/api/accounts/<int:account_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_account_item(account_id):
    """Get, update, or delete specific account"""
    account = Account.query.get_or_404(account_id)

    if request.method == 'GET':
        return jsonify(account.to_dict())

    elif request.method == 'PUT':
        data = request.json
        account.name = data.get('name', account.name)
        account.account_type = data.get('account_type', account.account_type)
        account.institution = data.get('institution', account.institution)
        account.balance = data.get('balance', account.balance)
        account.credit_limit = data.get('credit_limit', account.credit_limit)
        account.interest_rate = data.get('interest_rate', account.interest_rate)
        account.account_number_last4 = data.get('account_number_last4', account.account_number_last4)
        account.notes = data.get('notes', account.notes)
        account.is_asset = data.get('account_type', account.account_type) not in ['credit_card']
        db.session.commit()
        return jsonify(account.to_dict())

    elif request.method == 'DELETE':
        db.session.delete(account)
        db.session.commit()
        return '', 204


# ========== Account Transaction Endpoints ==========

@app.route('/api/accounts/<int:account_id>/transactions', methods=['GET', 'POST'])
def handle_account_transactions(account_id):
    """Get transactions for an account or add new transaction"""
    account = Account.query.get_or_404(account_id)

    if request.method == 'GET':
        transactions = AccountTransaction.query.filter_by(account_id=account_id).order_by(AccountTransaction.date.desc()).all()
        return jsonify([t.to_dict() for t in transactions])

    elif request.method == 'POST':
        data = request.json
        transaction = AccountTransaction(
            account_id=account_id,
            transaction_type=data['transaction_type'],
            amount=data['amount'],
            description=data.get('description', ''),
            date=datetime.fromisoformat(data['date']).date() if 'date' in data else date.today(),
            category=data.get('category')
        )

        # Update account balance
        if data['transaction_type'] in ['deposit', 'interest', 'dividend']:
            account.balance += data['amount']
        elif data['transaction_type'] in ['withdrawal', 'payment']:
            account.balance -= data['amount']

        db.session.add(transaction)
        db.session.commit()
        return jsonify(transaction.to_dict()), 201


@app.route('/api/account-types')
def get_account_types():
    """Get list of account types"""
    account_types = [
        {'value': 'checking', 'label': 'Checking Account', 'icon': 'bank'},
        {'value': 'savings', 'label': 'Savings Account', 'icon': 'piggy-bank'},
        {'value': 'credit_card', 'label': 'Credit Card', 'icon': 'credit-card'},
        {'value': 'ira', 'label': 'IRA (Individual Retirement Account)', 'icon': 'retirement'},
        {'value': '401k', 'label': '401(k)', 'icon': 'retirement'},
        {'value': 'investment', 'label': 'Investment/Brokerage', 'icon': 'chart'},
        {'value': 'hsa', 'label': 'HSA (Health Savings Account)', 'icon': 'health'},
        {'value': 'money_market', 'label': 'Money Market', 'icon': 'money'},
        {'value': 'cd', 'label': 'Certificate of Deposit (CD)', 'icon': 'certificate'},
        {'value': 'other', 'label': 'Other', 'icon': 'other'}
    ]
    return jsonify(account_types)


# ========== Net Worth Endpoint ==========

@app.route('/api/net-worth')
def get_net_worth():
    """Calculate and return net worth"""
    accounts = Account.query.all()
    debts = Debt.query.all()

    # Assets
    total_checking = sum(a.balance for a in accounts if a.account_type == 'checking')
    total_savings = sum(a.balance for a in accounts if a.account_type == 'savings')
    total_retirement = sum(a.balance for a in accounts if a.account_type in ['ira', '401k'])
    total_investments = sum(a.balance for a in accounts if a.account_type == 'investment')
    total_other_assets = sum(a.balance for a in accounts if a.account_type in ['hsa', 'money_market', 'cd', 'other'])

    # Liabilities
    total_credit_card_balance = sum(a.balance for a in accounts if a.account_type == 'credit_card')
    total_debt = sum(d.current_balance for d in debts)

    total_assets = total_checking + total_savings + total_retirement + total_investments + total_other_assets
    total_liabilities = total_credit_card_balance + total_debt
    net_worth = total_assets - total_liabilities

    return jsonify({
        'net_worth': round(net_worth, 2),
        'total_assets': round(total_assets, 2),
        'total_liabilities': round(total_liabilities, 2),
        'breakdown': {
            'assets': {
                'checking': round(total_checking, 2),
                'savings': round(total_savings, 2),
                'retirement': round(total_retirement, 2),
                'investments': round(total_investments, 2),
                'other': round(total_other_assets, 2)
            },
            'liabilities': {
                'credit_cards': round(total_credit_card_balance, 2),
                'debts': round(total_debt, 2)
            }
        },
        'accounts': [a.to_dict() for a in accounts]
    })


# ========== Debt Payoff Calculator Endpoints ==========

@app.route('/api/debt-payoff/calculate', methods=['POST'])
def calculate_debt_payoff():
    """Calculate debt payoff schedule using different strategies"""
    data = request.json
    strategy = data.get('strategy', 'avalanche')  # avalanche, snowball, or custom
    extra_payment = data.get('extra_payment', 0)

    debts = Debt.query.filter(Debt.current_balance > 0).all()

    if not debts:
        return jsonify({'error': 'No active debts found', 'schedules': []})

    # Prepare debt data
    debt_list = []
    for debt in debts:
        debt_list.append({
            'id': debt.id,
            'name': debt.name,
            'balance': debt.current_balance,
            'rate': debt.interest_rate / 100 / 12,  # Monthly rate
            'minimum': debt.minimum_payment,
            'original_balance': debt.current_balance
        })

    # Sort based on strategy
    if strategy == 'avalanche':
        # Highest interest rate first
        debt_list.sort(key=lambda x: x['rate'], reverse=True)
    elif strategy == 'snowball':
        # Lowest balance first
        debt_list.sort(key=lambda x: x['balance'])

    # Calculate payoff schedule
    schedule = calculate_payoff_schedule(debt_list, extra_payment)

    # Calculate totals
    total_interest = sum(s['total_interest'] for s in schedule)
    total_paid = sum(s['total_paid'] for s in schedule)
    payoff_months = max(s['payoff_month'] for s in schedule) if schedule else 0

    # Calculate minimum-only payoff for comparison
    min_only_schedule = calculate_payoff_schedule(
        [{'id': d['id'], 'name': d['name'], 'balance': d['original_balance'],
          'rate': d['rate'], 'minimum': d['minimum'], 'original_balance': d['original_balance']}
         for d in debt_list],
        0
    )
    min_only_interest = sum(s['total_interest'] for s in min_only_schedule)
    min_only_months = max(s['payoff_month'] for s in min_only_schedule) if min_only_schedule else 0

    return jsonify({
        'strategy': strategy,
        'extra_payment': extra_payment,
        'schedule': schedule,
        'summary': {
            'total_interest': round(total_interest, 2),
            'total_paid': round(total_paid, 2),
            'payoff_months': payoff_months,
            'payoff_date': get_future_date(payoff_months),
            'interest_saved': round(min_only_interest - total_interest, 2),
            'months_saved': min_only_months - payoff_months
        },
        'minimum_only': {
            'total_interest': round(min_only_interest, 2),
            'payoff_months': min_only_months,
            'payoff_date': get_future_date(min_only_months)
        }
    })


def calculate_payoff_schedule(debts, extra_payment):
    """Calculate month-by-month payoff schedule"""
    schedule = []

    for i, debt in enumerate(debts):
        balance = debt['balance']
        rate = debt['rate']
        minimum = debt['minimum']
        total_interest = 0
        total_paid = 0
        month = 0
        monthly_breakdown = []

        while balance > 0.01 and month < 600:  # Cap at 50 years
            month += 1

            # Calculate interest for this month
            interest = balance * rate
            total_interest += interest
            balance += interest

            # Calculate payment (minimum + extra for priority debt)
            payment = minimum
            if i == 0:  # Priority debt gets extra payment
                payment += extra_payment

            # Don't overpay
            if payment > balance:
                payment = balance

            balance -= payment
            total_paid += payment

            monthly_breakdown.append({
                'month': month,
                'payment': round(payment, 2),
                'interest': round(interest, 2),
                'principal': round(payment - interest, 2),
                'balance': round(max(0, balance), 2)
            })

        # After this debt is paid off, add the freed up minimum to extra_payment
        if balance <= 0.01:
            extra_payment += minimum

        schedule.append({
            'debt_id': debt['id'],
            'debt_name': debt['name'],
            'starting_balance': debt['original_balance'],
            'total_interest': round(total_interest, 2),
            'total_paid': round(total_paid, 2),
            'payoff_month': month,
            'monthly_breakdown': monthly_breakdown
        })

    return schedule


def get_future_date(months_from_now):
    """Get date string for N months in the future"""
    from dateutil.relativedelta import relativedelta
    future_date = date.today() + relativedelta(months=months_from_now)
    return future_date.strftime('%B %Y')


# ========== Income Endpoints ==========

@app.route('/api/income', methods=['GET', 'POST'])
def handle_income():
    """Get all income or add new income"""
    if request.method == 'GET':
        incomes = Income.query.order_by(Income.date.desc()).all()
        return jsonify([income.to_dict() for income in incomes])

    elif request.method == 'POST':
        data = request.json
        income = Income(
            amount=data['amount'],
            source=data['source'],
            date=datetime.fromisoformat(data['date']).date() if 'date' in data else date.today(),
            description=data.get('description', ''),
            account_id=data.get('account_id')
        )
        db.session.add(income)

        # If linked to an account, update balance
        if data.get('account_id'):
            account = Account.query.get(data['account_id'])
            if account:
                account.balance += data['amount']

        db.session.commit()
        return jsonify(income.to_dict()), 201


@app.route('/api/income/<int:income_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_income_item(income_id):
    """Get, update, or delete specific income"""
    income = Income.query.get_or_404(income_id)

    if request.method == 'GET':
        return jsonify(income.to_dict())

    elif request.method == 'PUT':
        data = request.json
        income.amount = data.get('amount', income.amount)
        income.source = data.get('source', income.source)
        if 'date' in data:
            income.date = datetime.fromisoformat(data['date']).date()
        income.description = data.get('description', income.description)
        db.session.commit()
        return jsonify(income.to_dict())

    elif request.method == 'DELETE':
        db.session.delete(income)
        db.session.commit()
        return '', 204


# ========== Expense Endpoints ==========

@app.route('/api/expenses', methods=['GET', 'POST'])
def handle_expenses():
    """Get all expenses or add new expense"""
    if request.method == 'GET':
        expenses = Expense.query.order_by(Expense.date.desc()).all()
        return jsonify([expense.to_dict() for expense in expenses])

    elif request.method == 'POST':
        data = request.json
        expense = Expense(
            amount=data['amount'],
            category=data['category'],
            date=datetime.fromisoformat(data['date']).date() if 'date' in data else date.today(),
            description=data.get('description', ''),
            account_id=data.get('account_id')
        )
        db.session.add(expense)

        # If linked to an account, update balance
        if data.get('account_id'):
            account = Account.query.get(data['account_id'])
            if account:
                account.balance -= data['amount']

        db.session.commit()
        return jsonify(expense.to_dict()), 201


@app.route('/api/expenses/<int:expense_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_expense_item(expense_id):
    """Get, update, or delete specific expense"""
    expense = Expense.query.get_or_404(expense_id)

    if request.method == 'GET':
        return jsonify(expense.to_dict())

    elif request.method == 'PUT':
        data = request.json
        expense.amount = data.get('amount', expense.amount)
        expense.category = data.get('category', expense.category)
        if 'date' in data:
            expense.date = datetime.fromisoformat(data['date']).date()
        expense.description = data.get('description', expense.description)
        db.session.commit()
        return jsonify(expense.to_dict())

    elif request.method == 'DELETE':
        db.session.delete(expense)
        db.session.commit()
        return '', 204


# ========== Debt Endpoints ==========

@app.route('/api/debts', methods=['GET', 'POST'])
def handle_debts():
    """Get all debts or add new debt"""
    if request.method == 'GET':
        debts = Debt.query.all()
        return jsonify([debt.to_dict() for debt in debts])

    elif request.method == 'POST':
        data = request.json
        debt = Debt(
            name=data['name'],
            debt_type=data.get('debt_type', 'other'),
            principal=data['principal'],
            current_balance=data.get('current_balance', data['principal']),
            interest_rate=data['interest_rate'],
            minimum_payment=data['minimum_payment'],
            due_date=data.get('due_date')
        )
        db.session.add(debt)
        db.session.commit()
        return jsonify(debt.to_dict()), 201


@app.route('/api/debts/<int:debt_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_debt_item(debt_id):
    """Get, update, or delete specific debt"""
    debt = Debt.query.get_or_404(debt_id)

    if request.method == 'GET':
        return jsonify(debt.to_dict())

    elif request.method == 'PUT':
        data = request.json
        debt.name = data.get('name', debt.name)
        debt.debt_type = data.get('debt_type', debt.debt_type)
        debt.principal = data.get('principal', debt.principal)
        debt.current_balance = data.get('current_balance', debt.current_balance)
        debt.interest_rate = data.get('interest_rate', debt.interest_rate)
        debt.minimum_payment = data.get('minimum_payment', debt.minimum_payment)
        debt.due_date = data.get('due_date', debt.due_date)
        db.session.commit()
        return jsonify(debt.to_dict())

    elif request.method == 'DELETE':
        db.session.delete(debt)
        db.session.commit()
        return '', 204


# ========== Debt Payment Endpoints ==========

@app.route('/api/debts/<int:debt_id>/payments', methods=['GET', 'POST'])
def handle_debt_payments(debt_id):
    """Get payments for a debt or add new payment"""
    debt = Debt.query.get_or_404(debt_id)

    if request.method == 'GET':
        payments = DebtPayment.query.filter_by(debt_id=debt_id).order_by(DebtPayment.date.desc()).all()
        return jsonify([payment.to_dict() for payment in payments])

    elif request.method == 'POST':
        data = request.json
        payment = DebtPayment(
            debt_id=debt_id,
            amount=data['amount'],
            date=datetime.fromisoformat(data['date']).date() if 'date' in data else date.today(),
            description=data.get('description', '')
        )
        # Update debt balance
        debt.current_balance -= data['amount']
        db.session.add(payment)
        db.session.commit()
        return jsonify(payment.to_dict()), 201


# ========== Savings Goals Endpoints ==========

@app.route('/api/savings-goals', methods=['GET', 'POST'])
def handle_savings_goals():
    """Get all savings goals or add new goal"""
    if request.method == 'GET':
        goals = SavingsGoal.query.all()
        return jsonify([goal.to_dict() for goal in goals])

    elif request.method == 'POST':
        data = request.json
        goal = SavingsGoal(
            name=data['name'],
            target_amount=data['target_amount'],
            current_amount=data.get('current_amount', 0),
            deadline=datetime.fromisoformat(data['deadline']).date() if 'deadline' in data and data['deadline'] else None
        )
        db.session.add(goal)
        db.session.commit()
        return jsonify(goal.to_dict()), 201


@app.route('/api/savings-goals/<int:goal_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_savings_goal_item(goal_id):
    """Get, update, or delete specific savings goal"""
    goal = SavingsGoal.query.get_or_404(goal_id)

    if request.method == 'GET':
        return jsonify(goal.to_dict())

    elif request.method == 'PUT':
        data = request.json
        goal.name = data.get('name', goal.name)
        goal.target_amount = data.get('target_amount', goal.target_amount)
        goal.current_amount = data.get('current_amount', goal.current_amount)
        if 'deadline' in data and data['deadline']:
            goal.deadline = datetime.fromisoformat(data['deadline']).date()
        db.session.commit()
        return jsonify(goal.to_dict())

    elif request.method == 'DELETE':
        db.session.delete(goal)
        db.session.commit()
        return '', 204


# ========== Savings Contributions Endpoints ==========

@app.route('/api/savings-goals/<int:goal_id>/contributions', methods=['GET', 'POST'])
def handle_savings_contributions(goal_id):
    """Get contributions for a goal or add new contribution"""
    goal = SavingsGoal.query.get_or_404(goal_id)

    if request.method == 'GET':
        contributions = SavingsContribution.query.filter_by(goal_id=goal_id).order_by(SavingsContribution.date.desc()).all()
        return jsonify([contrib.to_dict() for contrib in contributions])

    elif request.method == 'POST':
        data = request.json
        contribution = SavingsContribution(
            goal_id=goal_id,
            amount=data['amount'],
            date=datetime.fromisoformat(data['date']).date() if 'date' in data else date.today(),
            description=data.get('description', '')
        )
        # Update goal amount
        goal.current_amount += data['amount']
        db.session.add(contribution)
        db.session.commit()
        return jsonify(contribution.to_dict()), 201


# ========== Budget Endpoints ==========

@app.route('/api/budgets', methods=['GET', 'POST'])
def handle_budgets():
    """Get budgets or add new budget"""
    if request.method == 'GET':
        month = request.args.get('month', datetime.now().month, type=int)
        year = request.args.get('year', datetime.now().year, type=int)
        budgets = Budget.query.filter_by(month=month, year=year).all()
        return jsonify([budget.to_dict() for budget in budgets])

    elif request.method == 'POST':
        data = request.json
        # Check if budget already exists
        existing = Budget.query.filter_by(
            category=data['category'],
            month=data['month'],
            year=data['year']
        ).first()

        if existing:
            existing.amount = data['amount']
            db.session.commit()
            return jsonify(existing.to_dict())
        else:
            budget = Budget(
                category=data['category'],
                amount=data['amount'],
                month=data['month'],
                year=data['year']
            )
            db.session.add(budget)
            db.session.commit()
            return jsonify(budget.to_dict()), 201


@app.route('/api/budgets/<int:budget_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_budget_item(budget_id):
    """Get, update, or delete specific budget"""
    budget = Budget.query.get_or_404(budget_id)

    if request.method == 'GET':
        return jsonify(budget.to_dict())

    elif request.method == 'PUT':
        data = request.json
        budget.category = data.get('category', budget.category)
        budget.amount = data.get('amount', budget.amount)
        budget.month = data.get('month', budget.month)
        budget.year = data.get('year', budget.year)
        db.session.commit()
        return jsonify(budget.to_dict())

    elif request.method == 'DELETE':
        db.session.delete(budget)
        db.session.commit()
        return '', 204


# ========== Dashboard/Analytics Endpoints ==========

@app.route('/api/dashboard')
def dashboard():
    """Get dashboard summary data"""
    now = datetime.now()
    current_month = now.month
    current_year = now.year

    # Monthly income
    monthly_income = db.session.query(func.sum(Income.amount)).filter(
        extract('month', Income.date) == current_month,
        extract('year', Income.date) == current_year
    ).scalar() or 0

    # Monthly expenses
    monthly_expenses = db.session.query(func.sum(Expense.amount)).filter(
        extract('month', Expense.date) == current_month,
        extract('year', Expense.date) == current_year
    ).scalar() or 0

    # Expenses by category for current month
    expenses_by_category = db.session.query(
        Expense.category,
        func.sum(Expense.amount).label('total')
    ).filter(
        extract('month', Expense.date) == current_month,
        extract('year', Expense.date) == current_year
    ).group_by(Expense.category).all()

    # Total debt
    total_debt = db.session.query(func.sum(Debt.current_balance)).scalar() or 0

    # Debts list
    debts = Debt.query.all()

    # Savings goals
    savings_goals = SavingsGoal.query.all()
    total_savings = sum(goal.current_amount for goal in savings_goals)

    # Account totals
    accounts = Account.query.all()
    total_cash = sum(a.balance for a in accounts if a.account_type in ['checking', 'savings'])
    total_retirement = sum(a.balance for a in accounts if a.account_type in ['ira', '401k'])
    total_investments = sum(a.balance for a in accounts if a.account_type == 'investment')
    total_credit_balance = sum(a.balance for a in accounts if a.account_type == 'credit_card')

    # Net worth
    total_assets = sum(a.balance for a in accounts if a.is_asset)
    total_liabilities = total_credit_balance + total_debt
    net_worth = total_assets - total_liabilities

    # Budget comparison
    budgets = Budget.query.filter_by(month=current_month, year=current_year).all()
    budget_comparison = []
    for budget in budgets:
        spent = db.session.query(func.sum(Expense.amount)).filter(
            Expense.category == budget.category,
            extract('month', Expense.date) == current_month,
            extract('year', Expense.date) == current_year
        ).scalar() or 0

        budget_comparison.append({
            'category': budget.category,
            'budgeted': budget.amount,
            'spent': spent,
            'remaining': budget.amount - spent,
            'percentage': round((spent / budget.amount * 100) if budget.amount > 0 else 0, 2)
        })

    return jsonify({
        'monthly_income': round(monthly_income, 2),
        'monthly_expenses': round(monthly_expenses, 2),
        'net_monthly': round(monthly_income - monthly_expenses, 2),
        'expenses_by_category': [{'category': cat, 'amount': round(amt, 2)} for cat, amt in expenses_by_category],
        'total_debt': round(total_debt, 2),
        'debts': [debt.to_dict() for debt in debts],
        'total_savings': round(total_savings, 2),
        'savings_goals': [goal.to_dict() for goal in savings_goals],
        'budget_comparison': budget_comparison,
        'net_worth': round(net_worth, 2),
        'total_cash': round(total_cash, 2),
        'total_retirement': round(total_retirement, 2),
        'total_investments': round(total_investments, 2),
        'total_credit_balance': round(total_credit_balance, 2),
        'accounts': [a.to_dict() for a in accounts]
    })


@app.route('/api/categories')
def get_categories():
    """Get list of expense categories"""
    categories = [
        'Housing', 'Utilities', 'Food & Groceries', 'Transportation',
        'Healthcare', 'Insurance', 'Entertainment', 'Shopping',
        'Dining Out', 'Personal Care', 'Education', 'Savings',
        'Debt Payment', 'Other'
    ]
    return jsonify(categories)


@app.route('/api/debt-types')
def get_debt_types():
    """Get list of debt types"""
    debt_types = [
        {'value': 'credit_card', 'label': 'Credit Card'},
        {'value': 'student_loan', 'label': 'Student Loan'},
        {'value': 'mortgage', 'label': 'Mortgage'},
        {'value': 'auto_loan', 'label': 'Auto Loan'},
        {'value': 'personal_loan', 'label': 'Personal Loan'},
        {'value': 'medical', 'label': 'Medical Debt'},
        {'value': 'other', 'label': 'Other'}
    ]
    return jsonify(debt_types)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
