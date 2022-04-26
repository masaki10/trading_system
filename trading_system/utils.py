from selenium import webdriver
import chromedriver_binary
import time
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import config as cf

line_bot_api = LineBotApi(cf.CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(cf.CHANNEL_SECRET)

def send_message(message):
    line_bot_api.push_message(cf.USER_ID, TextSendMessage(text=message))

# def login_to_rakuten():
#     driver = webdriver.Chrome()
#     driver.get(cf.RAKUTEN_URL)
#     time.sleep(1)
        
#     id_el = driver.find_element_by_name("loginid")
#     id_el.send_keys(cf.RAKUTEN_ID)

#     passwd_el = driver.find_element_by_name("passwd")
#     passwd_el.send_keys(cf.RAKUTEN_PASSWORD)

#     try:
#         passwd_el.submit()
#         return "ok"
#     except:
#         return None