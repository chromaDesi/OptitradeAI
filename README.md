# 📊 Smart Portfolio Trader

An intelligent, full-stack algorithmic trading platform that combines financial data, social sentiment, and portfolio optimization to generate actionable trading signals. Built with React, Python, and MongoDB, this project is designed to support multiple users, predictive modeling, and long-term portfolio performance tracking.

---

## 🚀 Features

- 📈 Fetches real-time market data via **Alpha Vantage API**
- 📣 Integrates social and news sentiment via **Tradestie (Reddit)** and **Finnhub**
- 🧠 Predicts expected returns using **regression models (Logistic/XGBoost)**
- ⚖️ Optimizes portfolio weights using the **Portfolio Optimizer API**
- 📉 Simulates and backtests strategies with performance metrics
- 📊 Visualizes returns, allocations, and sentiment via **Streamlit** or **Plotly**
- 🔐 Built to scale for **multiple users** with isolated data and models

---

## 🧩 Tech Stack

| Frontend      | Backend     | Data / ML        | Storage        |
|---------------|-------------|------------------|----------------|
| React (Vite)  | Python (FastAPI or Flask) | scikit-learn, XGBoost | MongoDB Atlas |
| Tailwind CSS  | REST API    | Pandas, NumPy    | dotenv (.env)  |
| Streamlit (viz) |             | Matplotlib, Plotly |              |

---

| Step  | Task                                                                                      | API or DIY                                          |
| ----- | ----------------------------------------------------------------------------------------- | --------------------------------------------------- |
| 1️⃣   | **Fetch price data** (daily OHLCV, indicators)                                            | ✅ **Alpha Vantage API**                             |
| 2️⃣   | **Store raw price data** in MongoDB                                                       | 🧠 You write this script                            |
| 3️⃣   | **Fetch sentiment data** (Reddit + News)                                                  | ✅ **Tradestie API** + ✅ **Finnhub API**             |
| 4️⃣   | **Store sentiment data** in MongoDB                                                       | 🧠 You write schema + script                        |
| 5️⃣   | **Engineer features** (returns, volatility, score weights, etc.)                          | 🧠 You write this logic                             |
| 5️⃣.5️⃣ | **Train regression model** (e.g., Linear, Ridge, XGBoost) to **predict expected returns** | 🧠 You write this using `scikit-learn` or `xgboost` |
| 6️⃣   | **Send predicted returns + cov matrix to Portfolio Optimizer**                            | ✅ **Portfolio Optimizer API**                       |
| 7️⃣   | **Generate portfolio allocation and signals** based on output                             | 🧠 You write this rule logic                        |
| 8️⃣   | **Simulate/backtest** over past data                                                      | ✅ Use **Backtrader**, or build minimal custom logic |
| 9️⃣   | **Store strategy performance** (returns, drawdown, Sharpe, trades)                        | 🧠 Store in MongoDB (`backtests` collection)        |
| 🔟    | **Visualize results** (charts, dashboards)                                                | ✅ Use **Streamlit** or **Plotly/Matplotlib**        |

