from discord.ext import commands
from src.utils import status
import logging
import logging.handlers
import asyncio


Bot = commands.Bot(command_prefix='!') #TODO, description=msg.poc_bot_description)

Bot.logger = status.setup_logger()
Bot.logger.info("Discord Bot started!")
# Remove predefined help function
Bot.remove_command('help')


@Bot.event
async def on_ready():
    status.get_on_ready_status(Bot)


@Bot.event
async def on_message(msg):
    if msg.channel.name in config.CHANNEL_NAMES or msg.channel.is_private:
        Bot.logger.info("{0} in {1}: {2}".format(msg.author.name, msg.channel.name, msg.content))
        await Bot.process_commands(msg)