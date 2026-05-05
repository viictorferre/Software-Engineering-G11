const categories = ["Food", "Transport", "Leisure", "Housing", "Studies", "Health", "Income", "Other"];

const defaultBudgets = [
  { category: "Food", limit: 260 },
  { category: "Transport", limit: 90 },
  { category: "Leisure", limit: 150 },
  { category: "Studies", limit: 120 },
];

function createId() {
  return crypto?.randomUUID ? crypto.randomUUID() : `${Date.now()}-${Math.random().toString(16).slice(2)}`;
}

function monthDate(day) {
  const now = new Date();
  return `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, "0")}-${String(day).padStart(2, "0")}`;
}

function createDemoTransactions() {
  return [
    { id: createId(), type: "income", amount: 850, description: "Part-time job", category: "Income", date: monthDate(1) },
    { id: createId(), type: "expense", amount: 42.7, description: "Weekly groceries", category: "Food", date: monthDate(3) },
    { id: createId(), type: "expense", amount: 18.5, description: "Metro and bus", category: "Transport", date: monthDate(4) },
    { id: createId(), type: "expense", amount: 32, description: "Dinner with friends", category: "Leisure", date: monthDate(4) },
    { id: createId(), type: "expense", amount: 64.9, description: "University material", category: "Studies", date: monthDate(5) },
  ];
}

const state = {
  transactions: loadTransactions(),
  budgets: loadBudgets(),
  activeView: "dashboard",
};

const elements = {
  tabs: document.querySelectorAll(".nav-tab"),
  views: document.querySelectorAll(".view"),
  currentMonth: document.querySelector("#currentMonth"),
  incomeTotal: document.querySelector("#incomeTotal"),
  expenseTotal: document.querySelector("#expenseTotal"),
  balanceTotal: document.querySelector("#balanceTotal"),
  savingRate: document.querySelector("#savingRate"),
  categoryBars: document.querySelector("#categoryBars"),
  latestTransactions: document.querySelector("#latestTransactions"),
  transactionList: document.querySelector("#transactionList"),
  transactionForm: document.querySelector("#transactionForm"),
  transactionType: document.querySelector("#transactionType"),
  transactionAmount: document.querySelector("#transactionAmount"),
  transactionDescription: document.querySelector("#transactionDescription"),
  transactionCategory: document.querySelector("#transactionCategory"),
  transactionDate: document.querySelector("#transactionDate"),
  categoryFilter: document.querySelector("#categoryFilter"),
  budgetForm: document.querySelector("#budgetForm"),
  budgetCategory: document.querySelector("#budgetCategory"),
  budgetLimit: document.querySelector("#budgetLimit"),
  budgetGrid: document.querySelector("#budgetGrid"),
  recommendationList: document.querySelector("#recommendationList"),
  resetDemo: document.querySelector("#resetDemo"),
};

function loadTransactions() {
  const saved = localStorage.getItem("estalvia-transactions");
  if (!saved) {
    return createDemoTransactions();
  }

  try {
    const parsed = JSON.parse(saved);
    return Array.isArray(parsed) ? parsed : createDemoTransactions();
  } catch {
    return createDemoTransactions();
  }
}

function saveTransactions() {
  localStorage.setItem("estalvia-transactions", JSON.stringify(state.transactions));
}

function loadBudgets() {
  const saved = localStorage.getItem("estalvia-budgets");
  if (!saved) {
    return defaultBudgets.map((budget) => ({ ...budget }));
  }

  try {
    const parsed = JSON.parse(saved);
    return Array.isArray(parsed) && parsed.length ? parsed : defaultBudgets.map((budget) => ({ ...budget }));
  } catch {
    return defaultBudgets.map((budget) => ({ ...budget }));
  }
}

function saveBudgets() {
  localStorage.setItem("estalvia-budgets", JSON.stringify(state.budgets));
}

function formatMoney(value) {
  return `EUR ${new Intl.NumberFormat("en-GB", {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  }).format(value)}`;
}

function formatDate(date) {
  return new Intl.DateTimeFormat("en-GB", {
    day: "2-digit",
    month: "short",
    year: "numeric",
  }).format(new Date(`${date}T00:00:00`));
}

function getMonthTransactions() {
  const now = new Date();
  const year = now.getFullYear();
  const month = now.getMonth();

  return state.transactions.filter((transaction) => {
    const date = new Date(`${transaction.date}T00:00:00`);
    return date.getFullYear() === year && date.getMonth() === month;
  });
}

function getTotals(transactions = getMonthTransactions()) {
  return transactions.reduce(
    (totals, transaction) => {
      if (transaction.type === "income") {
        totals.income += transaction.amount;
      } else {
        totals.expense += transaction.amount;
      }
      totals.balance = totals.income - totals.expense;
      return totals;
    },
    { income: 0, expense: 0, balance: 0 },
  );
}

function getExpenseByCategory(transactions = getMonthTransactions()) {
  return transactions
    .filter((transaction) => transaction.type === "expense")
    .reduce((summary, transaction) => {
      summary[transaction.category] = (summary[transaction.category] || 0) + transaction.amount;
      return summary;
    }, {});
}

function suggestCategory(description, type) {
  if (type === "income") {
    return "Income";
  }

  const text = description.toLowerCase();
  const rules = [
    { category: "Food", words: ["supermarket", "groceries", "food", "coffee", "restaurant", "shopping"] },
    { category: "Transport", words: ["metro", "bus", "train", "fuel", "taxi", "uber"] },
    { category: "Leisure", words: ["cinema", "dinner", "bar", "concert", "game"] },
    { category: "Housing", words: ["rent", "electricity", "water", "internet"] },
    { category: "Studies", words: ["university", "book", "material", "course"] },
    { category: "Health", words: ["pharmacy", "doctor", "gym"] },
  ];

  const match = rules.find((rule) => rule.words.some((word) => text.includes(word)));
  return match ? match.category : "Other";
}

function renderCategoryOptions() {
  elements.transactionCategory.innerHTML = categories
    .map((category) => `<option value="${category}">${category}</option>`)
    .join("");

  elements.categoryFilter.innerHTML = [
    '<option value="all">All</option>',
    ...categories.map((category) => `<option value="${category}">${category}</option>`),
  ].join("");

  elements.budgetCategory.innerHTML = categories
    .filter((category) => category !== "Income")
    .map((category) => `<option value="${category}">${category}</option>`)
    .join("");
}

function renderTotals() {
  const totals = getTotals();
  const savingRate = totals.income > 0 ? Math.max(0, Math.round((totals.balance / totals.income) * 100)) : 0;

  elements.incomeTotal.textContent = formatMoney(totals.income);
  elements.expenseTotal.textContent = formatMoney(totals.expense);
  elements.balanceTotal.textContent = formatMoney(totals.balance);
  elements.savingRate.textContent = `${savingRate}%`;
}

function renderCategoryBars() {
  const summary = getExpenseByCategory();
  const entries = Object.entries(summary).sort((a, b) => b[1] - a[1]);
  const max = Math.max(...entries.map((entry) => entry[1]), 1);

  if (!entries.length) {
    elements.categoryBars.innerHTML = '<div class="empty-state">There are no expenses this month yet.</div>';
    return;
  }

  elements.categoryBars.innerHTML = entries
    .map(([category, amount]) => {
      const width = Math.round((amount / max) * 100);
      return `
        <div class="bar-row">
          <span>${category}</span>
          <div class="bar-track" aria-hidden="true">
            <div class="bar-fill" style="width: ${width}%"></div>
          </div>
          <strong>${formatMoney(amount)}</strong>
        </div>
      `;
    })
    .join("");
}

function transactionRow(transaction) {
  const sign = transaction.type === "income" ? "+" : "-";
  return `
        <article class="transaction-row">
          <div class="transaction-title">
            <strong>${transaction.description}</strong>
        <span>${transaction.category} - ${formatDate(transaction.date)}</span>
          </div>
          <div class="amount ${transaction.type}">${sign}${formatMoney(transaction.amount)}</div>
        </article>
  `;
}

function renderTransactions() {
  const sorted = [...state.transactions].sort((a, b) => new Date(b.date) - new Date(a.date));
  const filtered =
    elements.categoryFilter.value === "all"
      ? sorted
      : sorted.filter((transaction) => transaction.category === elements.categoryFilter.value);

  elements.latestTransactions.innerHTML = sorted.length
    ? sorted.map(transactionRow).join("")
    : '<div class="empty-state">Add a transaction to get started.</div>';

  elements.transactionList.innerHTML = filtered.length
    ? filtered.map(transactionRow).join("")
    : '<div class="empty-state">There are no transactions for this filter.</div>';
}

function renderBudgets() {
  const summary = getExpenseByCategory();

  elements.budgetGrid.innerHTML = state.budgets
    .sort((a, b) => a.category.localeCompare(b.category))
    .map((budget) => {
      const spent = summary[budget.category] || 0;
      const percentage = Math.min(Math.round((spent / budget.limit) * 100), 100);
      const remaining = budget.limit - spent;
      const status = percentage >= 100 ? "danger" : percentage >= 80 ? "warning" : "";
      const label = percentage >= 100 ? "Exceeded" : percentage >= 80 ? "Warning" : "On track";

      return `
        <article class="panel budget-card">
          <div class="budget-meta">
            <h3>${budget.category}</h3>
            <span class="status-pill ${status}">${label}</span>
          </div>
          <div class="progress-track" aria-hidden="true">
            <div class="progress-fill ${status}" style="width: ${percentage}%"></div>
          </div>
          <div class="budget-numbers">
            <span>Spent: ${formatMoney(spent)}</span>
            <span>Limit: ${formatMoney(budget.limit)}</span>
            <span>Remaining: ${formatMoney(remaining)}</span>
          </div>
        </article>
      `;
    })
    .join("");
}

function renderRecommendations() {
  const totals = getTotals();
  const summary = getExpenseByCategory();
  const highestCategory = Object.entries(summary).sort((a, b) => b[1] - a[1])[0];
  const recommendations = [];

  if (totals.income === 0) {
    recommendations.push({
      title: "Register your income",
      body: "Adding income allows the app to calculate your savings rate and detect whether the month is balanced.",
    });
  }

  if (highestCategory) {
    recommendations.push({
      title: `Review ${highestCategory[0]}`,
      body: `It is your highest spending category this month: ${formatMoney(highestCategory[1])}. Reducing it by 10% would free up ${formatMoney(highestCategory[1] * 0.1)}.`,
    });
  }

  if (totals.balance > 0) {
    recommendations.push({
      title: "Automate a small goal",
      body: `You could set aside ${formatMoney(totals.balance * 0.25)} this month without committing your full available balance.`,
    });
  } else if (totals.expense > totals.income) {
    recommendations.push({
      title: "Prioritize variable expenses",
      body: "Your balance is negative. Start by reviewing leisure, transport and small purchases before changing essential expenses.",
    });
  }

  recommendations.push({
    title: "Keep a weekly habit",
    body: "A short weekly review prevents the budget from getting out of control at the end of the month.",
  });

  elements.recommendationList.innerHTML = recommendations
    .map(
      (recommendation) => `
        <article class="panel recommendation">
          <h3>${recommendation.title}</h3>
          <p>${recommendation.body}</p>
        </article>
      `,
    )
    .join("");
}

function renderMonth() {
  elements.currentMonth.textContent = new Intl.DateTimeFormat("en-GB", {
    month: "long",
    year: "numeric",
  }).format(new Date());
}

function renderAll() {
  renderMonth();
  renderTotals();
  renderCategoryBars();
  renderTransactions();
  renderBudgets();
  renderRecommendations();
}

function changeView(viewId) {
  state.activeView = viewId;
  elements.tabs.forEach((tab) => tab.classList.toggle("active", tab.dataset.view === viewId));
  elements.views.forEach((view) => view.classList.toggle("active", view.id === viewId));
}

function setDefaultDate() {
  elements.transactionDate.value = new Date().toISOString().slice(0, 10);
}

elements.tabs.forEach((tab) => {
  tab.addEventListener("click", () => changeView(tab.dataset.view));
});

elements.transactionDescription.addEventListener("input", () => {
  elements.transactionCategory.value = suggestCategory(elements.transactionDescription.value, elements.transactionType.value);
});

elements.transactionType.addEventListener("change", () => {
  elements.transactionCategory.value = suggestCategory(elements.transactionDescription.value, elements.transactionType.value);
});

elements.categoryFilter.addEventListener("change", renderTransactions);

elements.budgetForm.addEventListener("submit", (event) => {
  event.preventDefault();

  const category = elements.budgetCategory.value;
  const limit = Number(elements.budgetLimit.value);
  const existingBudget = state.budgets.find((budget) => budget.category === category);

  if (existingBudget) {
    existingBudget.limit = limit;
  } else {
    state.budgets.push({ category, limit });
  }

  saveBudgets();
  elements.budgetForm.reset();
  renderBudgets();
  renderRecommendations();
});

elements.transactionForm.addEventListener("submit", (event) => {
  event.preventDefault();

  const transaction = {
    id: createId(),
    type: elements.transactionType.value,
    amount: Number(elements.transactionAmount.value),
    description: elements.transactionDescription.value.trim(),
    category: elements.transactionCategory.value,
    date: elements.transactionDate.value,
  };

  state.transactions.push(transaction);
  saveTransactions();
  elements.transactionForm.reset();
  setDefaultDate();
  renderAll();
  changeView("dashboard");
});

elements.resetDemo.addEventListener("click", () => {
  state.transactions = createDemoTransactions();
  state.budgets = defaultBudgets.map((budget) => ({ ...budget }));
  saveTransactions();
  saveBudgets();
  renderAll();
});

renderCategoryOptions();
setDefaultDate();
renderAll();
