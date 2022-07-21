import discord.errors
from discord.ext import commands, tasks
from utils.fun import embed_meme
import datetime


class ServerTools(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.send_a_meme.start()
        #  self.clear_messages.start()  temporarily unavailable

    @tasks.loop(hours=4)
    async def send_a_meme(self):
        for guild in self.client.guilds:
            if guild.id == 689108090653507616:
                channel = self.client.get_channel(725784429691404329)
                await channel.send(embed=embed_meme())

    @tasks.loop(hours=6)
    async def clear_messages(self):
        for guild in self.client.guilds:
            if guild.id == 689108090653507616:
                channel = self.client.get_channel(968637041501933650)
                async for message in channel.history(limit=None):
                    try:
                        if message.content == '[Original Message Deleted]':
                            await message.delete()
                        if str(message.author)[0:3] == 'LAO' and \
                           message.created_at < (datetime.datetime.now()-datetime.timedelta(hours=6)):
                            await message.delete()
                    except discord.errors.NotFound:
                        pass


def setup(client):
    client.add_cog(ServerTools(client))