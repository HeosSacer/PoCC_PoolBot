from unittest import TestCase
from src.utils import Status
from src.utils import Configuration
from src.utils import Messages
from src.utils import MessageProcessing as MP
from src.utils.WebWalletRequests import WebWalletRequests
from src.utils import Users
from src.utils import Pools
from autocorrect import spell as spellcheck


class TestBot(TestCase):
    def testSetupLogger(self):
        self.assertRaises(Exception, Status.setupLogger())

    def testConfiguration(self):
        self.assertRaises(Exception, Configuration.Config())
        config = Configuration.Config()
        self.assertEqual(type(config.webWalletAddressList), type([]))

    def testSpellCheck(self):
        self.assertEqual(spellcheck('Hte'), 'The')
        self.assertEqual(spellcheck('ststus'), 'status')
        self.assertEqual(spellcheck('status'), 'status')
        self.assertEqual(spellcheck('help'), 'help')
        self.assertEqual(spellcheck('pool'), 'pool')
        self.assertEqual(spellcheck('subscribe'), 'subscribe')
        self.assertEqual(spellcheck('unsubscribe'), 'unsubscribe')
        self.assertEqual(spellcheck('price'), 'price')

    def testMessages(self):
        self.assertRaises(Exception, Messages.getHelpEmbed())
        self.assertRaises(Exception, Messages.getSubscriptionEmbed())
        self.assertRaises(Exception, Messages.getBlockEmbed())
        self.assertRaises(Exception, Messages.getWinnerEmbed())
        self.assertRaises(Exception, Messages.getNotificationEmbed())
        self.assertRaises(Exception, Messages.getPriceEmbed("burst"))

    def testPriceCommand(self):
        MsgStandalone = MP.price("!price")
        MsgSpecified = MP.price("!price BTC")
        MsgWrong = MP.price("!price Chia")
        self.assertEqual(MsgStandalone.error, None)
        self.assertEqual(MsgSpecified.error, None)
        self.assertIsNot(MsgWrong.error, None)

    def testWebWalletRequest(self):
        testBurstId = "BURST-6QMX-MMUF-QN47-6DQ85"
        testBurstNumericId = "4727314633861519997"
        self.assertRaises(Exception, WebWalletRequests(testBurstId))
        self.assertRaises(Exception, WebWalletRequests(testBurstNumericId))
        WWR = WebWalletRequests(testBurstId)
        self.assertEqual(WWR.burstName, "TUM SEC EI Block Chain Cracker")

    def testUserDatabase(self):
        testBurstId1 = "BURST-6QMX-MMUF-QN47-6DQ85"
        testBurstId2 = "BURST-V5FE-B268-MMUY-44SNJ"
        DB = Users.connectToDB()
        testUser1 = Users.BurstUser(testBurstId1, MockDiscord)
        testUser2 = Users.BurstUser(testBurstId2, MockDiscord)
        self.assertRaises(Exception,Users.addBurstAccounts(DB, [testUser1, testUser2]))
        self.assertEqual(len(Users.getUsersList(DB)), 2)
        self.assertRaises(Exception, Users.deleteBurstAccountByDiscordId(DB, MockDiscord.id))
        self.assertEqual(len(Users.getUsersList(DB)), 0)
        testUser1 = Users.BurstUser(testBurstId1, MockDiscord)
        testUser2 = Users.BurstUser(testBurstId2, MockDiscord)
        self.assertRaises(Exception, Users.addBurstAccounts(DB, [testUser1, testUser2]))
        self.assertRaises(Exception, Users.deleteBurstAccountByBurstId(DB, testBurstId2))
        self.assertEqual(len(Users.getUsersList(DB)), 1)
        testUser1 = Users.BurstUser(testBurstId1, MockDiscord)
        self.assertRaises(Exception, Users.deleteBurstAccountByBurstNumericId(DB, testUser1.burstNumericId))
        self.assertEqual(len(Users.getUsersList(DB)), 0)

    def testPoolDatabase(self):
        DB = Pools.connectToDB()
        testPoolName1 = "0-100-test"
        testPoolUrl1 = "0-100-pool.burst.cryptoguru.org:8008"
        testPoolName2 = "50-50-test"
        testPoolUrl2 = "50-50-pool.burst.cryptoguru.org:8008"
        testPool1 = Pools.Pool(testPoolName1, testPoolUrl1)
        testPool2 = Pools.Pool(testPoolName2, testPoolUrl2)
        self.assertRaises(Exception, Pools.addPoolDataPoint(DB, [testPool1, testPool2]))
        testPool1 = Pools.Pool(testPoolName1, testPoolUrl1)
        self.assertRaises(Exception, Pools.addPoolDataPoint(DB, [testPool1]))
        self.assertRaises(Exception, Pools.getWeeklyReport(DB, testPoolName1))
        self.assertRaises(Exception, Pools.deleteAllDataPointsForPool(DB, testPoolName1))
        self.assertRaises(Exception, Pools.deleteAllDataPointsForPool(DB, testPoolName2))
        #raise NotImplementedError

    def testSubscribers(self):
        raise NotImplementedError

class MockDiscord:
    id = "80351110224678912"
    name = "Wubwub"