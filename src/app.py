import streamlit as st
import pandas as pd
from datetime import datetime
from time import time
import yfinance as yf
from data_collection import download_stock_data, clean_and_save_data, calculate_returns_and_risk
from problem_formulation import construct_qubo
from classical_solver import solve_qubo_classically
# from quantum_solver import solve_qubo as solve_qubo_quantum  # Uncomment if quantum works

st.set_page_config(page_title="Portfolio Optimizer", layout="wide")
st.title("🧠 Portfolio Optimizer")
st.markdown("Easily find your **optimal stock portfolio** using modern optimization techniques.")

# --- PRESETS (Optional) ---
preset = st.sidebar.radio(
    "Parameter Presets", ["Balanced", "Conservative", "Aggressive", "Custom"], horizontal=True
)
def preset_vals(name):
    if name == "Conservative": return 3.0, 20.0
    if name == "Aggressive": return 0.5, 5.0
    return 1.0, 10.0 # Balanced or default

lambda_val, gamma = preset_vals(preset)
if preset == "Custom":
    lambda_val = st.sidebar.number_input(
        "λ (risk aversion)", min_value=0.0, max_value=100.0, value=1.0, step=0.1,
        help="How much you care about minimizing risk. Higher λ = safer."
    )
    gamma = st.sidebar.number_input(
        "γ (constraint penalty)", min_value=0.0, max_value=1000.0, value=10.0, step=1.0,
        help="Enforces that exactly K stocks are picked. Usually leave at 10."
    )
else:
    st.sidebar.info(f"λ: {lambda_val}, γ: {gamma} (Set to preset: {preset})")

# ----- MAIN INPUTS -----
with st.expander("How to Use (Click to Expand)", expanded=True):
    st.markdown("""
    **Instructions:**  
    1. Enter comma-separated stock tickers (e.g., `AAPL,MSFT,GOOGL`).  
    2. Choose your analysis period and number of stocks (`K`).  
    3. Click **Run Optimizer**.  
    _Change parameter preset on the left for different strategies._
    """)

tickers = st.text_input(
    "Stock Tickers (comma-separated):", 
    "AAPL,MSFT,GOOGL,AMZN,JPM", 
    help="E.g., AAPL, MSFT, GOOGL, AMZN, JPM"
)
col1, col2, col3 = st.columns(3)
with col1:
    start_date = st.date_input(
        "Start Date", datetime(2020, 1, 1),
        help="Start of your backtest window"
    )
with col2:
    end_date = st.date_input(
        "End Date", datetime.now(),
        help="End of your backtest window"
    )
with col3:
    K = st.number_input(
        "Stocks to pick (K)", min_value=1, max_value=20, value=2,
        help="Number of stocks to select for your portfolio"
    )

st.divider()
run_button = st.button("🚀 Run Optimizer")

if run_button:
    try:
        t0 = time()
        tickers_list = [t.strip().upper() for t in tickers.split(',') if t.strip()]
        if K > len(tickers_list):
            st.warning("K cannot be more than the number of stocks!")
            st.stop()
        st.info(f"Fetching data for: {', '.join(tickers_list)}")
        stock_data = download_stock_data(tickers_list, str(start_date), str(end_date))
        clean_data = clean_and_save_data(stock_data, 'stock_data.csv')
        mu, Sigma = calculate_returns_and_risk(clean_data)
        st.success("Data downloaded & cleaned successfully!")

        # Show a preview
        with st.expander("Show price data table"):
            st.dataframe(clean_data.tail(10))

        # --------- Show latest price and chart in dropdown only ---------
        with st.expander("Show latest stock prices"):
            for t in tickers_list:
                try:
                    data = yf.download(t, period="1mo", progress=False)
                    if data is not None and not data.empty and 'Close' in data:
                        close_prices = data['Close'].dropna()
                        if not close_prices.empty:
                            price = float(close_prices.iloc[-1])
                            st.write(f"**{t}:** ${price:.2f}")
                            st.line_chart(close_prices)
                        else:
                            st.warning(f"{t}: No recent closing prices found.")
                    else:
                        st.warning(f"{t}: No data returned by yfinance.")
                except Exception as ex:
                    st.error(f"{t}: Could not fetch price. ({ex})")
        # --------------------------------------------------------------

        # Construct QUBO
        Q = construct_qubo(mu, Sigma, K, lambda_val=lambda_val, gamma=gamma)

        # Solve
        sol, val = solve_qubo_classically(Q)

        selected = [tickers_list[i] for i in range(len(sol)) if sol[i] == 1]
        not_selected = [tickers_list[i] for i in range(len(sol)) if sol[i] == 0]
        st.subheader("📊 Optimization Results")
        st.markdown("#### 🏆 **Final Portfolio Decision:**")
        for idx, (t, sel) in enumerate(zip(tickers_list, sol)):
            if sel == 1:
                st.success(f"✅ {t}: **INVEST (Buy/Hold)**")
            else:
                exp_return = float(mu[idx]) if hasattr(mu, '__getitem__') else 0
                if exp_return > 0:
                    st.warning(f"🟡 {t}: **HOLD** (not in optimal portfolio, but expected return > 0)")
                else:
                    st.error(f"❌ {t}: **SELL** (expected return ≤ 0)")

        with st.expander("Show optimization solution bitstring (for nerds)"):
            st.markdown(f"**Bitstring:** `{sol}`")
            st.markdown(f"**Objective value:** `{val}`")

        # Download button
        results_df = pd.DataFrame({
            "Ticker": tickers_list,
            "In Portfolio (1=Yes)": sol
        })
        st.download_button("Download Portfolio Selection (CSV)", results_df.to_csv(index=False), "portfolio.csv")

        # --- Show mean returns and risk for all stocks ---
        st.markdown("### 📈 Stock Mean Returns & Risk")
        stats_df = pd.DataFrame({
            "Expected Return": mu,
            "Risk (Variance)": Sigma.values.diagonal()
        })
        st.dataframe(stats_df)
        st.bar_chart(stats_df["Expected Return"])

        # --- Show scatterplot Risk vs Return ---
        st.markdown("#### Risk vs Return (selected in green):")
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots()
        colors = ['g' if s in selected else 'r' for s in tickers_list]
        ax.scatter(stats_df["Risk (Variance)"], stats_df["Expected Return"], c=colors)
        for i, t in enumerate(tickers_list):
            ax.annotate(t, (stats_df["Risk (Variance)"][i], stats_df["Expected Return"][i]))
        ax.set_xlabel("Risk (Annualized Variance)")
        ax.set_ylabel("Expected Return")
        st.pyplot(fig)

        st.toast(f"Done in {time()-t0:.2f} seconds! Adjust parameters and re-run for different results.", icon="🎉")
    except Exception as e:
        st.error(f"❌ An error occurred: {e}")
        st.info("Tip: Check ticker spellings, date ranges, or try a smaller K.")

# ---- Footer & parameter summary
st.divider()
with st.expander("What do the parameters mean?"):
    st.markdown("""
- **K (Stocks to pick):** Number of stocks the optimizer will choose for your portfolio.
- **lambda (λ):** How much to avoid risk (higher = less risk).
- **gamma (γ):** How strictly to enforce the “pick K” rule.

_This app fetches real data, runs portfolio optimization, and gives you a simple, transparent recommendation._  
    """)
st.markdown("---\nMade with ❤️ by Ali Towaiji. [GitHub](https://github.com/Towaiji) | [LinkedIn](https://www.linkedin.com/in/alitowaiji/)")
