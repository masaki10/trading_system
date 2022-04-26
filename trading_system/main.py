import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
import config as cf
from fund import Fund

if __name__ == "__main__":
    leve_nas = Fund(cf.FUND_URL, cf.RATE, cf.PRICE)
    leve_nas.get_basic_price()
    if leve_nas.is_trading():
        leve_nas.buy()
        # print(leve_nas.is_trading())