from requests import Session
from bs4 import BeautifulSoup


class Account(Session):
    def __init__(self):
        Session.__init__(self)

        self.headers.update({
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36',
        })

    def get_email_address(self):
        page = self.get('https://tempmailo.com/', timeout=5)
        soup = BeautifulSoup(page.content, 'html.parser')

        print(soup)
