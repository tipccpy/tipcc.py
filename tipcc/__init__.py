from .client import TipccClient
from .balances import BalancesManager
from .currencies import CurrenciesManager
from .info import InfoManager
from .user import User


# stuff to work on:
# tipping does not work for whatever reason even though i followed everything docs said.... 415 error (wrong media type)
# some requests are very peciliar about how the currency is specified "Bitcoin", "bitcoin", "btc", "sat" - need to make it convert it
# write some docs
