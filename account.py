from mail_gw_api_wrapper import MailGW
from bs4 import BeautifulSoup
from twocaptcha import TwoCaptcha
import os


class Account(MailGW, TwoCaptcha):
    def __init__(self, username):
        MailGW.__init__(self, username)

        TwoCaptcha.__init__(self, os.environ.get('2captcha_key'))

        self.site_key = '6LeTnxkTAAAAAN9QEuDZRpn90WwKk_R1TRW_g-JC'

        self.email = None

        self.headers.update({
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36',
        })
