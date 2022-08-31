from account import Account


account = Account(('tester434_', ))
account.set_domain()

if account.create_email() == 1:
    account.set_token()
