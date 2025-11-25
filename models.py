"""
Database models for the Budget Tracker application
"""
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Account(db.Model):
    """Track financial accounts - bank accounts, credit cards, IRA, 401k"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    account_type = db.Column(db.String(50), nullable=False)  # checking, savings, credit_card, ira, 401k, investment
    institution = db.Column(db.String(100))  # Bank/Brokerage name
    balance = db.Column(db.Float, nullable=False, default=0)
    credit_limit = db.Column(db.Float)  # For credit cards
    interest_rate = db.Column(db.Float)  # APY for savings, APR for credit cards
    account_number_last4 = db.Column(db.String(4))  # Last 4 digits for reference
    is_asset = db.Column(db.Boolean, default=True)  # True for assets, False for liabilities (credit cards)
    notes = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    transactions = db.relationship('AccountTransaction', backref='account', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'account_type': self.account_type,
            'institution': self.institution,
            'balance': self.balance,
            'credit_limit': self.credit_limit,
            'interest_rate': self.interest_rate,
            'account_number_last4': self.account_number_last4,
            'is_asset': self.is_asset,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class AccountTransaction(db.Model):
    """Track transactions for accounts"""
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    transaction_type = db.Column(db.String(50), nullable=False)  # deposit, withdrawal, transfer, interest, dividend
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200))
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    category = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'account_id': self.account_id,
            'transaction_type': self.transaction_type,
            'amount': self.amount,
            'description': self.description,
            'date': self.date.isoformat() if self.date else None,
            'category': self.category,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Income(db.Model):
    """Track income entries"""
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    source = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    description = db.Column(db.String(200))
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'))  # Optional: link to account
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'amount': self.amount,
            'source': self.source,
            'date': self.date.isoformat() if self.date else None,
            'description': self.description,
            'account_id': self.account_id,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Expense(db.Model):
    """Track expense entries"""
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    description = db.Column(db.String(200))
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'))  # Optional: link to account
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'amount': self.amount,
            'category': self.category,
            'date': self.date.isoformat() if self.date else None,
            'description': self.description,
            'account_id': self.account_id,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Debt(db.Model):
    """Track debt accounts"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    debt_type = db.Column(db.String(50), default='other')  # credit_card, student_loan, mortgage, auto_loan, personal_loan, other
    principal = db.Column(db.Float, nullable=False)
    current_balance = db.Column(db.Float, nullable=False)
    interest_rate = db.Column(db.Float, nullable=False)  # Annual percentage rate
    minimum_payment = db.Column(db.Float, nullable=False)
    due_date = db.Column(db.Integer)  # Day of month (1-31)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    payments = db.relationship('DebtPayment', backref='debt', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        total_paid = sum(p.amount for p in self.payments)
        return {
            'id': self.id,
            'name': self.name,
            'debt_type': self.debt_type,
            'principal': self.principal,
            'current_balance': self.current_balance,
            'interest_rate': self.interest_rate,
            'minimum_payment': self.minimum_payment,
            'due_date': self.due_date,
            'total_paid': total_paid,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class DebtPayment(db.Model):
    """Track payments made on debts"""
    id = db.Column(db.Integer, primary_key=True)
    debt_id = db.Column(db.Integer, db.ForeignKey('debt.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    description = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'debt_id': self.debt_id,
            'amount': self.amount,
            'date': self.date.isoformat() if self.date else None,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class SavingsGoal(db.Model):
    """Track savings goals"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    target_amount = db.Column(db.Float, nullable=False)
    current_amount = db.Column(db.Float, default=0)
    deadline = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    contributions = db.relationship('SavingsContribution', backref='goal', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        progress = (self.current_amount / self.target_amount * 100) if self.target_amount > 0 else 0
        return {
            'id': self.id,
            'name': self.name,
            'target_amount': self.target_amount,
            'current_amount': self.current_amount,
            'deadline': self.deadline.isoformat() if self.deadline else None,
            'progress': round(progress, 2),
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class SavingsContribution(db.Model):
    """Track contributions to savings goals"""
    id = db.Column(db.Integer, primary_key=True)
    goal_id = db.Column(db.Integer, db.ForeignKey('savings_goal.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    description = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'goal_id': self.goal_id,
            'amount': self.amount,
            'date': self.date.isoformat() if self.date else None,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Budget(db.Model):
    """Track monthly budgets by category"""
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    month = db.Column(db.Integer, nullable=False)  # 1-12
    year = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Ensure unique budget per category per month
    __table_args__ = (db.UniqueConstraint('category', 'month', 'year', name='_category_month_year_uc'),)

    def to_dict(self):
        return {
            'id': self.id,
            'category': self.category,
            'amount': self.amount,
            'month': self.month,
            'year': self.year,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
