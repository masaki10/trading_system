import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
import config as cf
from fund import Fund

def run_trading():
    leve_nas = Fund(cf.FUND_URL, cf.RATE, cf.PRICE, cf.PRICE_DIC, cf.IS_RATE_FOR_YESTERDAY, cf.IS_BASE_PRICE)
    leve_nas.get_basic_price()
    if leve_nas.is_trading():
        leve_nas.buy()

if __name__ == "__main__":
    run_trading()