from alpha_vantage.timeseries import TimeSeries
from datetime import datetime, timedelta
import json


class Stonk:
    def __init__(self,
                 stock_name,
                 ticker,
                 api_token):
        self.name = stock_name
        self.ticker = ticker
        self.api_token = api_token
        self.stock_string = None

    @staticmethod
    def get_col(column):
        name = column.split(" ")[1]
        return name

    @staticmethod
    def get_date_from_string(string):
        dt = string.split(" ")[0]
        return dt

    def get_stock_data(self):
        ts = TimeSeries(key=self.api_token, output_format='pandas')
        data, meta_data = ts.get_intraday(symbol=self.ticker, interval='1min', outputsize='full')
        data = data.rename(self.get_col, axis='columns')

        dates = data.groupby(by=self.get_date_from_string, axis='index').last()
        return dates

    def get_stock_string(self):
        if self.stock_string:
            return self.stock_string

        dates = self.get_stock_data()
        today = datetime.strftime(datetime.now(), "%Y-%m-%d")
        week_ago = datetime.strftime(datetime.now() - timedelta(7), "%Y-%m-%d")

        recent = dates.loc[today]['close']
        today = datetime.strftime(datetime.now(), "%m/%d/%Y")
        oldest = dates.loc[week_ago]['close']
        week_ago = datetime.strftime(datetime.now() - timedelta(6), "%Y-%m-%d")
        delta = round(100*(recent-oldest)/recent, 1)

        if delta < 0:
            change = "down"
            react = "Yay!"
            delta = abs(delta)
        else:
            change = "up"
            react = "Boo."

        recent = format(recent, '.2f')
        oldest = format(oldest, '.2f')

        ret_str = "{name} is {chg} {delta}% at close from ${op} on {old} to ${np} on {new}. {react}"
        self.stock_string = ret_str.format(name=self.name,
                                           chg=change,
                                           delta=delta,
                                           op=oldest,
                                           old=week_ago,
                                           np=recent,
                                           new=today,
                                           react=react)
        return self.stock_string


