import requests
import json

class CurrenciesManager:
    def __init__(self, token) -> None:
        self.token = token

    def _fetch_data(self, url):
        """Helper function to fetch and return JSON data from the API."""
        try:
            response = requests.get(url)
            response.raise_for_status()
            return True, response.json()
        except requests.exceptions.RequestException as e:
            return False, str(e)
        except json.JSONDecodeError:
            return False, "Invalid JSON response"

    def get_currencies(self, savefile=False):
        success, data = self._fetch_data("https://api.tip.cc/api/v0/currencies/cryptocurrencies")
        if not success:
            return False, data

        if savefile:
            with open(savefile, "w") as f:
                json.dump(data, f, indent=4)

        return True, data

    def get_fiats(self, savefile=False):
        success, data = self._fetch_data("https://api.tip.cc/api/v0/currencies/fiats")
        if not success:
            return False, data

        if savefile:
            with open(savefile, "w") as f:
                json.dump(data, f, indent=4)

        return True, data

    def get_all(self, savefile=False):
        all_data = {}

        success_fiat, fiats = self._fetch_data("https://api.tip.cc/api/v0/currencies/fiats")
        if not success_fiat:
            return False, fiats
        all_data.update(fiats)

        success_crypto, cryptos = self._fetch_data("https://api.tip.cc/api/v0/currencies/cryptocurrencies")
        if not success_crypto:
            return False, cryptos
        all_data.update(cryptos)

        if savefile:
            with open(savefile, "w") as f:
                json.dump(all_data, f, indent=4)

        return True, all_data

    def get_rates(self, savefile=False, hideNull=False):
        success, data = self._fetch_data("https://api.tip.cc/api/v0/currencies/rates")
        if not success:
            return False, data

        rates = data.get("rates", [])
        if hideNull:
            rates = [rate for rate in rates if rate.get("usd_value") is not None]

        if savefile:
            with open(savefile, "w") as f:
                json.dump({"rates": rates}, f, indent=4)

        return True, {"rates": rates}

    def get_price(self, currency, file=None):
        """Fetches the price of a given currency in USD."""
        currency = currency.lower()

        if file:
            try:
                with open(file) as f:
                    data = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                return False, "Invalid or missing price file"
        else:
            success, data = self._fetch_data("https://api.tip.cc/api/v0/currencies/rates")
            if not success:
                return False, data

        for rate in data.get("rates", []):
            if rate.get("code", "").lower() == currency:
                usd_value = rate.get("usd_value")
                return True, None if usd_value is None else float(usd_value["value"]) / 10000

        return False, "Currency not found"

    def conversions(self):
        """Returns a dictionary of currency conversion factors."""
        success, data = self.get_currencies()
        if not success:
            return False

        conversions = {}

        for currency in data.get("cryptocurrencies", []):
            for unit in currency.get("format", {}).get("units", []):
                if unit["singular"] != currency["code"]:
                    scale_diff = abs(unit["scale"] - currency["format"]["scale"])
                    conversions[unit["singular"]] = {
                        "parent": currency["code"],
                        "conversion": 1 / (10 ** scale_diff)
                    }

        return conversions

    def convert_factors(self, factor, value):
        """Converts a sub-unit (e.g., satoshi) into its parent currency (e.g., BTC)."""
        conversions = self.conversions()
        if not conversions:
            return False

        if factor not in conversions:
            return False

        return True, conversions[factor]["parent"], conversions[factor]["conversion"] * float(value)
