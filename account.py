from mail_gw_api_wrapper import MailGW
from bs4 import BeautifulSoup
from twocaptcha import TwoCaptcha
import os
import json
from urllib.parse import urlparse, parse_qs


class Account(MailGW):
    def __init__(self, username):
        MailGW.__init__(self, username)

        self.proxies = {
            'http': f'http://{os.environ.get("ip_royal_username")}:{os.environ.get("ip_royal_password")}_country-us@geo.iproyal.com:22323',
            'https': f'http://{os.environ.get("ip_royal_username")}:{os.environ.get("ip_royal_password")}_country-us@geo.iproyal.com:22323'
        }

        self.two_captcha = TwoCaptcha(os.environ.get('2captcha_key'))

        self.site_key = '6LeTnxkTAAAAAN9QEuDZRpn90WwKk_R1TRW_g-JC'

        self.email = None
        self.csrf_token = None

        self.access_token = None

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

    def submit_register_req(self):
        g_recaptcha_response = self.two_captcha.recaptcha(sitekey='6LeTnxkTAAAAAN9QEuDZRpn90WwKk_R1TRW_g-JC', url='https://www.reddit.com/register')

        payload = {
            'csrf_token': self.csrf_token,
            'g-recaptcha-response': g_recaptcha_response['code'],
            'password': self.password,
            'dest': 'https://www.reddit.com',
            'email_permission': False,
            'lang': 'en',
            'username': self.username,
            'email': self.email
        }

        res = self.post('https://www.reddit.com/register', timeout=5, data=payload)

        if res.status_code == 200:
            if self.req_email() == 1:

                return 1

            else:
                return 0

        else:
            return 0

    def req_email(self):
        home_page = self.get('https://www.reddit.com/', timeout=5).content

        soup = BeautifulSoup(home_page, 'html.parser')

        script = soup.find('script', {'id': 'data'}).text

        script_json_raw = script[14: len(script) - 1]

        script_json = json.loads(script_json_raw)

        self.access_token = script_json['user']['session']['accessToken']

        self.headers.update({
            'Authorization': f'Bearer {self.access_token}'
        })

        email_verify = self.get(
            'https://oauth.reddit.com/api/send_verification_email?source=tooltip&raw_json=1&gilding_detail=1',
            timeout=5).json()

        if email_verify['success']:
            return 1

        else:
            return 0

    def verify_email(self, link):
        form_data = {
            'id': '#verify-email',
            'renderstyle': 'html'
        }

        self.headers.update({
            'Authorization': ''
        })

        verification_url = self.get_verification_url(link)

        res = self.post(verification_url, timeout=5, data=form_data).json()

        if res['success']:
            return 1

    @staticmethod
    def get_verification_url(url):
        url_parsed = urlparse(url)

        queries = parse_qs(url_parsed.query)

        param = url[36: url.find('?', 23)]

        correlation_id = queries['correlation_id'][0]
        ref_campaign = queries['ref_campaign'][0]

        verify_url = f'https://www.reddit.com/api/v1/verify_email/{param}.json?correlation_id={correlation_id}&ref_campaign={ref_campaign}'

        return verify_url
