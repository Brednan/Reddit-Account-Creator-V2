from requests import Session
from bs4 import BeautifulSoup
from selenium.webdriver import Firefox, FirefoxProfile


class Account(Session):
    def __init__(self):
        Session.__init__(self)

        self.email = None

        self.headers.update({
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36',
        })

    def get_email_address(self):
        page = self.get_home_page()
        soup = BeautifulSoup(page, 'html.parser')

        request_verification_token = soup.find('input', {'name': '__RequestVerificationToken'})['value']

        if not request_verification_token:
            return None

        self.headers.update({
            'requestverificationtoken': f'{request_verification_token}'
        })

        email = soup.find('input', {'id': 'i-email'})

        self.email = email

    def get_email_inbox(self):
        url = 'https://tempmailo.com/'

        payload = {
            'mail': self.email
        }

        inbox = self.post(url, data=payload, timeout=5)

    def get_home_page(self):
        firefox_profile = FirefoxProfile()
        firefox_profile.set_preference('general.useragent.override', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36')

        driver = Firefox(firefox_profile=firefox_profile)

        driver.get('https://tempmailo.com')

        page_source = driver.page_source

        cookies = driver.get_cookies()

        for cookie in cookies:
            self.cookies.set(cookie['name'], cookie['value'])

        return page_source
