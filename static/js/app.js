// Budget Tracker Application
const API_BASE = '/api';

// Utility Functions
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}

function formatDate(dateString) {
    const options = { year: 'numeric', month: 'short', day: 'numeric' };
    return new Date(dateString).toLocaleDateString('en-US', options);
}

function getTodayDate() {
    return new Date().toISOString().split('T')[0];
}

// Tab Navigation
function showTab(tabName) {
    // Hide all tabs
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });

    // Show selected tab
    document.getElementById(tabName).classList.add('active');
    event.target.classList.add('active');

    // Load data for the tab
    if (tabName === 'dashboard') {
        loadDashboard();
    } else if (tabName === 'income') {
        loadIncome();
    } else if (tabName === 'expenses') {
        loadExpenses();
    } else if (tabName === 'budgets') {
        loadBudgets();
    } else if (tabName === 'debts') {
        loadDebts();
    } else if (tabName === 'savings') {
        loadSavingsGoals();
    }
}

// Initialize App
document.addEventListener('DOMContentLoaded', function() {
    // Set default dates
    document.querySelectorAll('input[type="date"]').forEach(input => {
        input.value = getTodayDate();
    });

    // Set current month and year for budgets
    const now = new Date();
    document.getElementById('budget-month').value = now.getMonth() + 1;
    document.getElementById('budget-year').value = now.getFullYear();

    // Load categories
    loadCategories();

    // Load initial dashboard
    loadDashboard();

    // Setup form handlers
    setupFormHandlers();

    // Setup modal handlers
    setupModalHandlers();
});

// Load Categories
async function loadCategories() {
    try {
        const response = await fetch(`${API_BASE}/categories`);
        const categories = await response.json();

        const expenseCategory = document.getElementById('expense-category');
        const budgetCategory = document.getElementById('budget-category');

        categories.forEach(cat => {
            expenseCategory.add(new Option(cat, cat));
            budgetCategory.add(new Option(cat, cat));
        });
    } catch (error) {
        console.error('Error loading categories:', error);
    }
}

// Dashboard Functions
async function loadDashboard() {
    try {
        const response = await fetch(`${API_BASE}/dashboard`);
        const data = await response.json();

        // Update summary cards
        document.getElementById('monthly-income').textContent = formatCurrency(data.monthly_income);
        document.getElementById('monthly-expenses').textContent = formatCurrency(data.monthly_expenses);

        const netMonthly = document.getElementById('net-monthly');
        netMonthly.textContent = formatCurrency(data.net_monthly);
        netMonthly.className = 'amount ' + (data.net_monthly >= 0 ? 'positive' : 'negative');

        document.getElementById('total-debt').textContent = formatCurrency(data.total_debt);
        document.getElementById('total-savings').textContent = formatCurrency(data.total_savings);

        // Update charts
        updateExpensesChart(data.expenses_by_category);
        updateBudgetChart(data.budget_comparison);

        // Update debts summary
        updateDebtsSummary(data.debts);

        // Update savings summary
        updateSavingsSummary(data.savings_goals);
    } catch (error) {
        console.error('Error loading dashboard:', error);
    }
}

let expensesChart, budgetChart;

function updateExpensesChart(expensesByCategory) {
    const ctx = document.getElementById('expenses-chart').getContext('2d');

    if (expensesChart) {
        expensesChart.destroy();
    }

    if (expensesByCategory.length === 0) {
        return;
    }

    expensesChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: expensesByCategory.map(e => e.category),
            datasets: [{
                data: expensesByCategory.map(e => e.amount),
                backgroundColor: [
                    '#667eea', '#764ba2', '#f093fb', '#4facfe',
                    '#43e97b', '#fa709a', '#fee140', '#30cfd0'
                ]
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    });
}

function updateBudgetChart(budgetComparison) {
    const ctx = document.getElementById('budget-chart').getContext('2d');

    if (budgetChart) {
        budgetChart.destroy();
    }

    if (budgetComparison.length === 0) {
        return;
    }

    budgetChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: budgetComparison.map(b => b.category),
            datasets: [{
                label: 'Budgeted',
                data: budgetComparison.map(b => b.budgeted),
                backgroundColor: '#667eea'
            }, {
                label: 'Spent',
                data: budgetComparison.map(b => b.spent),
                backgroundColor: '#764ba2'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            },
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

function updateDebtsSummary(debts) {
    const container = document.getElementById('debts-summary');

    if (debts.length === 0) {
        container.innerHTML = '<div class="empty-state"><p>No active debts</p></div>';
        return;
    }

    container.innerHTML = debts.map(debt => `
        <div class="list-item">
            <div class="list-item-content">
                <div class="list-item-title">${debt.name}</div>
                <div class="list-item-details">
                    Balance: ${formatCurrency(debt.current_balance)} |
                    Rate: ${debt.interest_rate}% |
                    Min Payment: ${formatCurrency(debt.minimum_payment)}
                </div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: ${((debt.principal - debt.current_balance) / debt.principal * 100)}%">
                        ${Math.round((debt.principal - debt.current_balance) / debt.principal * 100)}%
                    </div>
                </div>
            </div>
        </div>
    `).join('');
}

function updateSavingsSummary(goals) {
    const container = document.getElementById('savings-summary');

    if (goals.length === 0) {
        container.innerHTML = '<div class="empty-state"><p>No savings goals</p></div>';
        return;
    }

    container.innerHTML = goals.map(goal => `
        <div class="list-item">
            <div class="list-item-content">
                <div class="list-item-title">${goal.name}</div>
                <div class="list-item-details">
                    ${formatCurrency(goal.current_amount)} of ${formatCurrency(goal.target_amount)}
                    ${goal.deadline ? ' | Deadline: ' + formatDate(goal.deadline) : ''}
                </div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: ${goal.progress}%">
                        ${goal.progress}%
                    </div>
                </div>
            </div>
        </div>
    `).join('');
}

// Income Functions
async function loadIncome() {
    try {
        const response = await fetch(`${API_BASE}/income`);
        const incomes = await response.json();

        const container = document.getElementById('income-list');

        if (incomes.length === 0) {
            container.innerHTML = '<div class="empty-state"><p>No income recorded</p></div>';
            return;
        }

        container.innerHTML = incomes.map(income => `
            <div class="list-item">
                <div class="list-item-content">
                    <div class="list-item-title">${income.source} - ${formatCurrency(income.amount)}</div>
                    <div class="list-item-details">
                        ${formatDate(income.date)}
                        ${income.description ? ' | ' + income.description : ''}
                    </div>
                </div>
                <div class="list-item-actions">
                    <button class="btn btn-danger" onclick="deleteIncome(${income.id})">Delete</button>
                </div>
            </div>
        `).join('');
    } catch (error) {
        console.error('Error loading income:', error);
    }
}

async function deleteIncome(id) {
    if (!confirm('Are you sure you want to delete this income entry?')) return;

    try {
        await fetch(`${API_BASE}/income/${id}`, { method: 'DELETE' });
        loadIncome();
        loadDashboard();
    } catch (error) {
        console.error('Error deleting income:', error);
    }
}

// Expense Functions
async function loadExpenses() {
    try {
        const response = await fetch(`${API_BASE}/expenses`);
        const expenses = await response.json();

        const container = document.getElementById('expense-list');

        if (expenses.length === 0) {
            container.innerHTML = '<div class="empty-state"><p>No expenses recorded</p></div>';
            return;
        }

        container.innerHTML = expenses.map(expense => `
            <div class="list-item">
                <div class="list-item-content">
                    <div class="list-item-title">${expense.category} - ${formatCurrency(expense.amount)}</div>
                    <div class="list-item-details">
                        ${formatDate(expense.date)}
                        ${expense.description ? ' | ' + expense.description : ''}
                    </div>
                </div>
                <div class="list-item-actions">
                    <button class="btn btn-danger" onclick="deleteExpense(${expense.id})">Delete</button>
                </div>
            </div>
        `).join('');
    } catch (error) {
        console.error('Error loading expenses:', error);
    }
}

async function deleteExpense(id) {
    if (!confirm('Are you sure you want to delete this expense?')) return;

    try {
        await fetch(`${API_BASE}/expenses/${id}`, { method: 'DELETE' });
        loadExpenses();
        loadDashboard();
    } catch (error) {
        console.error('Error deleting expense:', error);
    }
}

// Budget Functions
async function loadBudgets() {
    try {
        const month = document.getElementById('budget-month').value;
        const year = document.getElementById('budget-year').value;

        const response = await fetch(`${API_BASE}/budgets?month=${month}&year=${year}`);
        const budgets = await response.json();

        const container = document.getElementById('budget-list');

        if (budgets.length === 0) {
            container.innerHTML = '<div class="empty-state"><p>No budgets set for this month</p></div>';
            return;
        }

        container.innerHTML = budgets.map(budget => `
            <div class="list-item">
                <div class="list-item-content">
                    <div class="list-item-title">${budget.category}</div>
                    <div class="list-item-details">${formatCurrency(budget.amount)}</div>
                </div>
                <div class="list-item-actions">
                    <button class="btn btn-danger" onclick="deleteBudget(${budget.id})">Delete</button>
                </div>
            </div>
        `).join('');
    } catch (error) {
        console.error('Error loading budgets:', error);
    }
}

async function deleteBudget(id) {
    if (!confirm('Are you sure you want to delete this budget?')) return;

    try {
        await fetch(`${API_BASE}/budgets/${id}`, { method: 'DELETE' });
        loadBudgets();
        loadDashboard();
    } catch (error) {
        console.error('Error deleting budget:', error);
    }
}

// Debt Functions
async function loadDebts() {
    try {
        const response = await fetch(`${API_BASE}/debts`);
        const debts = await response.json();

        const container = document.getElementById('debt-list');

        if (debts.length === 0) {
            container.innerHTML = '<div class="empty-state"><p>No debts recorded</p></div>';
            return;
        }

        container.innerHTML = debts.map(debt => {
            const progress = ((debt.principal - debt.current_balance) / debt.principal * 100).toFixed(2);
            return `
                <div class="list-item">
                    <div class="list-item-content">
                        <div class="list-item-title">${debt.name}</div>
                        <div class="list-item-details">
                            Principal: ${formatCurrency(debt.principal)} |
                            Balance: ${formatCurrency(debt.current_balance)} |
                            Rate: ${debt.interest_rate}%
                        </div>
                        <div class="list-item-details">
                            Min Payment: ${formatCurrency(debt.minimum_payment)}
                            ${debt.due_date ? ' | Due: Day ' + debt.due_date : ''}
                        </div>
                        <div class="progress-bar">
                            <div class="progress-fill" style="width: ${progress}%">
                                ${progress}% paid
                            </div>
                        </div>
                    </div>
                    <div class="list-item-actions">
                        <button class="btn btn-secondary" onclick="showPaymentModal(${debt.id})">Record Payment</button>
                        <button class="btn btn-danger" onclick="deleteDebt(${debt.id})">Delete</button>
                    </div>
                </div>
            `;
        }).join('');
    } catch (error) {
        console.error('Error loading debts:', error);
    }
}

async function deleteDebt(id) {
    if (!confirm('Are you sure you want to delete this debt?')) return;

    try {
        await fetch(`${API_BASE}/debts/${id}`, { method: 'DELETE' });
        loadDebts();
        loadDashboard();
    } catch (error) {
        console.error('Error deleting debt:', error);
    }
}

// Savings Goal Functions
async function loadSavingsGoals() {
    try {
        const response = await fetch(`${API_BASE}/savings-goals`);
        const goals = await response.json();

        const container = document.getElementById('savings-list');

        if (goals.length === 0) {
            container.innerHTML = '<div class="empty-state"><p>No savings goals created</p></div>';
            return;
        }

        container.innerHTML = goals.map(goal => `
            <div class="list-item">
                <div class="list-item-content">
                    <div class="list-item-title">${goal.name}</div>
                    <div class="list-item-details">
                        Target: ${formatCurrency(goal.target_amount)} |
                        Current: ${formatCurrency(goal.current_amount)}
                        ${goal.deadline ? ' | Deadline: ' + formatDate(goal.deadline) : ''}
                    </div>
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: ${goal.progress}%">
                            ${goal.progress}%
                        </div>
                    </div>
                </div>
                <div class="list-item-actions">
                    <button class="btn btn-secondary" onclick="showContributionModal(${goal.id})">Add Contribution</button>
                    <button class="btn btn-danger" onclick="deleteSavingsGoal(${goal.id})">Delete</button>
                </div>
            </div>
        `).join('');
    } catch (error) {
        console.error('Error loading savings goals:', error);
    }
}

async function deleteSavingsGoal(id) {
    if (!confirm('Are you sure you want to delete this savings goal?')) return;

    try {
        await fetch(`${API_BASE}/savings-goals/${id}`, { method: 'DELETE' });
        loadSavingsGoals();
        loadDashboard();
    } catch (error) {
        console.error('Error deleting savings goal:', error);
    }
}

// Modal Functions
function setupModalHandlers() {
    // Payment Modal
    const paymentModal = document.getElementById('payment-modal');
    const contributionModal = document.getElementById('contribution-modal');

    document.querySelectorAll('.close').forEach(closeBtn => {
        closeBtn.onclick = function() {
            paymentModal.classList.remove('active');
            contributionModal.classList.remove('active');
        };
    });

    window.onclick = function(event) {
        if (event.target === paymentModal) {
            paymentModal.classList.remove('active');
        }
        if (event.target === contributionModal) {
            contributionModal.classList.remove('active');
        }
    };
}

function showPaymentModal(debtId) {
    document.getElementById('payment-debt-id').value = debtId;
    document.getElementById('payment-date').value = getTodayDate();
    document.getElementById('payment-modal').classList.add('active');
}

function showContributionModal(goalId) {
    document.getElementById('contribution-goal-id').value = goalId;
    document.getElementById('contribution-date').value = getTodayDate();
    document.getElementById('contribution-modal').classList.add('active');
}

// Form Handlers
function setupFormHandlers() {
    // Income Form
    document.getElementById('income-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        const data = {
            amount: parseFloat(document.getElementById('income-amount').value),
            source: document.getElementById('income-source').value,
            date: document.getElementById('income-date').value,
            description: document.getElementById('income-description').value
        };

        try {
            await fetch(`${API_BASE}/income`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
            e.target.reset();
            document.getElementById('income-date').value = getTodayDate();
            loadIncome();
            loadDashboard();
        } catch (error) {
            console.error('Error adding income:', error);
        }
    });

    // Expense Form
    document.getElementById('expense-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        const data = {
            amount: parseFloat(document.getElementById('expense-amount').value),
            category: document.getElementById('expense-category').value,
            date: document.getElementById('expense-date').value,
            description: document.getElementById('expense-description').value
        };

        try {
            await fetch(`${API_BASE}/expenses`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
            e.target.reset();
            document.getElementById('expense-date').value = getTodayDate();
            loadExpenses();
            loadDashboard();
        } catch (error) {
            console.error('Error adding expense:', error);
        }
    });

    // Budget Form
    document.getElementById('budget-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        const data = {
            category: document.getElementById('budget-category').value,
            amount: parseFloat(document.getElementById('budget-amount').value),
            month: parseInt(document.getElementById('budget-month').value),
            year: parseInt(document.getElementById('budget-year').value)
        };

        try {
            await fetch(`${API_BASE}/budgets`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
            e.target.reset();
            const now = new Date();
            document.getElementById('budget-month').value = now.getMonth() + 1;
            document.getElementById('budget-year').value = now.getFullYear();
            loadBudgets();
            loadDashboard();
        } catch (error) {
            console.error('Error adding budget:', error);
        }
    });

    // Debt Form
    document.getElementById('debt-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        const principal = parseFloat(document.getElementById('debt-principal').value);
        const data = {
            name: document.getElementById('debt-name').value,
            principal: principal,
            current_balance: parseFloat(document.getElementById('debt-balance').value),
            interest_rate: parseFloat(document.getElementById('debt-interest').value),
            minimum_payment: parseFloat(document.getElementById('debt-payment').value),
            due_date: document.getElementById('debt-due').value || null
        };

        try {
            await fetch(`${API_BASE}/debts`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
            e.target.reset();
            loadDebts();
            loadDashboard();
        } catch (error) {
            console.error('Error adding debt:', error);
        }
    });

    // Payment Form
    document.getElementById('payment-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        const debtId = document.getElementById('payment-debt-id').value;
        const data = {
            amount: parseFloat(document.getElementById('payment-amount').value),
            date: document.getElementById('payment-date').value,
            description: document.getElementById('payment-description').value
        };

        try {
            await fetch(`${API_BASE}/debts/${debtId}/payments`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
            e.target.reset();
            document.getElementById('payment-modal').classList.remove('active');
            loadDebts();
            loadDashboard();
        } catch (error) {
            console.error('Error recording payment:', error);
        }
    });

    // Savings Goal Form
    document.getElementById('savings-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        const data = {
            name: document.getElementById('savings-name').value,
            target_amount: parseFloat(document.getElementById('savings-target').value),
            current_amount: parseFloat(document.getElementById('savings-current').value),
            deadline: document.getElementById('savings-deadline').value || null
        };

        try {
            await fetch(`${API_BASE}/savings-goals`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
            e.target.reset();
            document.getElementById('savings-current').value = 0;
            loadSavingsGoals();
            loadDashboard();
        } catch (error) {
            console.error('Error creating savings goal:', error);
        }
    });

    // Contribution Form
    document.getElementById('contribution-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        const goalId = document.getElementById('contribution-goal-id').value;
        const data = {
            amount: parseFloat(document.getElementById('contribution-amount').value),
            date: document.getElementById('contribution-date').value,
            description: document.getElementById('contribution-description').value
        };

        try {
            await fetch(`${API_BASE}/savings-goals/${goalId}/contributions`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
            e.target.reset();
            document.getElementById('contribution-modal').classList.remove('active');
            loadSavingsGoals();
            loadDashboard();
        } catch (error) {
            console.error('Error adding contribution:', error);
        }
    });
}
