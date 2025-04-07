import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime

def download_stock_data(tickers, start_date, end_date):
    """
    Downloads historical stock data for the given tickers between start_date and end_date.
    Returns a DataFrame of adjusted closing prices.
    """

    print(f"Downloading data for: {tickers}")
    print(f"Period: {start_date} to {end_date}")

    try:
        data = yf.download(tickers,
                           start=start_date,
                           end=end_date,
                           auto_adjust=True,
                           actions=False,
                           progress=True)
        
        adj_close_prices = data['Close']

    except Exception as e:
        print(f"Error downloading data: {e}")
        adj_close_prices = pd.DataFrame()
    return adj_close_prices

def clean_and_save_data(df, csv_filename):
    """
    Cleans the DataFrame by checking for and dropping rows with missing values,
    then saves the clean DataFrame to a CSV file.
    Returns the cleaned DataFrame.
    """
    if df.empty:
        print("No data to clean or save.")
        return df

    print("\nDownloaded Data Head:")
    print(df.head())

    print("\nMissing Values Check:")
    print(df.isnull().sum())

    initial_rows = len(df)
    df_clean = df.dropna()
    if len(df_clean) < initial_rows:
        print(f"\nDropped {initial_rows - len(df_clean)} rows with NA values.")

    print("\nCleaned Data Head:")
    print(df_clean.head())

    try:
        df_clean.to_csv(csv_filename)
        print(f"\nData successfully saved to {csv_filename}")

        df_loaded = pd.read_csv(csv_filename, index_col=0, parse_dates=True)
        print(f"\nVerification: Loaded data from {csv_filename} Head:")
        print(df_loaded.head())
    except Exception as e:
        print(f"Error saving data to CSV: {e}")

    return df_clean

def calculate_returns_and_risk(df):
    """
    Calculates daily returns, annual mean returns, and annual covariance matrix
    from the provided DataFrame of stock prices.
    Returns the annual mean returns (mu) and the covariance matrix (Sigma).
    """
    if df.empty:
        print("No data available for calculating returns and risk.")
        return None, None

    daily_returns = df.pct_change().dropna()
    print("\nCalculated Daily Returns Head:")
    print(daily_returns.head())

    mu = daily_returns.mean() * 252
    Sigma = daily_returns.cov() * 252

    print("\nEstimated Annual Mean Returns (mu):")
    print(mu)
    print("\nEstimated Annual Covariance Matrix (Sigma):")
    print(Sigma)

    return mu, Sigma

if __name__ == "__main__":
    # Define parameters
    tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'JPM']
    start_date = '2020-01-01'
    end_date = datetime.now().strftime('%Y-%m-%d')
    csv_filename = 'data/stock_data.csv'

    # Step 1: Download data
    stock_data = download_stock_data(tickers, start_date, end_date)

    # Step 2: Clean data and save to CSV
    clean_data = clean_and_save_data(stock_data, csv_filename)

    # Step 3: Calculate returns and risk metrics
    mu, Sigma = calculate_returns_and_risk(clean_data)
