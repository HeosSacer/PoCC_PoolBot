import requests
import traceback
import json
from src.utils import Messages
from src.utils.Pools import Pool

class Message:
    def __init__(self):
        self.content = None
        self.error = None
        self.traceback = None


def price(message):
    if len(message) == len("!price"):
        coinName = "burst"
    else:
        coinName = message.lower().split(" ")[1]
    Msg = Message()
    if coinName == "btc":
        coinName = "bitcoin"
    try:
        USDStats = _getCoinPriceInUSD(coinName)
        EURStats = _getCoinPriceInEUR(coinName)
        Msg.content = Messages.getPriceEmbed(coinName, USDStats, EURStats)
    except Exception as Error:
        Msg.content = "Coin with name ***%s*** does not exist or is not listed!" % coinName.upper()
        Msg.error = Error
        Msg.traceback = traceback.format_exc()
    return Msg


def _getCoinPriceInUSD(coinName):
    coinmarketUrlUSD = "https://api.coinmarketcap.com/v1/ticker/{}/?convert=USD".format(coinName)
    responseUSD = requests.get(coinmarketUrlUSD, timeout= 2)
    responseUSD = json.loads(responseUSD.text)[0]
    return responseUSD


def _getCoinPriceInEUR(coinName):
    coinmarketUrlEUR = "https://api.coinmarketcap.com/v1/ticker/{}/?convert=EUR".format(coinName)
    responseEUR = requests.get(coinmarketUrlEUR, timeout=2)
    responseEUR = json.loads(responseEUR.text)[0]
    return responseEUR


def pool(message, BotHandle):
    poolUrls = BotHandle.config.poolUrlDictByPoolName
    statsDict = {}
    Msg = Message()
    Msg.content = []
    try:
        for poolName in poolUrls.keys():
            stats = Pool.getPoolStats(poolUrls[poolName])
            embed = Messages.getPoolEmbed(stats, poolUrls[poolName])
            Msg.content.append(embed)
    except Exception as Error:
        Msg.content = "Pools does not support PoCC-Pool Communication API!"
        Msg.error = Error
        Msg.traceback = traceback.format_exc()
    return Msg
