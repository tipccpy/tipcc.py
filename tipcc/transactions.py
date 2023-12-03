import requests
import json
import tipcc


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
        print(url)
        x = requests.get(
            url,
            headers={
                "accept": "application/json",
                "Authorization": f"Bearer {tipcc.get_token()}",
            },
        )
    if x.status_code not in [200, 404, 401]:
        return False, x.status_code
    if x.status_code == 404:
        return False, (json.loads(x.content))["error"]
    elif x.status_code == 401:
        return False, 401

    return True, json.loads(x.content)


def tip(recipient, value, currency):
    data = {
        "service": "discord",
        "recipient": str(recipient),
        "amount": {"value": str(value), "currency": str(currency)},
    }
    x = requests.post("https://api.tip.cc/api/v0/tips", data=data)

    if x.status_code not in [200, 404, 401]:
        return False, x.status_code
    if x.status_code == 404:
        return False, (json.loads(x.content))["error"]
    elif x.status_code_code == 401:
        return False, 401

    return True, json.loads(x.content)


def withdraw_fee(address, value, currency):
    data = {
        "address": str(address),
        "extra": "string",
        "amount": {"value": str(value), "currency": str(currency)},
    }
    x = requests.post(
        f"https://api.tip.cc/api/v0/account/wallets/{currency}/withdrawal", data=data
    )

    if x.status_code not in [200, 404, 401]:
        return False, "Error in tip.cc api server"
    if x.status_code == 404:
        return False, (json.loads(x.content))["error"]
    elif x.status_code_code == 401:
        return False, "401 Unauthorized"

    return True, json.loads(x.content)


def withdraw_confirm(id, currency):
    x = requests.post(
        f"https://api.tip.cc/api/v0/account/wallets/{currency}/withdrawal/{id}"
    )
