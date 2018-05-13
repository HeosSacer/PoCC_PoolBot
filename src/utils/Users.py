from src.utils.WebWalletRequests import WebWalletRequests
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os


cwd = os.getcwd()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'sqlite:////{0}/UserAndPool.db'.format(cwd)
db = SQLAlchemy(app)


class BurstUser(db.Model):
    __tablename__ = 'burst_users'
    discordId = db.Column(db.String(20))
    discordName = db.Column(db.Unicode(40))
    burstName = db.Column(db.Unicode(40))
    burstId = db.Column(db.String(20), primary_key=True)
    burstNumericId = db.Column(db.String(20))
    lastWonBlock = db.Column(db.String(20))
    lastWonBlockTime = db.Column(db.String(20))
    lastPayout = db.Column(db.String(20))
    lastPayoutTime = db.Column(db.String(20))
    rewardRecipientId = db.Column(db.String(20))
    rewardRecipientNumericalId = db.Column(db.String(20))
    rewardRecipientName = db.Column(db.String(20))
    balance = db.Column(db.Integer)

    def __init__(self, burstCredentials, discordUserHandle):
        try:
            WWR = WebWalletRequests(burstCredentials)
        except Exception as error:
            raise ValueError
        self.burstName = WWR.burstName
        self.burstNumericId = WWR.burstNumericId
        self.burstId = WWR.burstId
        self.balance = WWR.balance
        self.lastWonBlock = None
        self.lastWonBlockTime = None
        self.lastPayout = None
        self.lastPayoutTime = None
        self.rewardRecipientId = WWR.rewardRecipientId
        self.rewardRecipientNumericalId = WWR.rewardRecipientNumericalId
        self.rewardRecipientName= WWR.rewardRecipientName
        self.discordId = discordUserHandle.id
        self.discordName = discordUserHandle.name


def connectToDB():
    db.create_all()
    #Session = sessionmaker(bind=engine)
    return db


def getUsersList(DB):
    userList = []
    for user in BurstUser.query.all():
        userList.append(user)
    return userList


def addBurstAccounts(DB, BurstUserObjList):
    for BurstUserObj in BurstUserObjList:
        DB.session.add(BurstUserObj)
    DB.session.commit()


def deleteBurstAccountByDiscordId(DB, discordId):
    BurstUser.query.filter_by(discordId=discordId).delete()
    DB.session.commit()


def deleteBurstAccountByBurstId(DB, burstId):
    BurstUser.query.filter_by(burstId=burstId).delete()
    DB.session.commit()


def deleteBurstAccountByBurstNumericId(DB, burstNumericId):
    BurstUser.query.filter_by(burstNumericId=burstNumericId).delete()
    DB.session.commit()
