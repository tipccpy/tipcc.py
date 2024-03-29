import json

class BalancesManager:
    def __init__(self, client) -> None:
        self.client = client

    def get_balances(self, currency=None):
        if not currency:
            url = "https://api.tip.cc/api/v0/account/wallets"
        else:
            url = "https://api.tip.cc/api/v0/account/wallets/" + currency

        x = self.client.session.get(url)
        if x.status_code != 200:
            return False, x.status_code
        return True, x.content


    def get_transaction(self, id, simple=True, custom=[]):
        x = self.client.session.get(f"https://api.tip.cc/api/v0/account/transactions/{id}")
        if x.status_code != 200:
            return False, x.status_code

        data = json.loads(x.content)
        if not simple:
            return True, data
        x = {}
        if simple:
            x.update({"id": data["transaction"]["id"]})
            x.update({"type": data["transaction"]["type"]})
            x.update({"amount": data["transaction"]["amount"]})
            x.update({"usd_value": data["transaction"]["usd_value"]})
            x.update({"sender": data["transaction"]["sender"]})
            x.update({"recipient": data["transaction"]["recipient"]})
        for i in custom:
            try:
                x.update({i: data["transaction"][i]})
            except:
                return False, f"{i} not found in json response"
        return True, x


    def get_transactions(
        self,
        id=None,
        since="2001-01-01T00%3A00%3A00%2B00%3A00",
        until="3001-01-01T00%3A00%3A00%2B00%3A00",
        offset=0,
        limit=100,
        types=("tip", "deposit", "withdrawal"),
        sort="desc",
        currency=None,
    ):
        if id != None:
            x = self.client.session.get(f"https://api.tip.cc/api/v0/account/transactions/{id}")
        else:
            url = f"https://api.tip.cc/api/v0/account/transactions?since={since}&until={until}&offset={offset}&limit={limit}"
            for i in range(len(types)):
                url += "&types=" + types[i]
            url += f"&sort={sort}"
            if currency != None:
                url += "&currency=" + currency
            x = self.client.session.get(url)
        if x.status_code not in [200]:
            return False, (json.loads(x.content))["error"]

        return True, json.loads(x.content)


    def tip(
        self, recipient, value, currency
    ):
        data = {
            "service": "discord",
            "recipient": str(recipient),
            "amount": {"value": str(value), "currency": str(currency)},
        }
        x = self.client.session.post(
            "https://api.tip.cc/api/v0/tips",
            json=data
        )

        if x.status_code not in [200]:
            return False, (json.loads(x.content))["error"], x.status_code

        return True, json.loads(x.content)
