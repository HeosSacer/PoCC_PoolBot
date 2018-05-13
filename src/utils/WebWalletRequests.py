import requests

# define request strings
requestType = 'https://wallet1.burst-team.us:2083/burst?requestType='  # 'https://wallet.burst.cryptoguru.org:8125/burst?requestType='
getBlockHeight = requestType + 'getBlock&height='
getMiningInfo = requestType + 'getMiningInfo'
getAccount = requestType + 'getAccount&account='
getRewardRecipient = requestType + 'getRewardRecipient&account='
getAccountTransactions = requestType + 'getAccountTransactions&account='


class WebWalletRequests:
    def __init__(self, burstIdOrNumeric):
        self.burstName = self.getAccountName(burstIdOrNumeric)
        (self.burstNumericId, self.burstId) = self.getAccountBurstIds(burstIdOrNumeric)
        self.balance = self.getAccountBalance(burstIdOrNumeric)
        self.rewardRecipientId, self.rewardRecipientNumericalId, self.rewardRecipientName = \
            self.getRewardRecipient(self.burstId)

    @staticmethod
    def getSpecificBlockByHeight(height):
        r = requests.get(getBlockHeight + str(int(height)))
        if r.status_code != requests.codes.ok:
            return
        try:
            minerId = r.json()['generatorRS']
            blockId = r.json()['block']
        except KeyError:
            minerId = None
            blockId = None
        return minerId, blockId

    @staticmethod
    def getLastMinedBlock():
        """returns last mined block"""
        r = requests.get(getMiningInfo)
        if r.status_code != requests.codes.ok:
            return
        blockHeight = int(r.json()['height'])
        return str(blockHeight-1)

    def getAccountName(self, minerId):
        """returns nick of a burst id, returns BURST-XXX if not set"""
        r = requests.get(getAccount + '%s' % minerId)
        if r.status_code != requests.codes.ok:
            return
        msg = r.json()
        try:
            minerName = msg['name']
        # if miner has no name
        except KeyError:
            minerName = msg['accountRS']
        return minerName

    def getAccountBurstIds(self, minerId):
        r = requests.get(getAccount + '%s' % minerId)
        if r.status_code != requests.codes.ok:
            return
        msg = r.json()
        numericalId = msg['account']
        burstId = msg['accountRS']
        return numericalId, burstId

    @staticmethod
    def getAccountBalance(minerId):
        r = requests.get(getAccount + '%s' % minerId)
        if r.status_code != requests.codes.ok:
            return
        msg = r.json()
        balance = float(int(msg['balanceNQT'])/100000000)
        return balance

    def getRewardRecipient(self, burstId):
        """gets pool name/ name of reward recipient"""
        r = requests.get(getRewardRecipient + '%s' % burstId)
        if r.status_code != requests.codes.ok:
            return
        msg = r.json()
        try:
            recipientName = self.getAccountName(msg['rewardRecipient'])
        # if miner is alone
        except KeyError:
            recipientName = None
        recipientId, recipientNumericalId = self.getAccountBurstIds(msg['rewardRecipient'])
        return recipientId, recipientNumericalId, recipientName

    @staticmethod
    def getAccountTransactions(burstId, numberOfTransactions = 1):
        """gets last transactions of a burst account"""
        r = requests.get(getAccountTransactions + '%s&firstIndex=0&lastIndex=%i' % (burstId, numberOfTransactions))
        if r.status_code != requests.codes.ok:
            return
        msg = r.json()
        try:
            transactionsList = []
            transactions = msg['transactions']
            for transaction in transactions:
                transactionsList.append({'sender': transaction['sender'],
                                          'amount': float(transaction['amountNQT'])/100000000,
                                          'acc_id': transaction['recipient'],
                                          'timestamp': transaction['timestamp']})
        # if no transactions are there
        except KeyError:
            transactionsList = None
        return transactionsList
