import requests


class Stock:
    STOCK_API_ENDPOINT = "https://www.alphavantage.co/query?"

    def __init__(self, symbol, apikey, function="TIME_SERIES_DAILY", outputsize="compact"):
        self.function = function
        self.symbol = symbol
        self.outputsize = outputsize
        self.apikey = apikey
        self.time_series_data = self.get_stock_data()["Time Series (Daily)"]
        self.time_series_iterator = iter(self.time_series_data)
        self.yesterday_closing_price = float(self.time_series_data[self.yesterday_stock_closing()]["4. close"])
        self.previous_closing_price = float(self.time_series_data[self.previous_day_closing()]['4. close'])
        self.percentage_change = self.get_closing_percentage_change()

    def get_stock_data(self):
        stock_parameters = {
            "function": self.function,
            "symbol": self.symbol,
            "outputsize": self.outputsize,
            "apikey": self.apikey
        }

        response = requests.get(url=self.STOCK_API_ENDPOINT, params=stock_parameters)
        response.raise_for_status()
        return response.json()

    def yesterday_stock_closing(self):
        try:
            return next(self.time_series_iterator)
        except StopIteration:
            return None

    def previous_day_closing(self):
        try:
            return next(self.time_series_iterator)
        except StopIteration:
            return None

    def get_closing_percentage_change(self):
        difference = self.yesterday_closing_price - self.previous_closing_price
        change = difference / self.yesterday_closing_price
        return float(f"{change:.2f}")

    def is_5percent_change(self):
        return abs(self.percentage_change) >= 5

    def up_or_down(self):
        if self.percentage_change > 0:
            return "🔺"
        return "🔻"