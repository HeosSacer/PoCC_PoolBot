from os import path
import configparser


config.read('config.ini')

class Config(config):
    def __init__(self):
        self.read_config_file()

    def read_config_file(self):
        basePath = path.dirname(__file__)
        configFilePath = path.abspath(path.join(basePath, "..", "..")) + "config.ini"
        self.ConfigFile = configparser.ConfigParser()
        self.ConfigFile.read(configFilePath)

    def get_bot_config(self):

    def get_discord_config(self):


    def get_pool_info(self):