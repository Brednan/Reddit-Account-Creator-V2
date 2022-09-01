from account import Account
import requests


class AccountCreator:
    @staticmethod
    def generate_username():
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36'
        }

        res = requests.get('https://www.reddit.com/api/v1/generate_username.json', timeout=5, headers=headers).json()

        username = res['usernames'][0]
        print(username)
