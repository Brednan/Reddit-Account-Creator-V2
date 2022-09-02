from requests import Session
import json


class MailGW(Session):
    def __init__(self, username):
        Session.__init__(self)

        self.username = username
        self.password = 'Password_1264'

        self.email = None
        self.email_token = None
        self.email_domain = None
        self.email_id = None

    def set_domain(self):
        res = self.get('https://api.mail.gw/domains?page=1', timeout=5).json()

        self.email_id = res['hydra:member'][0]['id']

        self.email_domain = f"{res['hydra:member'][0]['domain']}"

    def create_email(self):
        payload = {
            'address': f'{self.username}@{self.email_domain}',
            'password': self.password
        }

        res = self.post('https://api.mail.gw/accounts', timeout=5, json=payload)

        if 200 <= res.status_code <= 204:
            self.email = f'{self.username}@{self.email_domain}'
            return 1

        else:
            return 0

    def set_token(self):
        payload = {
            'address': self.email,
            'password': self.password
        }

        res = self.post('https://api.mail.gw/token', json=payload, timeout=5).json()

        self.email_token = res['token']

        self.headers.update({
            'Authorization': f"Bearer {self.email_token}"
        })

        self.email_id = res['id']

    def get_message_id(self, index):
        messages_req = self.get(f'https://api.mail.gw/messages?id={self.email_id}', timeout=5).json()

        msg_id = messages_req['hydra:member'][index]['id']

        return msg_id

    def get_message(self, msg_id):
        message_raw = self.get(f'https://api.mail.gw/messages/{msg_id}', timeout=5).json()

        message = message_raw['text']
        return message
