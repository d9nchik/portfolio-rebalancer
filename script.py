import math
import os

from dotenv import load_dotenv

load_dotenv()

current_asset_split = {
    'CSPX': 0.6,
    'EMIM': 0.2,
    'XUSE': 0.2,
}

# all prices in minimum currency value (cents)
current_stock_prices = {
    'CSPX': {'amount': 74082, 'currency': 'USD'},
    'EMIM': {'amount': 4064, 'currency': 'EUR'},
    'XUSE': {'amount': 669, 'currency': 'USD'},
}

exchange_rate = {
    'USD': 1,
    'EUR': 1.1822
}

stocks = {
    'CSPX': int(os.environ['STOCKS_CSPX']),
    'EMIM': int(os.environ['STOCKS_EMIM']),
    'XUSE': int(os.environ['STOCKS_XUSE']),
}

liquidity = {
    'USD': int(os.environ['LIQUIDITY_USD']),
    'EUR': int(os.environ['LIQUIDITY_EUR']),
}


def validate_split(split):
    """
    Validate the asset split to ensure it sums to 1.
    """
    total = sum(split.values())
    if total != 1:
        raise ValueError(f"Asset split must sum to 1, but got {total}")


if __name__ == '__main__':
    validate_split(current_asset_split)
    print("Asset split is valid.")

    # Calculate the total value of the portfolio in USD
    total_value_usd = 0

    for currency, amount in liquidity.items():
        total_value_usd += amount * exchange_rate[currency]

    for stock, amount in stocks.items():
        stock_price = current_stock_prices[stock]['amount']
        stock_currency = current_stock_prices[stock]['currency']
        total_value_usd += amount * stock_price * exchange_rate[stock_currency]

    total_value_usd = math.floor(total_value_usd)

    print(f"Total portfolio value in USD: {total_value_usd / 100:.2f} USD")

    print()
    # Calculate the value of each asset in the portfolio
    asset_values = {}
    for asset, split in current_asset_split.items():
        asset_value = total_value_usd * split
        asset_values[asset] = asset_value
    print("Target asset portfolio:")
    for asset, value in asset_values.items():
        print(f"{asset}: {value / 100:.2f} USD")

    # Calculate the value of each stock in the portfolio
    stock_values = {}
    for stock, amount in stocks.items():
        stock_price = current_stock_prices[stock]['amount']
        stock_currency = current_stock_prices[stock]['currency']
        stock_value = amount * stock_price * exchange_rate[stock_currency]
        stock_values[stock] = stock_value
    print()
    print("Stock values in portfolio:")
    for stock, value in stock_values.items():
        print(f"{stock}: {value / 100:.2f} USD")
    # Calculate the value of each currency in the portfolio
    currency_values = {}
    for currency, amount in liquidity.items():
        currency_value = amount * exchange_rate[currency]
        currency_values[currency] = currency_value
    print()
    print("Currency values in portfolio:")
    for currency, value in currency_values.items():
        print(f"{currency}: {value / 100:.2f} USD")

    # calculate the percent of each stock in the portfolio
    stock_percentages = {}
    for stock, amount in stocks.items():
        stock_price = current_stock_prices[stock]['amount']
        stock_currency = current_stock_prices[stock]['currency']
        stock_value = amount * stock_price * exchange_rate[stock_currency]
        stock_percentage = (stock_value / total_value_usd) * 100
        stock_percentages[stock] = stock_percentage
    print()
    print("Stock percentages in portfolio:")
    for stock, percentage in stock_percentages.items():
        print(f"{stock}: {percentage:.2f}%")

    # calculate the percent of each stock in the stock portfolio
    stock_portfolio_value = sum(stock_values.values())
    stock_percentages = {}
    for stock, value in stock_values.items():
        stock_percentage = (value / stock_portfolio_value) * 100
        stock_percentages[stock] = stock_percentage
    print()
    print("Stock percentages in stock portfolio:")
    for stock, percentage in stock_percentages.items():
        print(f"{stock}: {percentage:.2f}%")

    # advice on how to rebalance the asset portfolio use stock_portfolio value and current_asset_split
    print()
    print("Advice on how to rebalance the asset portfolio:")
    for asset, current_amount in stock_values.items():
        target_amount = asset_values[asset]
        amount = (target_amount - current_amount) / (current_stock_prices[asset]['amount'] * exchange_rate[
            current_stock_prices[asset]['currency']])
        if current_amount < target_amount:
            print(f"Buy {asset} x {amount:.2f} for {(target_amount - current_amount) / 100:.2f} USD")
        elif current_amount > target_amount:
            print(f"Sell {asset} x {-amount:.2f} for {(current_amount - target_amount) / 100:.2f} USD")
        else:
            print(f"{asset} is already balanced")
