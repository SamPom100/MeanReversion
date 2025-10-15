import pandas as pd
import matplotlib.pyplot as plt
from src.durations import Durations

def plot_stock_data(full_df: pd.DataFrame, plot_df: pd.DataFrame, ticker: str, duration: Durations) -> None:    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 8), height_ratios=[3, 1])

    # Main price chart - use plot_df
    ax1.plot(plot_df.index, plot_df['Close'], label='Close Price', linewidth=1.5, color='#2E86AB')
    ax1.plot(plot_df.index, plot_df['SMA_200'], label='200-day SMA', linewidth=2, color="red", linestyle='--', alpha=0.3)
    ax1.plot(plot_df.index, plot_df['SMA_50'], label='50-day SMA', linewidth=2, color="green", linestyle='--', alpha=0.3)
    ax1.set_ylabel(f'{ticker} Share Price', fontsize=12)
    ax1.grid(True, alpha=0.3)    

    # Distance from SMA chart - use plot_df
    distance = (plot_df['Close'] - plot_df['SMA_200']) / plot_df['SMA_200'] * 100
    ax2.plot(plot_df.index, distance, color='black', linewidth=1)
    ax2.fill_between(plot_df.index, distance, 0, where=(distance > 0), color='green', alpha=0.3)
    ax2.fill_between(plot_df.index, distance, 0, where=(distance <= 0), color='red', alpha=0.3)
    ax2.axhline(y=0, color='black', linestyle='-', linewidth=1)
    ax2.set_ylabel('Distance from 200-SMA (%)', fontsize=12)
    ax2.set_xlabel('Date', fontsize=12)
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(f'plots/{ticker.lower()}_{duration.name.lower()}_chart.png', dpi=300)
    plt.show()
