import logging
import datetime
from os import path


def setup_logger():
    logging.basicConfig(level=logging.DEBUG)
    logFormatter = logging.Formatter("%(asctime)s [%(levelname)-5.5s]  %(message)s")
    rootLogger = logging.getLogger()

    basePath = path.dirname(__file__)
    logPath = path.abspath(path.join(basePath, "..", "..")) + "\\log\\"
    now = datetime.datetime.now()
    fileName = "%s" % str(now.strftime("%Y-%m-%d_%H-%M"))
    fileHandler = logging.FileHandler("{0}/{1}.log".format(logPath, fileName))
    fileHandler.setFormatter(logFormatter)
    rootLogger.addHandler(fileHandler)
    rootLogger.info("Log-File created!")
    return rootLogger


def get_on_ready_status(Bot):
    print('=====================')
    print('Logged in as')
    print(Bot.user.name)
    print('=====================')
    print('Connected Servers:')
    for server in Bot.servers:
        print(server.name)
        for channel in server.channels:
            try:
                print('|- ' + channel.name)
            except UnicodeEncodeError:
                # TODO: Handle UTF-8 channel names
                pass
    print('=====================')