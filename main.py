from src.stock_data import get_stock_data
from src.plot import plot_stock_data
from src.durations import Durations

TICKER = "QQQ"
DURATION = Durations.TEN_YEARS

if __name__ == "__main__":
    full_data, plot_data = get_stock_data(TICKER, DURATION)
    plot_stock_data(full_data, plot_data, TICKER, DURATION)