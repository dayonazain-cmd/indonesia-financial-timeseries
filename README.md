# Indonesia Multi-Asset Market Analytics (2010–2026)

An end-to-end Data Science portfolio project analyzing the macroeconomic and financial time-series data of Indonesia and global markets. This project covers the entire pipeline: from rigorous data auditing and advanced statistical tests to Machine Learning modeling, business impact backtesting, and an interactive web dashboard.

## Project Overview
Financial time-series data is often fraught with hidden anomalies. This project demonstrates how to detect data quality issues (such as stale prices and decimal errors), engineer robust features, build honest predictive models, and optimize portfolio allocation using Modern Portfolio Theory.

## Repository Structure
- `notebooks/01_eda_analysis.ipynb`: Data auditing, cleaning, and exploratory data analysis.
- `notebooks/02_modeling.ipynb`: Feature engineering, XGBoost/Random Forest modeling, and evaluation.
- `notebooks/03_business_impact.ipynb`: Trading strategy simulation (Backtesting) and risk metrics (Sharpe Ratio, Max Drawdown).
- `notebooks/04_portfolio_optimization.ipynb`: Markowitz Efficient Frontier and asset allocation.
- `notebooks/05_advanced_analysis.ipynb`: Econometric tests (Granger Causality) and Volatility modeling (GARCH).
- `dashboard/app.py`: Interactive Streamlit dashboard.
- `data/`: Contains the raw and cleaned datasets.

## Key Findings

### 1. Data Quality Audit
Before modeling, a comprehensive audit revealed critical anomalies:
- **Stale Prices:** Found 300 days (7% of the dataset) where IHSG prices remained identical to the previous day—a clear artifact of scraping bugs, not actual market behavior.
- **Decimal Errors:** Detected 2 extreme anomalies in the USD/IDR exchange rate (e.g., 888.10 instead of 8881.0) which were corrected.
- **Forward-Filled Holidays:** Identified 147 days of global market holidays that were forward-filled.

### 2. Advanced Statistical Analysis
- **Granger Causality Test:** Proved statistically that Global Oil prices *cause* IHSG movements (p-value 0.0000), whereas daily USD/IDR movements do not significantly predict next-day IHSG direction (p-value 0.1681).
- **Volatility Clustering (GARCH):** Modeled market volatility to capture risk clustering, showing that high-volatility periods (e.g., COVID-19 crash) persist over time.

### 3. Machine Learning & Business Impact
- **Model:** XGBoost Classifier to predict the next-day direction of IHSG (Up/Down).
- **Validation:** Strict *Time-Series Split* (80% Train: 2010–2023, 20% Test: 2023–2026) to prevent data leakage.
- **Performance:** Achieved a realistic **49.16% accuracy** (slightly outperforming the 48.03% Naive Baseline). This highlights the extreme difficulty of daily market timing.
- **Backtesting:** Simulated trading strategy showed a Win Rate of 47.67% and a negative Sharpe Ratio, confirming that daily predictions are prone to the *whipsaw effect* and do not beat a passive Buy & Hold strategy in this specific timeframe.

### 4. Portfolio Optimization (Markowitz)
Using the Efficient Frontier (Max Sharpe Ratio) on 4 major assets, the algorithm calculated the optimal allocation to maximize returns while minimizing risk:
- **S&P 500:** 49.0%
- **Crude Oil (WTI):** 36.5%
- **IHSG:** 14.5%
- **Gold:** 0.0% (eliminated due to lower risk-adjusted returns in this period).

## Interactive Dashboard
The project includes a fully interactive Streamlit dashboard featuring:
- **Market & Risk Overview:** Dual-axis charts with rolling volatility and crisis annotations.
- **AI Model Insights:** Backtesting simulations and XGBoost feature importance.
- **Portfolio Optimization:** Interactive Donut chart of the Markowitz allocation.
- **Data Quality:** Transparent display of data anomalies and raw data tables.

## Technologies Used
- **Programming:** Python 3.14
- **Data Manipulation:** Pandas, NumPy
- **Machine Learning:** Scikit-Learn, XGBoost
- **Statistical Modeling:** Statsmodels, Arch (GARCH)
- **Visualization:** Plotly, Matplotlib, Seaborn
- **Dashboard:** Streamlit

## How to Run Locally
1. Clone this repository:
   ```bash
   git clone https://github.com/dayonazain-cmd/indonesia-financial-timeseries.git
   cd indonesia-financial-timeseries