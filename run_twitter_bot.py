from pull_stocks import Stonk
import json


def get_api_token(name):
    filename = "secrets.json"
    with open(filename, 'r') as f:
        secret = json.load(f)["api_tokens"].get(name)

    if secret:
        return secret
    else:
        raise KeyError("Secret for {} not found".format(name))


def main():
    vantage_api = get_api_token("vantage_api_token")
    geo_stonk = Stonk("Geo Group", "GEO", vantage_api)
    cxw_stonk = Stonk("CoreCivic", "CXW", vantage_api)
    print(geo_stonk.get_stock_string())
    print(cxw_stonk.get_stock_string())

if __name__ == '__main__':
    main()
