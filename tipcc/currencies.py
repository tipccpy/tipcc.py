import requests
import json


def get_currencies(savefile=False):
    x = requests.get(f"https://api.tip.cc/api/v0/currencies/cryptocurrencies")
    if x.status_code != 200:
        return False, x.status_code

    if not savefile:
        return True, json.loads(x.content)
    with open(savefile, "w") as f:
        f.write(json.dumps(x.content, indent=4))
    return True, json.loads(x.content)


def get_fiats(savefile=False):
    x = requests.get(f"https://api.tip.cc/api/v0/currencies/fiats")
    if x.status_code != 200:
        return False, x.status_code

    if not savefile:
        return True, json.loads(x.content)
    with open(savefile, "w") as f:
        f.write(json.dumps(x.content, indent=4))
    return True, json.loads(x.content)


def get_all(savefile=False):
    x = {}
    fiats = requests.get(f"https://api.tip.cc/api/v0/currencies/fiats")
    if fiats.status_code != 200:
        return False, fiats.status_code

    x.update(json.loads(fiats.content))

    cryptos = requests.get(f"https://api.tip.cc/api/v0/currencies/cryptocurrencies")
    if cryptos.status_code != 200:
        return False, cryptos.status_code

    x.update(json.loads(cryptos.content))

    if not savefile:
        return True, x
    with open(savefile, "w") as f:
        f.write(json.dumps(x, indent=4))
    return True, x


def get_rates(savefile=False, hideNull=False):
    x = requests.get(f"https://api.tip.cc/api/v0/currencies/rates")
    if x.status_code != 200:
        return False, x.status_code

    if not hideNull:
        if not savefile:
            return True, json.loads(x.content)
        with open(savefile, "w") as f:
            f.write(json.dumps(json.loads(x.content), indent=4))
        return True, json.loads(x.content)
    y = []
    for i in json.loads(x.content)["rates"]:
        if i["usd_value"] != None:
            y.append(i)
    if not savefile:
        return True, json.loads({"rates": y})
    with open(savefile, "w") as f:
        f.write(json.dumps({"rates": y}, indent=4))
    return True, {"rates": y}


def get_price(token, file=None):
    # only does token FULL NAME rn... gotta have it accept abreviations
    token = token.lower()

    if file == None:
        for i in json.loads(
            requests.get("https://api.tip.cc/api/v0/currencies/rates").content
        )["rates"]:
            if i["code"].lower() == token:
                if str(i["usd_value"]) != "null":
                    return True, float(i["usd_value"]["value"]) / 10000
    else:
        with open(file) as f:
            x = json.loads(f.read())
        for i in x["rates"]:
            if i["code"].lower() == token:
                if str(i["usd_value"]) != "null":
                    return True, float(i["usd_value"]["value"]) / 10000
                else:
                    return True, None  # return none if no value

    return False


def conversions():
    # returns list of conversions of coins (btc/sat, eth/wei)
    x = get_currencies()

    if x[0] != True:
        return False

    x = x[1]["cryptocurrencies"]

    data = {}

    for i in x:
        for y in i["format"]["units"]:
            if y["singular"] != i["code"]:
                scale = 1
                for x in range(abs(y["scale"] - i["format"]["scale"])):
                    scale = scale * 10
                data.update(
                    {y["singular"]: {"parent": i["code"], "conversion": 1 / scale}}
                )

    return data


def convert_factors(factor, value):
    # returns the converted value of the factor into its parent currency

    data = conversions()

    if factor not in data:
        return False

    return True, data[factor]["parent"], data[factor]["conversion"] * float(value)
