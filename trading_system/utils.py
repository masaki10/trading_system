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
from Crypto.Cipher import AES

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import config as cf

line_bot_api = LineBotApi(cf.CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(cf.CHANNEL_SECRET)

def send_message(message):
    line_bot_api.push_message(cf.USER_ID, TextSendMessage(text=message))

def decrypt_data(ciphertext, tag, filename):
    with open(filename, "rb") as f:
        key = f.read(16)
        nonce = f.read(16)
    cipher_dec = AES.new(key, AES.MODE_EAX, nonce)
    data = cipher_dec.decrypt_and_verify(ciphertext, tag)
    return data

def get_pwd():
    pass

def get_order_num():
    pass