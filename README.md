# 📊 Smart Portfolio Trader

An intelligent, full-stack algorithmic trading platform that combines financial data, social sentiment, and portfolio optimization to generate actionable trading signals. Built with React, Python, and MongoDB, this project is designed to support multiple users, predictive modeling, and long-term portfolio performance tracking. Currently built for a solo invester, with hopes to scale into a multi-user software.

---

## 🚀 Features

- 📈 Fetches real-time market data via **Finnhub**
- 📣 Integrates social and news sentiment **Finnhub**
- 🧠 Predicts expected returns using **regression models (Logistic Regression)**
- ⚖️ Optimizes portfolio weights using the **Portfolio Optimizer API**
- 📉 Simulates and backtests strategies with performance metrics
- 📊 Visualizes returns, allocations, and sentiment via **Streamlit** or **Plotly**
- 🔐 Built to scale for **multiple users** with isolated data and models

---

## 🧩 Tech Stack

| Frontend      | Backend     | Data / ML        | Storage        |
|---------------|-------------|------------------|----------------|
| React (Vite)  | Python (FastAPI or Flask) | scikit-learn | MongoDB Atlas |
| Tailwind CSS  | REST API    | Pandas, NumPy    | dotenv (.env)  |
| Streamlit (viz) |             | Matplotlib, Plotly |              |

---

| Step   | Task                                                          | API or DIY                                              |
| ------ | ------------------------------------------------------------- | ------------------------------------------------------- |
| 1️⃣    | **Fetch price data** (daily OHLCV, intraday optional)         | ✅ **Finnhub API**                                       |
| 2️⃣    | **Fetch sentiment data** (news + Reddit/Stocktwits)           | ✅ **Finnhub API**                                       |
| 3️⃣    | **Store raw data** in MongoDB (prices, sentiment)             | 🧠 You write this script                                |
| 4️⃣    | **Engineer features** (returns, volatility, sentiment trends) | 🧠 You write this logic                                 |
| 5️⃣    | **Train regression model** to predict expected returns        | 🧠 You build this (start with `LinearRegression`)       |
| 6️⃣    | **Predict expected returns** for current market state         | 🧠 Model inference on latest feature batch              |
| 7️⃣    | **Send returns + covariance to Portfolio Optimizer**          | ✅ **Portfolio Optimizer API**                           |
| 8️⃣    | **Receive optimized weights** (asset allocation)              | ✅ JSON output (weights for each asset)                  |
| 9️⃣    | **Compare to current portfolio & generate signals**           | 🧠 You write logic for buy/sell/hold + deltas           |
| 🔟     | **Simulate/backtest portfolio performance**                   | 🧠 Use `Backtrader` or custom logic                     |
| 1️⃣1️⃣ | **Store user-specific signals, weights, and performance**     | 🧠 MongoDB (multi-user-aware schema)                    |
| 1️⃣2️⃣ | **Visualize results** (performance, allocation, sentiment)    | ✅ Use **Streamlit**, **Plotly**, or **React dashboard** |

---

## How can this project grow (Future planes)?

- User authentication and authorization for multi user access
- Integration with other data sources (e.g., Twitter, news APIs)
- Upgrading to a heavier model such as XGBoost
- Let users choose their tickers and risk levels
- Add live trading via Alpaca API
- Implement daily auto-update scheduler
- Deploy to cloud with CI/CD



## 🚀 What Makes OptiTradeAI Different

While many portfolio optimization tools and libraries exist — such as **PyPortfolioOpt**, **QuantConnect**, or APIs like **PortfolioOptimizer.io** — **OptiTradeAI** stands out through **holistic integration, strategy flexibility, and real-world usability**:

### ✅ Multi-Signal Intelligence  
Unlike most optimizers that rely solely on price and return data, OptiTradeAI enhances decision-making by incorporating:
- Technical indicators (SMA, EMA)
- Insider sentiment (MSPR scores)
- News or social sentiment *(planned)*

This multi-layered signal processing leads to **more context-aware and adaptive portfolio strategies**.

### ✅ Strategy Selector: Swing vs Long-Term  
Traders have different goals. OptiTradeAI allows users to toggle between **swing trading** (short-term signals) and **long-term investing** (stable trend tracking), adapting portfolios to their time horizon and risk tolerance.

### ✅ Full Automation with Human-Level Insights  
From data ingestion and preprocessing to portfolio recommendations, everything is automated — yet powered by **interpretable insights**.  
No more manually chaining tools — OptiTradeAI is designed as a **full pipeline solution**.

### ✅ Future-Ready: ML-Enhanced Optimization  
The system is built with extensibility in mind. Coming soon:
- Custom sentiment classification via NLP
- Risk scoring through ML
- Clustering and reinforcement-based rebalancing

**OptiTradeAI is more than a toolkit — it’s a smart assistant for retail and emerging quant traders.**
