import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from src.durations import Durations

def calculate_streaks(df: pd.DataFrame) -> tuple[list, list]:
    above_sma = df['Close'] > df['SMA_200']
    above_streaks = []
    below_streaks = []
    current_streak = 0
    current_state = None
    
    for is_above in above_sma:
        if current_state is None:
            current_state = is_above
            current_streak = 1
        elif current_state == is_above:
            current_streak += 1
        else:
            if current_state:
                above_streaks.append(current_streak)
            else:
                below_streaks.append(current_streak)
            current_state = is_above
            current_streak = 1
    
    if current_state:
        above_streaks.append(current_streak)
    else:
        below_streaks.append(current_streak)
    
    return above_streaks, below_streaks

def get_current_streak(df: pd.DataFrame) -> tuple[int, bool]:
    current_above = df['Close'].iloc[-1] > df['SMA_200'].iloc[-1]
    current_streak = 1
    
    for i in range(len(df) - 2, -1, -1):
        is_above = df['Close'].iloc[i] > df['SMA_200'].iloc[i]
        if is_above == current_above:
            current_streak += 1
        else:
            break
    
    return current_streak, current_above

def plot_stock_data(full_df: pd.DataFrame, plot_df: pd.DataFrame, ticker: str, duration: Durations) -> None:    
    fig = plt.figure(figsize=(14, 8))
    
    # Main price chart (50%)
    ax1 = plt.subplot2grid((8, 2), (0, 0), colspan=2, rowspan=4)
    ax1.plot(plot_df.index, plot_df['Close'], label='Close Price', linewidth=1.5, color='#2E86AB')
    ax1.plot(plot_df.index, plot_df['SMA_200'], label='200-day SMA', linewidth=2, color="red", linestyle='--', alpha=0.3)
    ax1.plot(plot_df.index, plot_df['SMA_50'], label='50-day SMA', linewidth=2, color="green", linestyle='--', alpha=0.3)
    ax1.set_ylabel(f'{ticker} Share Price', fontsize=12)
    ax1.grid(True, alpha=0.3)
    ax1.legend()

    # Distance from SMA chart (25%)
    ax2 = plt.subplot2grid((8, 2), (4, 0), colspan=2, rowspan=2)
    distance = (plot_df['Close'] - plot_df['SMA_200']) / plot_df['SMA_200'] * 100
    ax2.plot(plot_df.index, distance, color='black', linewidth=1)
    ax2.fill_between(plot_df.index, distance, 0, where=(distance > 0), color='green', alpha=0.3)
    ax2.fill_between(plot_df.index, distance, 0, where=(distance <= 0), color='red', alpha=0.3)
    ax2.axhline(y=0, color='black', linestyle='-', linewidth=1)
    ax2.set_ylabel('Distance from 200-SMA (%)', fontsize=12)
    ax2.grid(True, alpha=0.3)

    # Streak histograms - side by side (25%)
    above_streaks, below_streaks = calculate_streaks(full_df)
    current_streak, is_above = get_current_streak(full_df)
    
    # Calculate percentiles
    above_percentile = (sum(1 for s in above_streaks if s < current_streak) / len(above_streaks)) * 100 if is_above else 0
    below_percentile = (sum(1 for s in below_streaks if s < current_streak) / len(below_streaks)) * 100 if not is_above else 0
    
    ax3 = plt.subplot2grid((8, 2), (6, 0), rowspan=2)
    ax3.hist(above_streaks, bins=20, alpha=0.7, color='green', edgecolor='black')
    title = f'Above 200-SMA (avg: {np.mean(above_streaks):.0f}d)'
    if is_above:
        title += f' Current: {above_percentile:.1f}th percentile'
    ax3.set_title(title, fontsize=10)
    ax3.set_ylabel('Frequency', fontsize=12)
    ax3.set_xlabel('Days')
    ax3.grid(True, alpha=0.3)
    if is_above:
        ax3.axvline(current_streak, color='black', linestyle='--', linewidth=2, label=f'Today: {current_streak}d')
        ax3.legend()
    
    ax4 = plt.subplot2grid((8, 2), (6, 1), rowspan=2)
    ax4.hist(below_streaks, bins=20, alpha=0.7, color='red', edgecolor='black')
    title = f'Below 200-SMA (avg: {np.mean(below_streaks):.0f}d)'
    if not is_above:
        title += f' Current: {below_percentile:.1f}th percentile'
    ax4.set_title(title, fontsize=10)
    ax4.set_ylabel('Frequency', fontsize=12)
    ax4.set_xlabel('Days')
    ax4.grid(True, alpha=0.3)
    if not is_above:
        ax4.axvline(current_streak, color='black', linestyle='--', linewidth=2, label=f'Today: {current_streak}d')
        ax4.legend()

    plt.tight_layout()
    plt.savefig(f'plots/{ticker.lower()}_{duration.name.lower()}_chart.png', dpi=300)
    # plt.show()
