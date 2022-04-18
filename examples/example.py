from src.wealthsimple import wealthsimple

AIR_CANADA_SECURITY_ID = 'sec-s-6e73535b8e474d8689064c4c9fee326a'
AIR_CANADA_TICKER = 'AC'


def get_login_credentials():
    """
    Prompts user for login credentials.
    """
    email = input("Email: ")
    password = input("Password: ")
    auth_secret_key = input("Auth Secret Key: ")
    return email, password, auth_secret_key


if __name__ == '__main__':
    ws_email, ws_password, ws_auth_secret_key = get_login_credentials()

    ws = wealthsimple.WS(ws_email, ws_password, ws_auth_secret_key)

    # Get accounts
    accounts = ws.get_accounts()
    print("Accounts: ", accounts)

    # Get account ids
    ids = ws.get_account_ids()
    print("ID's: ", ids)
    first_account_id = ids[0]

    # Get account
    account = ws.get_account(first_account_id)
    print("Account: ", account)

    # Get account history
    account_history = ws.get_account_history(first_account_id, '3m')
    print("Account History: ", account_history)

    # Get orders
    orders = ws.get_orders()
    print("Orders: ", orders)

    # Get Security from security id
    security = ws.get_security(AIR_CANADA_SECURITY_ID)
    print("Security from ID: ", security)

    # Get Security from ticker
    security = ws.get_security_from_ticker(AIR_CANADA_TICKER)
    print("Security from Ticker: ", security)

    # Get Positions
    positions = ws.get_positions(first_account_id)
    print("Positions: ", positions)

    # Get activity
    activity = ws.get_activities()
    print("Activity: ", activity)

    # Get Wealthsimple user object
    user = ws.get_me()
    print("User Object: ", user)

    # Get Wealthsimple person object
    person = ws.get_person()
    print("Person Object: ", person)

    # Get bank accounts associated with the user
    bank_accounts = ws.get_bank_accounts()
    print("Bank Accounts: ", bank_accounts)

    # Get past deposits
    past_deposits = ws.get_deposits()
    print("Past Deposits: ", past_deposits)

    # Get Forex exchange rates
    forex_rates = ws.get_forex()
    print("Forex Rates: ", forex_rates)

    # Refresh authentication token
    ws.refresh_token()
