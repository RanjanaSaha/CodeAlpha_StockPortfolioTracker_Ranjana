import requests
import pandas as pd

# API configuration
API_KEY = '10GUWDNHP35BPKJC'  # Replace with your Alpha Vantage API key
BASE_URL = 'https://www.alphavantage.co/query'

# Function to get real-time stock data
def get_stock_data(symbol):
    url = f'{BASE_URL}?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=5min&apikey={API_KEY}'
    response = requests.get(url)
    data = response.json()
    
    if "Time Series (5min)" in data:
        time_series = data["Time Series (5min)"]
        df = pd.DataFrame.from_dict(time_series, orient='index', dtype=float)
        df.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
        df.index = pd.to_datetime(df.index)
        return df
    else:
        return None

# Portfolio class to manage stocks
class Portfolio:
    def _init_(self):
        self.stocks = {}

    def add_stock(self, symbol, shares):
        self.stocks[symbol] = self.stocks.get(symbol, 0) + shares
        print(f'Added {shares} shares of {symbol}.')

    def remove_stock(self, symbol, shares):
        if symbol in self.stocks and self.stocks[symbol] >= shares:
            self.stocks[symbol] -= shares
            if self.stocks[symbol] == 0:
                del self.stocks[symbol]
            print(f'Removed {shares} shares of {symbol}.')
        else:
            print(f'Not enough shares of {symbol} to remove.')

    def view_portfolio(self):
        for symbol, shares in self.stocks.items():
            print(f'{symbol}: {shares} shares')

    def track_portfolio(self):
        for symbol in self.stocks:
            print(f'Tracking {symbol}...')
            stock_data = get_stock_data(symbol)
            if stock_data is not None:
                latest_data = stock_data.iloc[0]
                print(f'{symbol}: Latest Price: ${latest_data["Close"]:.2f}')
            else:
                print(f'Failed to retrieve data for {symbol}.')

# Main program
def main():
    portfolio = Portfolio()

    while True:
        print("\n--- Stock Portfolio Tracker ---")
        print("1. Add Stock")
        print("2. Remove Stock")
        print("3. View Portfolio")
        print("4. Track Portfolio")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ")

        if choice == '1':
            symbol = input("Enter the stock symbol (e.g., AAPL): ").upper()
            shares = int(input(f"Enter the number of shares to add for {symbol}: "))
            portfolio.add_stock(symbol, shares)
        
        elif choice == '2':
            symbol = input("Enter the stock symbol (e.g., AAPL): ").upper()
            shares = int(input(f"Enter the number of shares to remove for {symbol}: "))
            portfolio.remove_stock(symbol, shares)

        elif choice == '3':
            portfolio.view_portfolio()

        elif choice == '4':
            portfolio.track_portfolio()

        elif choice == '5':
            print("Exiting Stock Portfolio Tracker.")
            break

        else:
            print("Invalid choice! Please select a valid option.")

if __name__ == "_main_":
    main()
