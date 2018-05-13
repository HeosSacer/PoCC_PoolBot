from src.utils.pool_api import api_pb2, api_pb2_grpc
import grpc
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
import datetime

cwd = os.getcwd()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'sqlite:////{0}/UserAndPool.db'.format(cwd)
db = SQLAlchemy(app)


class Pool(db.Model):
    __tablename__ = "pool_data"
    timestamp = db.Column(db.String(20), primary_key=True)
    poolName = db.Column(db.Unicode(40))
    minerCount = db.Column(db.String(40))
    poolCapacityInTB = db.Column(db.String(20))

    def __init__(self, poolName, poolAddr):
        poolStats = self.getPoolStats(poolAddr = poolAddr)
        self.timestamp = str(datetime.datetime.utcnow())
        self.minerCount = poolStats.minerCount
        self.poolCapacityInTB = poolStats.effectivePoolCapacity
        self.poolName = poolName

    @staticmethod
    def getPoolStats(poolAddr='0-100-pool.burst.cryptoguru.org:8008'):
        channel = grpc.insecure_channel(poolAddr)
        stub = api_pb2_grpc.ApiStub(channel)
        poolStats = stub.GetPoolStatsInfo(api_pb2.Void())
        block_info = stub.GetBlockInfo(api_pb2.Void())
        return poolStats


def connectToDB():
    db.create_all()
    #Session = sessionmaker(bind=engine)
    return db


def getWeeklyReport(DB, _poolName):
    poolStatsList = []
    for poolDatum in DB.session.query(Pool).filter(Pool.poolName ==_poolName).all():
        fmt = "%Y-%m-%d %H:%M:%S.%f"
        poolDatum.timestamp = datetime.datetime.strptime(poolDatum.timestamp, fmt)
        poolStatsList.append(poolDatum)
    poolStatsList.sort(key=lambda obj: obj.timestamp, reverse=True)
    weekOfPoolStats = [poolStatsList[0]]
    i = 1
    timeDelta = poolStatsList[0].timestamp - poolStatsList[i].timestamp
    while timeDelta.days <= 7:
        weekOfPoolStats.append(poolStatsList[i])
        i+=1
        if i < len(poolStatsList):
            timeDelta = poolStatsList[0].timestamp - poolStatsList[i].timestamp
        else:
            break
    return weekOfPoolStats


def addPoolDataPoint(DB, PoolObjList):
    for PoolObj in PoolObjList:
        DB.session.add(PoolObj)
    DB.session.commit()


def deleteAllDataPointsForPool(DB, _poolName):
    DB.session.query(Pool).filter(Pool.poolName == _poolName).delete()
    DB.session.commit()
