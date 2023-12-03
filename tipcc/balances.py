import requests
import json
import tipcc


def get_transaction(id, crap=False):
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
    if not crap:
        # get rid of the crap data
        x = {}
        x.update({"id": data["transaction"]["id"]})
        x.update({"type": data["transaction"]["type"]})
        x.update({"type": data["transaction"]["amount"]})
        x.update({"type": data["transaction"]["usd_value"]})
        x.update({"type": data["transaction"]["sender"]})
        x.update({"type": data["transaction"]["recipient"]})
        return True, x
    return True, data


def tip(recipient, value, currency):
    if recipient == None or value == None or currency == None:
        return False
    x = requests.post(
        f"https://api.tip.cc/api/v0/tips",
        headers={
            "accept": "application/json",
            "Authorization": f"Bearer {tipcc.get_token()}",
        },
        data={
            "service": "discord",
            "recipient": recipient,
            "amount": {"value": value, "currency": currency},
        },
    )
    if x.status_code != 200:
        return False, x.status_code

    return True


def get_deposit_address(currency):  # users only
    x = requests.get(
        f"https://api.tip.cc/api/v0/account/wallets/{currency}/addresses",
        headers={
            "accept": "application/json",
            "Authorization": f"Bearer {tipcc.get_token()}",
        },
    )
    if x.status_code != 200:
        return False, x.status_code, x.content

    return True, x.content
