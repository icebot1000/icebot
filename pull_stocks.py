from alpha_vantage.timeseries import TimeSeries
from datetime import datetime, timedelta
import json

def get_secret(name):
    filename = "secrets.json"
    with open(filename, 'r') as f:
        secret = json.load(f).get(name)

    if secret:
        return secret
    else:
        raise KeyError("Secret for {} not found".format(name))


def get_col(column):
    name = column.split(" ")[1]
    return name


def get_date_from_string(string):
    dt = string.split(" ")[0]
    return dt


def get_stock_string(symbol, name):
    api_token = get_secret("vantage_api_token")
    ts = TimeSeries(key=api_token, output_format='pandas')
    data, meta_data = ts.get_intraday(symbol=symbol, interval='1min', outputsize='full')
    data = data.rename(get_col, axis='columns')

    today = datetime.strftime(datetime.now(), "%Y-%m-%d")
    week_ago = datetime.strftime(datetime.now() - timedelta(6), "%Y-%m-%d")

    dates = data.groupby(by=get_date_from_string, axis='index').last()

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
    return "{name} is {chg} {delta}% at close from ${op} on {old} to ${np} on {new}. {react}".format(name=name,
                                                                                                     chg=change,
                                                                                                     delta=delta,
                                                                                                     op=oldest,
                                                                                                     old=week_ago,
                                                                                                     np=recent,
                                                                                                     new=today,
                                                                                                     react=react)


def main():
    print(get_stock_string("GEO", "Geo Group"))
    print(get_stock_string("CXW", "CoreCivic"))


if __name__ == '__main__':
    main()
