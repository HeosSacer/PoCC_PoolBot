from discord.ext import commands
from src.utils import Status
from src.utils import Configuration
from src.utils import Messages
from src.utils import MessageProcessing
from src.utils import LoopProcess
import asyncio


Bot = commands.Bot(command_prefix='!') #TODO, description=msg.poc_bot_description)

Bot.logger = Status.setupLogger()
Bot.config = Configuration.Config()
Bot.logger.info("Discord Bot started!")
# Remove predefined help function
Bot.remove_command('help')


def start():
    Bot.loop.create_task(LoopProcess.Loop(BotHandle=Bot))
    Bot.run(Bot.config.discordToken)

@Bot.event
async def on_ready():
    Status.getOnReadyStatus(Bot)


@Bot.event
async def on_message(msg):
    if msg.channel.name in Bot.config.channelNameList or msg.channel.is_private:
        Bot.logger.info("{0} in {1}: {2}".format(msg.author.name, msg.channel.name, msg.content))
        try:
            await Bot.process_commands(msg)
        except Exception as error:
            Bot.logger.info("{0} in {1}: {2} caught exception ~{3}~".format(msg.author.name, msg.channel.name, msg.content, error))
            Bot.logger.exception("EXCEPTION WHILE PROCESSING MESSAGE:")


@Bot.command()
async def help():
    await Bot.say(Messages.getHelpEmbed())


@Bot.command(pass_context=True)
async def pool(context):
    Message = MessageProcessing.pool(context.message.content, Bot)
    if Message.error:
        Bot.logger.error("Error in !pool: {0} \n {1}".format(Message.error, Message.traceback))
    if not Message.error:
        for embed in Message.content:
            await Bot.send_message(context.message.channel, embed=embed)
    else:
        await Bot.send_message(context.message.channel, embed=Message.content)


@Bot.command(pass_context=True)
async def price(context):
    Message = MessageProcessing.price(context.message.content)
    if Message.error:
        Bot.logger.error("Error in !price: {0} \n {1}".format(Message.error, Message.traceback))
    if not Message.error:
        await Bot.send_message(context.message.channel, embed=Message.content)
    else:
        await Bot.send_message(context.message.channel, Message.content)


@Bot.command()
async def status():
    await Bot.say(Messages.getStatus())