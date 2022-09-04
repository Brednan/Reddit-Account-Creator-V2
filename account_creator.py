from account import Account
import requests


class AccountCreator:
    def __init__(self, amount):
        self.amount = amount

    @staticmethod
    def generate_username():
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36'
        }

        res = requests.get('https://www.reddit.com/api/v1/generate_username.json', timeout=5, headers=headers).json()

        username = res['usernames'][0]

        return username

    def create_accounts(self):
        i = 0

        while i < self.amount:
            self.create_account(i)

            i += 1

    def create_account(self, i: int):
        try:
            account = Account(self.generate_username().lower())

            account.set_domain()

            if account.create_email() == 1:
                account.set_token()

                if account.enter_email() == 200:
                    register_status = account.submit_register_req()

                    if register_status == 1:
                        account.headers.update({
                            'Authorization': f'Bearer {account.email_token}'
                        })

                        msg_id = account.get_message_id(0)

                        message = account.get_message(msg_id)

                        link_beginning_index = message.find('https://www.reddit.com/verification')

                        link_ending_index = message.find(']', link_beginning_index)

                        verify_link = message[link_beginning_index: link_ending_index]

                        success = account.verify_email(verify_link)

                        if success == 1:
                            print(f'Account {i + 1}: Success!')

                            self.save_account(account.username, account.password)

                        else:
                            print(f'Account {i + 1}: Failed!')

                    else:
                        print(f'Account {i + 1}: Failed!')

                else:
                    print(f'Account {i + 1}: Failed!')

            else:
                print(f'Account {i + 1}: Failed!')

        except requests.exceptions.ProxyError:
            print(f'Account {i + 1}: Failed!')

    @staticmethod
    def save_account(username, password):
        f = open('./output.txt', 'a', encoding='utf-8')
        f.write(f'{username}:{password}\n')
        f.close()
