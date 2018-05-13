import asyncio
import traceback
import datetime
from src.utils.WebWalletRequests import WebWalletRequests as WWRequests
from src.utils import Messages
from src.utils import Users

async def Loop(BotHandle):
    """A Loop, where the bot updates block mining status and processes subscribers"""
    await BotHandle.wait_until_ready()

    loop = asyncio.get_event_loop()
    oldHeight = None

    channelHandleList = getConfiguredChannelsHandle(BotHandle)
    if BotHandle.config.subscriptionFeature:
        UsersDb = Users.connectToDB()

    # Loop retrieving block winner
    if BotHandle.config.subscriptionFeature or BotHandle.config.blockWinBroadcastFeature:
        while not BotHandle.is_closed:
            try:
                Winner, blockHeight = await getBlockWinner(oldHeight)
                if Winner is not None:
                    oldHeight = blockHeight
                    if not BotHandle.config.displayOurPoolBlockWinsOnly or Winner.rewardRecipientName in BotHandle.config.poolNameList:
                        winnerEmbed = Messages.getWinnerEmbed(Winner, BotHandle, blockHeight)
                        if BotHandle.config.blockWinBroadcastFeature:
                            await broadcastPoolWinner(BotHandle, channelHandleList, winnerEmbed)
                        if BotHandle.config.subscriptionFeature:
                            await processSubscribers(Winner, UsersDb, BotHandle, winnerEmbed)
            except Exception as Error:
                BotHandle.logger.error("Error in LoopProcess: {0} \n {1}".format(Error, traceback.format_exc()))
            await asyncio.sleep(BotHandle.config.requestPeriodInSeconds)


def getConfiguredChannelsHandle(Bot):
    channels = Bot.get_all_channels()
    channelHandleList = []
    for channel in channels:
        for channelNameInConfig in Bot.config.channelNameList:
            if channel.name == channelNameInConfig:
                channelHandleList.append(channel)
    return channelHandleList


async def getBlockWinner(oldHeight):
    newHeight = WWRequests.getLastMinedBlock()
    if newHeight != oldHeight:
        minerId, blockId = WWRequests.getSpecificBlockByHeight(newHeight)
        if minerId:
            return WWRequests(minerId), newHeight
    else:
        return None, oldHeight


async def broadcastPoolWinner(BotHandle, channels, winnerEmbed):
    if not winnerEmbed:
        return
    for channel in channels:
        await BotHandle.send_message(channel, embed=winnerEmbed)


async def processSubscribers(Winner, UsersDb, BotHandle, winnerEmbed):
    UsersList = Users.getUsersList(UsersDb)
    for User in UsersList:
        if User.burstName == Winner.burstName:
            User.lastWonBlock = winnerEmbed
            User.lastWonBlockTime = datetime.datetime.utcnow()
            await BotHandle.send_message(User.discordId, winnerEmbed)
        transactionsList = WWRequests.getAccountTransactions(User.burstId, numberOfTransactions=3)
        if transactionsList:
            for transaction in transactionsList:
                if transaction["timestamp"] is not User.lastPayoutTime:
                    if transaction['sender'] == User.rewardRecipientNumericalId:
                        User.lastPayout = transaction["amount"]
                        User.lastPayoutTime = transaction["timestamp"]
                        payoutEmbed = Messages.getPayoutEmbed(User,BotHandle)
                        BotHandle.send_message(User.discordId, embed=payoutEmbed)
                        break
                else:
                    break
        User.balance = WWRequests.getAccountBalance(User.burstId)
    UsersDb.session.commit()
