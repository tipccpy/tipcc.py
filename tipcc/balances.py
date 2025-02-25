import json

class BalancesManager:
    def __init__(self, client) -> None:
        self.client = client

    def get_balances(self, currency=None):
        url = f"https://api.tip.cc/api/v0/account/wallets{('/' + currency) if currency else ''}"
        response = self.client.session.get(url)
        
        if response.status_code != 200:
            return False, response.status_code
        
        try:
            return True, response.json()
        except json.JSONDecodeError:
            return False, "Invalid JSON response"

    def get_transaction(self, transaction_id, simple=True, custom_fields=None):
        if custom_fields is None:
            custom_fields = []
        
        response = self.client.session.get(f"https://api.tip.cc/api/v0/account/transactions/{transaction_id}")
        if response.status_code != 200:
            return False, response.status_code

        try:
            data = response.json()
        except json.JSONDecodeError:
            return False, "Invalid JSON response"
        
        if not simple:
            return True, data

        transaction_data = {
            "id": data["transaction"].get("id"),
            "type": data["transaction"].get("type"),
            "amount": data["transaction"].get("amount"),
            "usd_value": data["transaction"].get("usd_value"),
            "sender": data["transaction"].get("sender"),
            "recipient": data["transaction"].get("recipient"),
        }

        for field in custom_fields:
            if field in data["transaction"]:
                transaction_data[field] = data["transaction"][field]
            else:
                return False, f"{field} not found in JSON response"
        
        return True, transaction_data

    def get_transactions(self, transaction_id=None, since="2001-01-01T00%3A00%3A00%2B00%3A00", 
                         until="3001-01-01T00%3A00%3A00%2B00%3A00", offset=0, limit=100, 
                         types=("tip", "deposit", "withdrawal"), sort="desc", currency=None):
        
        if transaction_id:
            response = self.client.session.get(f"https://api.tip.cc/api/v0/account/transactions/{transaction_id}")
        else:
            url = (f"https://api.tip.cc/api/v0/account/transactions?since={since}&until={until}" 
                   f"&offset={offset}&limit={limit}&sort={sort}")
            url += ''.join([f"&types={t}" for t in types])
            if currency:
                url += f"&currency={currency}"
            
            response = self.client.session.get(url)

        if response.status_code != 200:
            try:
                error_message = response.json().get("error", "Unknown error")
            except json.JSONDecodeError:
                error_message = "Invalid JSON response"
            return False, error_message
        
        try:
            return True, response.json()
        except json.JSONDecodeError:
            return False, "Invalid JSON response"

    def tip(self, recipient, value, currency):
        data = {
            "service": "discord",
            "recipient": str(recipient),
            "amount": {"value": str(value), "currency": str(currency)},
        }
        response = self.client.session.post("https://api.tip.cc/api/v0/tips", json=data)

        if response.status_code != 200:
            try:
                error_message = response.json().get("error", "Unknown error")
            except json.JSONDecodeError:
                error_message = "Invalid JSON response"
            return False, error_message, response.status_code
        
        try:
            return True, response.json()
        except json.JSONDecodeError:
            return False, "Invalid JSON response"
