import requests
import json


def init(token):
    global __TIPCCTOKEN__
    try:
        if __TIPCCTOKEN__ is None:
            if check_token(token) != True:
                print(
                    "Your tip.cc auth token is invalid! Make sure to fix this if you want access to the api."
                )
                return False
            else:
                __TIPCCTOKEN__ = token
                return True
        else:
            print(
                "Your tip.cc auth token is invalid! Make sure to fix this if you want access to the api."
            )
            return False
    except:
        if check_token(token) != True:
            print(
                "Your tip.cc auth token is invalid! Make sure to fix this if you want access to the api."
            )
            return False
        else:
            __TIPCCTOKEN__ = token
            return True


def get_token():
    return __TIPCCTOKEN__


def check_token(tipcc_token):
    x = requests.get(
        f"https://api.tip.cc/api/v0/user",
        headers={
            "accept": "application/json",
            "Authorization": f"Bearer {tipcc_token}",
        },
    )
    if x.status_code not in [200, 404, 401]:
        return False, x.status_code
    if x.status_code == 401:
        return False
    return True


def get_token_from_dms(discord_bot_token):
    try:
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bot " + discord_bot_token,
        }
        dm_response = requests.post(
            "https://discord.com/api/users/@me/channels",
            data='{"recipient_id":"350270174462607360"}',
            headers=headers,
        )
        dm = dm_response.json()
        dms_response = requests.get(
            "https://discord.com/api/channels/" + dm["id"] + "/messages",
            headers=headers,
        )
        messages = dms_response.json()
        key = [
            msg
            for msg in messages
            if msg["content"].startswith("eyJ")
            and msg["author"]["id"] == "350270174462607360"
        ][-1]
        if check_token(key["content"]) == True:
            return key["content"]
        else:
            return "Found key not valid", key["content"]
    except:
        return "No api key found"
