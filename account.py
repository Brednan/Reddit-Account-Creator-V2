from mail_gw_api_wrapper import MailGW
from bs4 import BeautifulSoup
from twocaptcha import TwoCaptcha
import os


class Account(MailGW, TwoCaptcha):
    def __init__(self, username):
        MailGW.__init__(self, username)

        self.username = username

        TwoCaptcha.__init__(self, os.environ.get('2captcha_key'))

        self.site_key = '6LeTnxkTAAAAAN9QEuDZRpn90WwKk_R1TRW_g-JC'

        self.email = None
        self.csrf_token = None

        self.headers.update({
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36',
        })

    def enter_email(self):
        self.headers.update({
            'Authorization': ''
        })

        home_page = self.get('https://www.reddit.com/register/', timeout=5).content
        soup = BeautifulSoup(home_page, 'html.parser')

        self.csrf_token = soup.find('input', {
            'name': 'csrf_token'
        })['value']

        payload = {
            'csrf_token': self.csrf_token,
            'email': self.email
        }

        res = self.post('https://www.reddit.com/check_email', timeout=5, data=payload).status_code

        return res

    def enter_user_and_password(self):
        payload = {
            'csrf_token': self.csrf_token,
            'dest': 'https://www.reddit.com',
        }
