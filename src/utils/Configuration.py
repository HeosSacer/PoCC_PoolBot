from os import path
import configparser
from autocorrect import spell as spellcheck

class Config:
    def __init__(self):
        self.configFileName = "config.ini"
        self.ConfigFile = self.readConfigFile()
        self.readContents()

    def readConfigFile(self):
        basePath = path.dirname(__file__)
        configFilePath = path.abspath(path.join(basePath, "..", "..")) + '/' + self.configFileName
        print(configFilePath)
        ConfigFile = configparser.ConfigParser()
        ConfigFile.read(configFilePath)
        return ConfigFile

    def readContents(self):
        self.getBotConfig()
        self.getFeatures()
        self.getDiscordConfig()
        self.getPoolInfo()

    def getBotConfig(self):
        self.webWalletAddressList = self.ConfigFile['Bot']['WebWallets'].split(',')
        self.requestPeriodInSeconds = float(self.ConfigFile['Bot']['RequestPeriodInSeconds'])
        self.botIconUrl = self.ConfigFile['Bot']['BotIconUrl']
        self.displayOurPoolBlockWinsOnly = self.parseBoolean(self.ConfigFile['Bot']['DisplayOurPoolBlockWinsOnly'])

    def getFeatures(self):
        self.subscriptionFeature = self.ConfigFile['Features']['Subscription']
        self.blockWinBroadcastFeature = self.ConfigFile['Features']['BlockWinBroadcast']

    def getDiscordConfig(self):
        self.channelNameList = self.ConfigFile['Discord']['ChannelNames'].split(',')
        self.discordToken = self.ConfigFile['Discord']['DiscordToken']

    def getPoolInfo(self):
        self.poolNameList = self.ConfigFile['Pool']['PoolNames'].split(',')
        self.poolUrlList = self.ConfigFile['Pool']['PoolUrl'].split(',')
        if len(self.poolUrlList) != len(self.poolNameList):
            raise ValueError("Each specified Pool in PoolUrl needs an name in PoolNames.")
        self.poolIconUrlList = self.ConfigFile['Pool']['PoolIconUrl'].split(',')
        self.poolDefaultPictureUrl = self.ConfigFile['Pool']['DefaultPoolIconUrl']
        if len(self.poolNameList) == len(self.poolUrlList):
            self.poolUrlDictByPoolName = {key: value for key, value in zip(self.poolNameList, self.poolUrlList)}
        else:
            self.poolUrlDictByPoolName = {key: value for key, value in zip(self.poolNameList, self.poolNameList)}
        if len(self.poolNameList) == len(self.poolIconUrlList):
            self.poolIconUrlDictByPoolName = {key: value for key, value in zip(self.poolNameList, self.poolIconUrlList)}
        elif self.poolIconUrlList == [""]:
            self.poolIconUrlDictByPoolName = None


    def parseBoolean(self, booleanFromConfig):
        stringWithBoolean = spellcheck(booleanFromConfig) if len(booleanFromConfig) > 1 else booleanFromConfig
        if stringWithBoolean.lower() in ['true', 'yes', '1', 'y']:
            return True
        elif stringWithBoolean.lower() in ['false', 'no', '0', 'n']:
            return False
        else:
            raise ValueError('Please use an appropriate boolean value in the config like YES or NO')
