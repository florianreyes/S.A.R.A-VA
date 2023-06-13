import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime
from stock_list import stocks



def get_stocks(stock, action):
    stock_l = stock.lower()
    action_l = action.lower().split(' ')
    print(action_l)

    if stock_l in stocks:
        ticker = yf.Ticker(stocks[stock_l])
    else:
        print("Sorry, I couldn't find that stock.")
        return
    for action in action_l:
        if action == "dividends":
            df = ticker.dividends
            print(df)
            data = df.resample('Y').sum()
            data = data.reset_index()
            data['Year'] = data['Date'].dt.year
            plt.figure()
            plt.bar(data['Year'], data['Dividends'])
            plt.xlabel('Year')
            plt.ylabel('Dividend Yield ($)')
            plt.title('{} historic dividend yield'.format(stock))
            plt.xlim(2000, datetime.now().year)
            plt.show()
        elif action == "cash" or action == "cashflow":
            print(ticker.cashflow)
        elif action == "major":
            print(ticker.major_holders)
        elif action == "institutional":
            print(ticker.institutional_holders)
        else:
            print("Sorry, I couldn't find that information.")


get_stocks("general electric", "institutional")