from selenium import webdriver
from selenium.webdriver.common.by import By
import chromedriver_binary
import time

import os
import sys

from trading_system.utils import send_message
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import config as cf
from utils import send_message

class Fund:
    def __init__(self, fund_url, rate=None, price=None, price_dic=None, is_rate_for_yesterday=False, is_base_price=False):
        if is_base_price == is_rate_for_yesterday:
            raise
        if is_rate_for_yesterday and (rate is None or price is None):
            raise
        if is_base_price and price_dic is None:
            raise
        self.fund_url = fund_url
        # self.symbol = symbol
        if is_rate_for_yesterday:
            self.rate = rate
            self.price = price
        if is_base_price:
            self.price_dic = sorted(price_dic.items())
        self.is_rate_for_yesterday = is_rate_for_yesterday
        self.is_base_price = is_base_price
        self.driver = webdriver.Chrome()

    def get_basic_price(self):
        self.driver.get(self.fund_url)
        time.sleep(1)

        fund_name_el = self.driver.find_element(by = By.CLASS_NAME, value="fund-name")
        self.fund_name = fund_name_el.text
            
        base_price_el = self.driver.find_element_by_class_name("value-01")
        self.base_price = int(base_price_el.text.replace(",", ""))

        rate_for_yesterday_el = self.driver.find_elements(by=By.CLASS_NAME, value="ratio-01")

        if rate_for_yesterday_el[1].text[0] == "-":
            self.is_down = True
        elif rate_for_yesterday_el[1].text[0] == "+":
            self.is_down = False
        else:
            raise

        self.rate_for_yesterday = float(rate_for_yesterday_el[1].text[1:])

        message = f"ファンド名 : {self.fund_name}\n基準価格 : {self.base_price}\n"
        if self.is_down:
            message += f"前日比 : -{self.rate_for_yesterday}"
        else:
            message += f"前日比 : +{self.rate_for_yesterday}"

        send_message(message)

    def is_trading(self):
        if self.is_rate_for_yesterday:
            if not self.is_down:
                return False
            
            if self.rate_for_yesterday > self.rate:
                return True
            
            return False
        elif self.is_base_price:
            for key, value in self.price_dic:
                if self.base_price < key:
                    return True
            return False

    def _buy(self, price):
        self.driver.get(self.fund_url)
        time.sleep(1)

        login_form_btn_el = self.driver.find_element_by_class_name("login-form--toggle-button")
        login_form_btn_el.click()
        time.sleep(0.5)

        id_el = self.driver.find_element_by_name("loginid")
        id_el.send_keys(cf.RAKUTEN_ID)

        passwd_el = self.driver.find_element_by_name("passwd")
        passwd_el.send_keys(cf.RAKUTEN_PASSWORD)

        try:
            passwd_el.submit()
        except:
            raise

        send_message('楽天証券にログインしました')

        spot_order_el = self.driver.find_element(
            by=By.CSS_SELECTOR, value="a[href*='JavaScript:showOrder(']")
        spot_order_el.click()
        time.sleep(1)

        price_el = self.driver.find_element(by=By.NAME, value="orderPriceUnit")
        price_el.send_keys(price)

        prospectus_el = self.driver.find_element(
            by=By.NAME, value="prospectusAgreementCheck")
        prospectus_el.click()

        comform_btn_el = self.driver.find_element(
            by=By.CSS_SELECTOR, value="a[onclick*='if(checkDoubleSend()==false)']")
        comform_btn_el.click()
        time.sleep(1)

        order_pass_el = self.driver.find_element(by=By.NAME, value="password")
        order_pass_el.send_keys(cf.ORDER_PASS)

        order_btn_el = self.driver.find_element(by=By.ID, value="sbm")
        order_btn_el.click()
        time.sleep(1)

        message = f"ファンド名 : {self.fund_name}\n買い付け価格 : {price}"
        send_message(message)

    def buy(self):
        if self.is_rate_for_yesterday:
            self._buy(self.price)
        elif self.is_base_price:
            for key, value in self.price_dic:
                if self.base_price < key:
                    self._buy(value)
                    break