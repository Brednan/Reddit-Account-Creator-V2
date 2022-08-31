from mail_gw_api_wrapper import MailGW
from bs4 import BeautifulSoup
from selenium.webdriver import Firefox, FirefoxProfile
from selenium.webdriver.common.by import By


class Account(MailGW):
    def __init__(self, credentials):
        MailGW.__init__(self, credentials[0])

        self.email = None

        self.headers.update({
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36',
        })
