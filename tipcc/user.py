import requests

class User:
    def __init__(self, client) -> None:
        self.client = client

    def _make_api_request(self, url, method="GET", data=None):
        """
        Helper function to make API requests (GET, POST, PUT, DELETE).
        """
        try:
            if method == "GET":
                response = self.client.session.get(url)
            elif method == "POST":
                response = self.client.session.post(url, data=data)
            elif method == "PUT":
                response = self.client.session.put(url)
            elif method == "DELETE":
                response = self.client.session.delete(url)
            else:
                return False, "Invalid HTTP method"

            response.raise_for_status()  # Will raise an exception for 4xx/5xx responses
            return True, response.json()  # Return parsed JSON response
        except requests.exceptions.RequestException as e:
            return False, str(e)  # Return the error message if something goes wrong

    def get_depo_address(self, currency):
        url = f"https://api.tip.cc/api/v0/account/wallets/{currency}/addresses"
        success, data = self._make_api_request(url)
        if not success:
            return False, f"Error: {data}"
        return True, data

    def validate_destination(self, address, currency, extra=None):
        url = f"https://api.tip.cc/api/v0/account/wallets/{currency}/destination_info?address={address}&code={currency}"
        if extra:
            url += f"&extra={extra}"
        success, data = self._make_api_request(url)
        if not success:
            return False, f"Error: {data}"
        return True, data

    def get_withdraw_info(self, address, currency, value, extra=None, validate=True):
        if validate:
            success, message = self.validate_destination(address, currency, extra=extra)
            if not success:
                return False, message  # Invalid destination
        data = {
            "address": str(address),
            "amount": {
                "value": str(value),
                "currency": str(currency),
            },
        }
        if extra is not None:
            data.update({"extra": extra})

        url = f"https://api.tip.cc/api/v0/account/wallets/{currency}/withdrawal"
        success, data = self._make_api_request(url, method="POST", data=data)
        if not success:
            return False, f"Error: {data}"
        return True, data

    def get_withdraw_fees(self, address, currency, value, extra=None, validate=True):
        success, data = self.get_withdraw_info(address, currency, value, extra, validate)
        if success:
            return True, data.get("amount", {}).get("value", "No fee found")
        return success, data  # Return the error from get_withdraw_info

    def confirm_withdraw(self, currency, withdrawid):
        url = f"https://api.tip.cc/api/v0/account/wallets/{currency}/withdrawal/{withdrawid}"
        success, data = self._make_api_request(url, method="PUT")
        if not success:
            return False, f"Error: {data}"
        return True, data

    def cancel_withdraw(self, currency, withdrawid):
        url = f"https://api.tip.cc/api/v0/account/wallets/{currency}/withdrawal/{withdrawid}"
        success, data = self._make_api_request(url, method="DELETE")
        if not success:
            return False, f"Error: {data}"
        return True, data
