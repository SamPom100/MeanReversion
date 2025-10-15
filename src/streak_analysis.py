import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def calculate_streaks(df: pd.DataFrame) -> tuple[list, list]:
    """Calculate consecutive streaks above and below 200-day SMA"""
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
    
    # Add final streak
    if current_state:
        above_streaks.append(current_streak)
    else:
        below_streaks.append(current_streak)
    
    return above_streaks, below_streaks

def plot_streak_histogram(above_streaks: list, below_streaks: list, ticker: str) -> None:
    """Plot histogram of streaks above and below 200-day SMA"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Above SMA streaks
    ax1.hist(above_streaks, bins=20, alpha=0.7, color='green', edgecolor='black')
    ax1.set_title(f'{ticker} - Days Above 200-day SMA')
    ax1.set_xlabel('Consecutive Days')
    ax1.set_ylabel('Frequency')
    ax1.grid(True, alpha=0.3)
    ax1.axvline(np.mean(above_streaks), color='red', linestyle='--', label=f'Mean: {np.mean(above_streaks):.1f}')
    ax1.legend()
    
    # Below SMA streaks
    ax2.hist(below_streaks, bins=20, alpha=0.7, color='red', edgecolor='black')
    ax2.set_title(f'{ticker} - Days Below 200-day SMA')
    ax2.set_xlabel('Consecutive Days')
    ax2.set_ylabel('Frequency')
    ax2.grid(True, alpha=0.3)
    ax2.axvline(np.mean(below_streaks), color='green', linestyle='--', label=f'Mean: {np.mean(below_streaks):.1f}')
    ax2.legend()
    
    plt.tight_layout()
    plt.savefig(f'plots/{ticker.lower()}_streak_histogram.png', dpi=300)
    plt.show()

def analyze_current_streak(df: pd.DataFrame, ticker: str) -> None:
    """Analyze the current streak and compare to historical data"""
    above_streaks, below_streaks = calculate_streaks(df)
    
    # Determine current streak
    current_above = df['Close'].iloc[-1] > df['SMA_200'].iloc[-1]
    current_streak = 1
    
    for i in range(len(df) - 2, -1, -1):
        is_above = df['Close'].iloc[i] > df['SMA_200'].iloc[i]
        if is_above == current_above:
            current_streak += 1
        else:
            break
    
    if current_above:
        all_streaks = above_streaks
        streak_type = "above"
    else:
        all_streaks = below_streaks
        streak_type = "below"
    
    percentile = (sum(1 for s in all_streaks if s < current_streak) / len(all_streaks)) * 100
    
    print(f"\n{ticker} Current Streak Analysis:")
    print(f"Currently {current_streak} days {streak_type} 200-day SMA")
    print(f"This is longer than {percentile:.1f}% of all {streak_type} streaks")
    print(f"Average {streak_type} streak: {np.mean(all_streaks):.1f} days")
    print(f"Longest {streak_type} streak: {max(all_streaks)} days")
    
    plot_streak_histogram(above_streaks, below_streaks, ticker)
