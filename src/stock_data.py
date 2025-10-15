import yfinance as yf
from src.durations import Durations
import pandas as pd

def get_stock_data(ticker: str, duration: Durations) -> tuple[pd.DataFrame, pd.DataFrame]:
    stock = yf.Ticker(ticker)

    full_df = stock.history(period="max")
    full_df['SMA_50'] = full_df['Close'].rolling(window=50).mean()
    full_df['SMA_200'] = full_df['Close'].rolling(window=200).mean()
    full_df = full_df.dropna(subset=['SMA_200'])
    full_df = full_df.drop(columns=['Open', 'High', 'Low', 'Dividends', 'Stock Splits'])

    if duration == Durations.MAX:
        plot_df = full_df
    else:
        end_date = pd.Timestamp.now(tz=full_df.index.tz)
        start_date = end_date - pd.Timedelta(days=duration.value[0])
        plot_df = full_df[full_df.index >= start_date]

    if full_df.empty or plot_df.empty:
        raise ValueError(f"No data found for ticker {ticker}.")

    return full_df, plot_df