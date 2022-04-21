import requests
import pyotp


class WS:
    """
    Wrapper for the Unofficial Wealthsimple API

    Attributes
    ----------
    baseURL : str
        Main URL endpoint for API
    session : session
        A requests Session object to be associated with the class
    """

    def __init__(self, email: str, password: str, auth_secret_key: str):
        """
        Initializes the requests Session object and logs in with provided credentials
        :param email: email for Wealthsimple login
        :param password: password for Wealthsimple login
        :param auth_secret_key: authenticator secret key for generating the two-factor authentication tokens
        """

        self.baseURL = "https://trade-service.wealthsimple.com/"
        self.session = requests.session()
        self.login(email, password, auth_secret_key)

    def login(self, email: str, password: str, auth_secret_key: str) -> None:
        """
        Login to Wealthsimple and add session header with access token for future requests
        :param email: email for Wealthsimple login
        :param password: password for Wealthsimple login
        :param auth_secret_key: authenticator secret key for generating the two-factor authentication tokens
        """

        if not (email and password and auth_secret_key):
            raise Exception("Missing login credentials")

        auth_token = pyotp.TOTP(auth_secret_key).now()
        req_body = {"email": email, "password": password, "otp": auth_token}
        res = self.session.post(self.baseURL + "auth/login", json=req_body)

        if res.status_code == 401:
            raise Exception("Invalid login credentials")

        self.session.headers.update({"Authorization": res.headers["X-Access-Token"]})

    def refresh_token(self) -> dict:
        """
        Refresh access token for future requests
        :return: response from the refresh token request
        """

        x_access_token = self.session.headers.get("Authorization")
        req_body = {"refresh_token": x_access_token}
        return self.session.post(self.baseURL + "auth/refresh", json=req_body).json()

    def get_accounts(self) -> list:
        """
        Get Wealthsimple accounts associated with login credentials
        :return: List of Wealthsimple account objects
        """

        res = self.session.get(self.baseURL + "account/list").json()
        return res["results"]

    def get_account_ids(self) -> list:
        """
        Get Wealthsimple account ids associated with login credentials
        :return: List of Wealthsimple account ids
        """

        user_accounts = self.get_accounts()
        return [account["id"] for account in user_accounts]

    def get_account(self, account_id: str) -> dict:
        """
        Get the Wealthsimple account associated with the given id
        :param account_id: The id of the account to fetch
        :return: Wealthsimple account object
        """

        user_accounts = self.get_accounts()
        for account in user_accounts:
            if account["id"] == account_id:
                return account
        raise NameError(f"{account_id} does not correspond to any account")

    def get_account_history(self, account_id: str, time: str = "all") -> dict:
        """
        Get the account history associated with the given account id
        :param account_id: The id of the account to fetch
        :param time: The time interval to return -> [1d, 1w, 1m, 3m, 1y, all]
        :return: Wealthsimple account history object associated with request
        """

        res = self.session.get(self.baseURL + "account/history/{}?account_id={}".format(time, account_id)).json()
        if "error" in res:
            if res["error"] == "Record not found":
                raise NameError(f"{account_id} does not correspond to any account")
        return res["results"]

    def get_orders(self, symbol: str = None) -> list:
        """
        Get Wealthsimple orders
        :param symbol: Security symbol to filter orders by
        :return: List of Wealthsimple order objects
        """

        res = self.session.get(self.baseURL + "orders").json()
        # Check if order must be filtered:
        if symbol:
            return [order for order in res["results"] if order["symbol"] == symbol]
        else:
            return res["results"]

    def place_fractional_share_order(self, security_id: str, account_id: str, purchase_value: float) -> dict:
        """
        Buy fractional shares for a given security
        Note: Purchasing fractional shares is only available for select securities
        :param security_id: The security id of the shares to be purchased
        :param account_id: The id of the account to buy the fractional shares with
        :param purchase_value: The dollar amount in the users local currency to be used to buy fractional shares
        :return: The response from the buy request
        """

        order_type = "buy_value"
        order_sub_type = "fractional"
        time_in_force = "day"
        req_body = {
            "security_id": security_id,
            "order_type": order_type,
            "order_sub_type": order_sub_type,
            "market_value": purchase_value,
            "time_in_force": time_in_force,
            "account_id": account_id
        }
        res = self.session.post(self.baseURL + "orders", json=req_body).json()
        return res

    def cancel_order(self, order_id: str) -> dict:
        """
        Cancel a pending order
        :param order_id: id of the order to be cancelled
        :return: Response from the cancel request
        """

        res = self.session.delete(self.baseURL + "orders/{}".format(order_id)).json()
        return res

    def get_security(self, security_id: str) -> dict:
        """
        Get information about a given security
        :param security_id: The id of the security to fetch
        :return: security information object
        """

        res = self.session.get(self.baseURL + "securities/{}".format(security_id)).json()
        return res

    def get_security_from_ticker(self, symbol: str) -> list:
        """
        Get information about a security given its ticker symbol
        :param symbol: The ticker symbol of security
        :return: security information object
        """

        res = self.session.get(self.baseURL + "securities?query={}".format(symbol)).json()
        return res["results"]

    def get_positions(self, account_id: str) -> list:
        """
        Get positions for a given account id
        :param account_id: The id of the account to fetch
        :return: list of positions
        """

        res = self.session.get(self.baseURL + "account/positions?account_id={}".format(account_id)).json()
        return res["results"]

    def get_activities(self, activity_type: str = None, limit: int = 20, account_id: list = []) -> list:
        """
        Get user activity
        :param activity_type: The type of activity to filter by -> [
        dividend, buy, sell, deposit, convert_funds, withdrawal, institutional_transfer, internal_transfer,
        subscription_payment, refund, referral_bonus, affiliate, asset_movement
        ]
        :param limit: The number of activities to return
        :param account_id: The id of the account to fetch, if not specified, activity for all accounts is returned
        :return: list of activity objects
        """

        if activity_type:
            res = self.session.get(self.baseURL + "account/activities?limit={}&account_id{}&type={}".format(
                limit, account_id, activity_type)).json()
        else:
            res = self.session.get(self.baseURL + "account/activities?limit={}&account_id{}".format(
                limit, account_id)).json()
        return res["results"]

    def get_me(self) -> dict:
        """
        Get Wealthsimple user object
        :return: user object
        """

        return self.session.get(self.baseURL + "me").json()

    def get_person(self) -> dict:
        """
        Get Wealthsimple person object
        :return: person object
        """

        return self.session.get(self.baseURL + "person").json()

    def get_bank_accounts(self) -> list:
        """
        Get bank accounts associated with Wealthsimple account
        :return: list of bank account objects
        """

        res = self.session.get(self.baseURL + "bank-accounts").json()
        return res["results"]

    def get_deposits(self) -> list:
        """
        Get list of deposits
        :return: list of deposit objects
        """

        res = self.session.get(self.baseURL + "deposits").json()
        return res["results"]

    def get_forex(self) -> dict:
        """
        Get currency exchange rates
        :return: exchange rates object
        """

        return self.session.get(self.baseURL + "forex").json()
