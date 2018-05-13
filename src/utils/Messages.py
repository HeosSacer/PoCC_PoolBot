import discord
import datetime


def getHelpEmbed():
    embed = discord.Embed(
        title="Bot Commands",
        url="https://github.com/HeosSacer/PoolBot",
        color=16777215,
        timestamp=datetime.datetime.now())
    embed.add_field(name="!status", value="shows some stats of the bot.", inline=False)
    embed.add_field(name="!pool [*pool_name*]", value=" shows some stats specified or all pools.", inline=False)
    embed.add_field(name="!miner [*miner_identifier*]** - ", value=" shows some interesting information about specified miner.", inline=False)
    embed.add_field(name="!subscribe [*payouts/blocks-by-us/blocks-by-me*] [*account-id*]**", value="sends private messages to your account")
    embed.add_field(name="!unsubscribe [*all/payouts/blocks-by-us/blocks-by-me*] [*account-id*]", value="stops subscription of service")
    return embed


def getPriceEmbed(coinName, coinStatDictInUSD, coinStatDictInEUR):
    embed = discord.Embed(
        title="{} Market Information".format(coinName).upper(),
        url="https://coinmarketcap.com/currencies/{}/".format(coinName.lower()),
        color=16777215)
    embed.add_field(name="Bitcoin Value", value="{} BTC".format(coinStatDictInUSD["price_btc"]))
    embed.add_field(name="Euro Value", value="{:.4f} €".format(float(coinStatDictInEUR["price_eur"])))
    embed.add_field(name="US-Dollar Value", value="{:.4f} $".format(float(coinStatDictInUSD["price_usd"])))
    embed.add_field(name="Currency Rank", value="{:.4f}".format(float(coinStatDictInEUR["rank"])))
    embed.add_field(name="Market Cap €", value="{:,} €".format(float(coinStatDictInEUR["market_cap_eur"])))
    embed.add_field(name="Market Cap $", value="{:,} $".format(float(coinStatDictInUSD["market_cap_usd"])))
    embed.add_field(name="1hr Change", value="{0:+.2f}%".format(float(coinStatDictInUSD["percent_change_1h"])))
    embed.add_field(name="24hr Change", value="{0:+.2f}%".format(float(coinStatDictInUSD["percent_change_24h"])))
    embed.add_field(name="7d Change", value="{0:+.2f}%".format(float(coinStatDictInUSD["percent_change_7d"])))
    return embed


def getSubscriptionEmbed():
    raise NotImplementedError


def getBlockEmbed():
    raise NotImplementedError


def getWinnerEmbed(Winner, Bot, blockHeight):
    winnerURI = "[%s](https://explore.burst.cryptoguru.org/account/%s)" % (Winner.burstName, Winner.burstNumericId)
    msgBody = ":trophy: " + winnerURI + " has won the block :trophy:\n\n"
    if Winner.rewardRecipientName and not (Winner.rewardRecipientName == Winner.burstName):
        msgBodyPool = "Pool: " + Winner.rewardRecipientName
    else:
        msgBodyPool = "Miner is mining solo! :scream:"
    embed = discord.Embed(
        title="NEW BLOCK WAS GENERATED",
        description= msgBody + msgBodyPool,
        url="https://explore.burst.cryptoguru.org/block/%s" % blockHeight,
        color=16777215)
    embed.set_footer(text="PoC-Bot")
    embed.set_author(
        name="PoC-Bot",
        url="https://explore.burst.cryptoguru.org/")
    if Winner.rewardRecipientName in Bot.config.poolNameList and Bot.config.poolIconUrlDictByPoolName != None:
        embed.set_thumbnail(url=Bot.config.poolIconUrlDictByPoolName[Winner.rewardRecipientName])
    return embed


def getPayoutEmbed(User, Bot):
    payoutURI = "[%s](https://explore.burst.cryptoguru.org/account/%s)" % (User.burstName, User.burstNumericId)
    msgBody = payoutURI + " got payed {0} BURST".format(User.lastPayout)
    embed = discord.Embed(
        title="PAYOUT",
        description=msgBody,
        url="https://explore.burst.cryptoguru.org/account/%s" % User.burstNumericId,
        color=16777215,
        timestamp=datetime.datetime.now())
    embed.set_footer(text="PoC-Bot")
    embed.set_author(
        name="PoC-Bot",
        url="https://explore.burst.cryptoguru.org/",
        icon_url=Bot.config.botIconUrl)
    return embed


def getPoolEmbed(PoolStats, PoolUrl):
    embed = discord.Embed(
        title="{}".format(PoolUrl).upper(),
        color=16777215)
    embed.add_field(name="Miner Count", value="{}".format(PoolStats.minerCount))
    embed.add_field(name="Effective Pool Capacity", value="{:.3f} TB".format(float(PoolStats.effectivePoolCapacity)))
    embed.add_field(name="Network Difficulty", value="{:.3f}".format(float(PoolStats.netDiff)))
    return embed

def getNotificationEmbed():
    raise NotImplementedError
