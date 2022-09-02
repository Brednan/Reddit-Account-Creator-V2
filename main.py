from account_creator import AccountCreator


if __name__ == '__main__':
    amount = int(input('Insert the amount of accounts you want to create: '))

    account_creator = AccountCreator(amount)

    account_creator.create_accounts()
