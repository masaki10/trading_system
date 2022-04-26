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
    def __init__(self, fund_url, rate, price):
        self.fund_url = fund_url
        # self.symbol = symbol
        self.rate = rate
        self.price = price
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
            message += f"-{self.rate_for_yesterday}"
        else:
            message += f"+{self.rate_for_yesterday}"

        send_message(message)

    def is_trading(self):
        if not self.is_down:
            return False
        
        if self.rate_for_yesterday > self.rate:
            return True
        
        return False

    def buy(self):
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
        price_el.send_keys(self.price)

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

        message = f"ファンド名 : {self.fund_name}\n買い付け価格 : {self.price}\n"
        send_message(message)