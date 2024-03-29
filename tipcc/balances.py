import requests
import json
import tipcc


def get_balances(currency=None):
    if not currency:
        url = "https://api.tip.cc/api/v0/account/wallets"
    else:
        url = "https://api.tip.cc/api/v0/account/wallets/" + currency

    x = requests.get(
        url,
        headers={
            "accept": "application/json",
            "Authorization": f"Bearer {tipcc.get_token()}",
        },
    )
    if x.status_code != 200:
        return False, x.status_code
    return True, x.content


def get_transaction(id, simple=True, custom=[]):
    x = requests.get(
        f"https://api.tip.cc/api/v0/account/transactions/{id}",
        headers={
            "accept": "application/json",
            "Authorization": f"Bearer {tipcc.get_token()}",
        },
    )
    if x.status_code != 200:
        return False, x.status_code

    data = json.loads(x.content())
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
        x = requests.get(
            f"https://api.tip.cc/api/v0/account/transactions/{id}",
            headers={
                "accept": "application/json",
                "Authorization": f"Bearer {tipcc.get_token()}",
            },
        )
    else:
        url = f"https://api.tip.cc/api/v0/account/transactions?since={since}&until={until}&offset={offset}&limit={limit}"
        for i in range(len(types)):
            url += "&types=" + types[i]
        url += f"&sort={sort}"
        if currency != None:
            url += "&currency=" + currency
        x = requests.get(
            url,
            headers={
                "accept": "application/json",
                "Authorization": f"Bearer {tipcc.get_token()}",
            },
        )
    if x.status_code not in [200]:
        return False, (json.loads(x.content))["error"]

    return True, json.loads(x.content)


def tip(
    recipient, value, currency
):  # does not work for whatever reason... 415 error (wrong media type)

    data = {
        "service": "discord",
        "recipient": str(recipient),
        "amount": {"value": str(value), "currency": str(currency)},
    }
    x = requests.post(
        "https://api.tip.cc/api/v0/tips",
        json=data,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {tipcc.get_token()}",
        },
    )

    if x.status_code not in [200]:
        return False, (json.loads(x.content))["error"], x.status_code

    return True, json.loads(x.content)
