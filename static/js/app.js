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

function getAccountTypeLabel(type) {
    const labels = {
        'checking': 'Checking',
        'savings': 'Savings',
        'credit_card': 'Credit Card',
        'ira': 'IRA',
        '401k': '401(k)',
        'investment': 'Investment',
        'hsa': 'HSA',
        'money_market': 'Money Market',
        'cd': 'CD',
        'other': 'Other'
    };
    return labels[type] || type;
}

function getDebtTypeLabel(type) {
    const labels = {
        'credit_card': 'Credit Card',
        'student_loan': 'Student Loan',
        'mortgage': 'Mortgage',
        'auto_loan': 'Auto Loan',
        'personal_loan': 'Personal Loan',
        'medical': 'Medical',
        'other': 'Other'
    };
    return labels[type] || type;
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
    } else if (tabName === 'accounts') {
        loadAccounts();
    } else if (tabName === 'income') {
        loadIncome();
    } else if (tabName === 'expenses') {
        loadExpenses();
    } else if (tabName === 'budgets') {
        loadBudgets();
    } else if (tabName === 'debts') {
        loadDebts();
    } else if (tabName === 'debt-payoff') {
        // Nothing to preload
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

    // Load categories and account types
    loadCategories();
    loadAccountTypes();
    loadDebtTypes();

    // Load initial dashboard
    loadDashboard();

    // Setup form handlers
    setupFormHandlers();

    // Setup modal handlers
    setupModalHandlers();
});

// Load Account Types
async function loadAccountTypes() {
    try {
        const response = await fetch(`${API_BASE}/account-types`);
        const types = await response.json();
        const accountType = document.getElementById('account-type');
        types.forEach(type => {
            accountType.add(new Option(type.label, type.value));
        });
    } catch (error) {
        console.error('Error loading account types:', error);
    }
}

// Load Debt Types
async function loadDebtTypes() {
    try {
        const response = await fetch(`${API_BASE}/debt-types`);
        const types = await response.json();
        const debtType = document.getElementById('debt-type');
        types.forEach(type => {
            debtType.add(new Option(type.label, type.value));
        });
    } catch (error) {
        console.error('Error loading debt types:', error);
    }
}

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

        // Update Net Worth
        const netWorthEl = document.getElementById('net-worth');
        netWorthEl.textContent = formatCurrency(data.net_worth);
        netWorthEl.className = 'net-worth-amount ' + (data.net_worth >= 0 ? 'positive' : 'negative');

        // Calculate total assets and liabilities
        const totalAssets = (data.total_cash || 0) + (data.total_retirement || 0) + (data.total_investments || 0);
        const totalLiabilities = (data.total_debt || 0) + (data.total_credit_balance || 0);

        document.getElementById('total-assets').textContent = formatCurrency(totalAssets);
        document.getElementById('total-liabilities').textContent = formatCurrency(totalLiabilities);

        // Update summary cards
        document.getElementById('monthly-income').textContent = formatCurrency(data.monthly_income);
        document.getElementById('monthly-expenses').textContent = formatCurrency(data.monthly_expenses);

        const netMonthly = document.getElementById('net-monthly');
        netMonthly.textContent = formatCurrency(data.net_monthly);
        netMonthly.className = 'amount ' + (data.net_monthly >= 0 ? 'positive' : 'negative');

        document.getElementById('total-cash').textContent = formatCurrency(data.total_cash || 0);
        document.getElementById('total-retirement').textContent = formatCurrency(data.total_retirement || 0);
        document.getElementById('total-debt').textContent = formatCurrency(data.total_debt);

        // Update charts
        updateExpensesChart(data.expenses_by_category);
        updateBudgetChart(data.budget_comparison);
        updateAccountsChart(data.accounts);
        updateNetworthChart(data);

        // Update debts summary
        updateDebtsSummary(data.debts);

        // Update savings summary
        updateSavingsSummary(data.savings_goals);
    } catch (error) {
        console.error('Error loading dashboard:', error);
    }
}

let expensesChart, budgetChart, accountsChart, networthChart;

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
                    '#43e97b', '#fa709a', '#fee140', '#30cfd0',
                    '#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4'
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

function updateAccountsChart(accounts) {
    const ctx = document.getElementById('accounts-chart').getContext('2d');

    if (accountsChart) {
        accountsChart.destroy();
    }

    if (!accounts || accounts.length === 0) {
        return;
    }

    // Group accounts by type
    const typeGroups = {};
    accounts.forEach(acc => {
        const type = getAccountTypeLabel(acc.account_type);
        if (!typeGroups[type]) {
            typeGroups[type] = 0;
        }
        typeGroups[type] += acc.balance;
    });

    const labels = Object.keys(typeGroups);
    const data = Object.values(typeGroups);

    accountsChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Balance',
                data: data,
                backgroundColor: [
                    '#28a745', '#20c997', '#17a2b8', '#6f42c1',
                    '#fd7e14', '#dc3545', '#6610f2', '#e83e8c'
                ]
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: function(value) {
                            return formatCurrency(value);
                        }
                    }
                }
            }
        }
    });
}

function updateNetworthChart(data) {
    const ctx = document.getElementById('networth-chart').getContext('2d');

    if (networthChart) {
        networthChart.destroy();
    }

    const totalAssets = (data.total_cash || 0) + (data.total_retirement || 0) + (data.total_investments || 0);
    const totalLiabilities = (data.total_debt || 0) + (data.total_credit_balance || 0);

    if (totalAssets === 0 && totalLiabilities === 0) {
        return;
    }

    networthChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Cash & Bank', 'Retirement', 'Investments', 'Debts', 'Credit Cards'],
            datasets: [{
                data: [
                    data.total_cash || 0,
                    data.total_retirement || 0,
                    data.total_investments || 0,
                    data.total_debt || 0,
                    data.total_credit_balance || 0
                ],
                backgroundColor: [
                    '#28a745',
                    '#6f42c1',
                    '#17a2b8',
                    '#dc3545',
                    '#fd7e14'
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

function updateDebtsSummary(debts) {
    const container = document.getElementById('debts-summary');

    if (debts.length === 0) {
        container.innerHTML = '<div class="empty-state"><p>No active debts - Great job!</p></div>';
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
                    <div class="progress-fill" style="width: ${Math.max(0, Math.min(100, (debt.principal - debt.current_balance) / debt.principal * 100))}%">
                        ${Math.round((debt.principal - debt.current_balance) / debt.principal * 100)}% paid
                    </div>
                </div>
            </div>
        </div>
    `).join('');
}

function updateSavingsSummary(goals) {
    const container = document.getElementById('savings-summary');

    if (goals.length === 0) {
        container.innerHTML = '<div class="empty-state"><p>No savings goals - Create one to start saving!</p></div>';
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

// Account Functions
async function loadAccounts() {
    try {
        const response = await fetch(`${API_BASE}/accounts`);
        const accounts = await response.json();

        // Group accounts by type
        const bankAccounts = accounts.filter(a => ['checking', 'savings', 'money_market'].includes(a.account_type));
        const creditCards = accounts.filter(a => a.account_type === 'credit_card');
        const retirementAccounts = accounts.filter(a => ['ira', '401k'].includes(a.account_type));
        const investmentAccounts = accounts.filter(a => a.account_type === 'investment');
        const otherAccounts = accounts.filter(a => ['hsa', 'cd', 'other'].includes(a.account_type));

        renderAccountList('bank-accounts-list', bankAccounts, 'No bank accounts added');
        renderAccountList('credit-cards-list', creditCards, 'No credit cards added');
        renderAccountList('retirement-accounts-list', retirementAccounts, 'No retirement accounts added');
        renderAccountList('investment-accounts-list', investmentAccounts, 'No investment accounts added');
        renderAccountList('other-accounts-list', otherAccounts, 'No other accounts added');
    } catch (error) {
        console.error('Error loading accounts:', error);
    }
}

function renderAccountList(containerId, accounts, emptyMessage) {
    const container = document.getElementById(containerId);

    if (accounts.length === 0) {
        container.innerHTML = `<div class="empty-state"><p>${emptyMessage}</p></div>`;
        return;
    }

    container.innerHTML = accounts.map(account => {
        const isCreditCard = account.account_type === 'credit_card';
        let utilizationHtml = '';

        if (isCreditCard && account.credit_limit) {
            const utilization = (account.balance / account.credit_limit * 100).toFixed(1);
            const utilizationClass = utilization > 30 ? (utilization > 50 ? 'danger' : 'warning') : 'safe';
            utilizationHtml = `
                <div class="credit-utilization">
                    <span>Utilization: ${utilization}%</span>
                    <div class="utilization-bar">
                        <div class="utilization-fill ${utilizationClass}" style="width: ${Math.min(100, utilization)}%"></div>
                    </div>
                </div>
            `;
        }

        return `
            <div class="account-item list-item">
                <div class="list-item-content">
                    <div class="list-item-title">
                        ${account.name}
                        ${account.account_number_last4 ? `<span class="account-last4">****${account.account_number_last4}</span>` : ''}
                    </div>
                    <div class="list-item-details">
                        ${account.institution ? account.institution + ' | ' : ''}
                        ${getAccountTypeLabel(account.account_type)}
                        ${account.interest_rate ? ' | ' + account.interest_rate + '% APY' : ''}
                        ${isCreditCard && account.credit_limit ? ' | Limit: ' + formatCurrency(account.credit_limit) : ''}
                    </div>
                    ${utilizationHtml}
                    <div class="account-balance ${isCreditCard ? 'negative' : 'positive'}">
                        ${formatCurrency(account.balance)}
                    </div>
                </div>
                <div class="list-item-actions">
                    <button class="btn btn-secondary" onclick="showUpdateBalanceModal(${account.id}, ${account.balance})">Update</button>
                    <button class="btn btn-danger" onclick="deleteAccount(${account.id})">Delete</button>
                </div>
            </div>
        `;
    }).join('');
}

async function deleteAccount(id) {
    if (!confirm('Are you sure you want to delete this account?')) return;

    try {
        await fetch(`${API_BASE}/accounts/${id}`, { method: 'DELETE' });
        loadAccounts();
        loadDashboard();
    } catch (error) {
        console.error('Error deleting account:', error);
    }
}

function showUpdateBalanceModal(accountId, currentBalance) {
    document.getElementById('update-account-id').value = accountId;
    document.getElementById('update-balance-amount').value = currentBalance;
    document.getElementById('update-balance-modal').classList.add('active');
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
            container.innerHTML = '<div class="empty-state"><p>No debts recorded - Congratulations!</p></div>';
            return;
        }

        container.innerHTML = debts.map(debt => {
            const progress = ((debt.principal - debt.current_balance) / debt.principal * 100).toFixed(2);
            return `
                <div class="list-item">
                    <div class="list-item-content">
                        <div class="list-item-title">${debt.name} <span class="debt-type-badge">${getDebtTypeLabel(debt.debt_type)}</span></div>
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

// Debt Payoff Calculator Functions
async function calculateDebtPayoff() {
    const strategy = document.getElementById('payoff-strategy').value;
    const extraPayment = parseFloat(document.getElementById('extra-payment').value) || 0;

    try {
        const response = await fetch(`${API_BASE}/debt-payoff/calculate`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ strategy, extra_payment: extraPayment })
        });

        const data = await response.json();

        if (data.error) {
            alert(data.error);
            return;
        }

        // Show results section
        document.getElementById('payoff-results').style.display = 'block';

        // Update summary
        document.getElementById('payoff-date').textContent = data.summary.payoff_date;
        document.getElementById('payoff-months').textContent = data.summary.payoff_months + ' months';
        document.getElementById('payoff-interest').textContent = formatCurrency(data.summary.total_interest);
        document.getElementById('interest-saved').textContent = formatCurrency(data.summary.interest_saved);
        document.getElementById('months-saved').textContent = data.summary.months_saved + ' months';

        // Update comparison
        document.getElementById('min-only-date').textContent = data.minimum_only.payoff_date;
        document.getElementById('min-only-interest').textContent = 'Interest: ' + formatCurrency(data.minimum_only.total_interest);
        document.getElementById('your-plan-date').textContent = data.summary.payoff_date;
        document.getElementById('your-plan-interest').textContent = 'Interest: ' + formatCurrency(data.summary.total_interest);

        // Update payoff order
        const orderContainer = document.getElementById('payoff-order');
        orderContainer.innerHTML = data.schedule.map((item, index) => `
            <div class="payoff-item">
                <div class="payoff-order-number">${index + 1}</div>
                <div class="payoff-item-content">
                    <div class="payoff-item-name">${item.debt_name}</div>
                    <div class="payoff-item-details">
                        Starting Balance: ${formatCurrency(item.starting_balance)} |
                        Total Interest: ${formatCurrency(item.total_interest)} |
                        Paid off in ${item.payoff_month} months
                    </div>
                </div>
            </div>
        `).join('');

    } catch (error) {
        console.error('Error calculating payoff:', error);
        alert('Error calculating payoff plan. Make sure you have debts added.');
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
    const updateBalanceModal = document.getElementById('update-balance-modal');

    document.querySelectorAll('.close').forEach(closeBtn => {
        closeBtn.onclick = function() {
            paymentModal.classList.remove('active');
            contributionModal.classList.remove('active');
            updateBalanceModal.classList.remove('active');
        };
    });

    window.onclick = function(event) {
        if (event.target === paymentModal) {
            paymentModal.classList.remove('active');
        }
        if (event.target === contributionModal) {
            contributionModal.classList.remove('active');
        }
        if (event.target === updateBalanceModal) {
            updateBalanceModal.classList.remove('active');
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
    // Account Form
    document.getElementById('account-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        const data = {
            name: document.getElementById('account-name').value,
            account_type: document.getElementById('account-type').value,
            institution: document.getElementById('account-institution').value,
            balance: parseFloat(document.getElementById('account-balance').value),
            interest_rate: document.getElementById('account-interest').value ? parseFloat(document.getElementById('account-interest').value) : null,
            credit_limit: document.getElementById('account-credit-limit').value ? parseFloat(document.getElementById('account-credit-limit').value) : null,
            account_number_last4: document.getElementById('account-last4').value,
            notes: document.getElementById('account-notes').value
        };

        try {
            await fetch(`${API_BASE}/accounts`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
            e.target.reset();
            loadAccounts();
            loadDashboard();
        } catch (error) {
            console.error('Error adding account:', error);
        }
    });

    // Update Balance Form
    document.getElementById('update-balance-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        const accountId = document.getElementById('update-account-id').value;
        const newBalance = parseFloat(document.getElementById('update-balance-amount').value);

        try {
            await fetch(`${API_BASE}/accounts/${accountId}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ balance: newBalance })
            });
            document.getElementById('update-balance-modal').classList.remove('active');
            loadAccounts();
            loadDashboard();
        } catch (error) {
            console.error('Error updating balance:', error);
        }
    });

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
            debt_type: document.getElementById('debt-type').value,
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

    // Debt Payoff Form
    document.getElementById('payoff-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        await calculateDebtPayoff();
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
