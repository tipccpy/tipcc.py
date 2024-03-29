# ALL FUNCTIONS ARE USER-ONLY; BOTS CANNOT USE

import requests

class User:
    def __init__(self, client) -> None:
        self.client = client

    def get_depo_address(self, currency):
        x = self.client.session.get(f"https://api.tip.cc/api/v0/account/wallets/{currency}/addresses")
        if x.status_code != 200:
            return False, x.status_code
        return True, x.content


    def validate_destination(self, address, currency, extra=None):
        url = f"https://api.tip.cc/api/v0/account/wallets/{currency}/destination_info?address={address}&code={currency}"
        url += f"&extra={extra}" if extra else ""
        x = self.client.session.get(url)
        if x.status_code != 200:
            return False, x.status_code
        return True, x.content


    def get_withdraw_info(self, address, currency, value, extra=None, validate=True):
        if validate:
            if self.validate_destination(address, currency, extra=extra)[0] == False:
                return False, "Invalid destination"
        data = {
            "address": str(address),
            "amount": {
                "value": str(value),
                "currency": str(currency),
            },
        }
        if extra != None:
            data.update({"extra": extra})

        x = self.client.session.get(f"https://api.tip.cc/api/v0/account/wallets/{currency}/withdrawal", data=data)
        if x.status_code != 200:
            return False, x.status_code
        return True, x.content


    def get_withdraw_fees(self, address, currency, value, extra=None, validate=True):
        response = self.get_withdraw_info(address, currency, value, extra=None, validate=True)
        if response[0]:
            return True, response[1]["amount"]["value"]
        return response


    def confirm_withdraw(self, currency, withdrawid):
        x = self.client.session.put(f"https://api.tip.cc/api/v0/account/wallets/{currency}/withdrawal/{withdrawid}")
        if x.status_code != 200:
            return False, x.status_code
        return True, x.content


    def cancel_withdraw(self, currency, withdrawid):
        x = self.client.session.delete(f"https://api.tip.cc/api/v0/account/wallets/{currency}/withdrawal/{withdrawid}")
        if x.status_code != 200:
            return False, x.status_code
        return True, x.content
