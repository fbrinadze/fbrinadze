"""
Budget Tracker Flask Application
"""
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from datetime import datetime, date
from models import db, Income, Expense, Debt, DebtPayment, SavingsGoal, SavingsContribution, Budget
from sqlalchemy import extract, func
import os

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
            description=data.get('description', '')
        )
        db.session.add(income)
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
            description=data.get('description', '')
        )
        db.session.add(expense)
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
        'budget_comparison': budget_comparison
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


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
