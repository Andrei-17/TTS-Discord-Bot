from discord.ext import commands
from discord.ext.tasks import loop
from discord.utils import get
import discord
from itertools import cycle
import datetime
import json
import functions

class VoiceChat(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        self.disconnectLoop.start()

    @commands.command(aliases=["j"])
    async def join(self, ctx):
        authorVoice = ctx.message.author.voice
        if authorVoice == None:
            await ctx.send("You are not in a voice channel!")
        else:
            channel = authorVoice.channel
            voice = get(self.client.voice_clients, guild=ctx.guild)
            if voice and voice.is_connected():
                if not voice.channel.id == channel.id:
                    await voice.move_to(channel)
                    message = "Successfully connected to \"{}\" channel.".format(channel)
                    functions.updateTime(ctx.guild.id)
                else:
                    message = "I am already in this voice channel!"
            else:
                voice = await channel.connect()
                message = "Successfully connected to \"{}\" channel.".format(channel)
                functions.updateTime(ctx.guild.id)
            await ctx.send(message)

    @commands.command(aliases=["disconnect", "l"])
    async def leave(self, ctx):
        authorVoice = ctx.message.author.voice
        if authorVoice == None:
            await ctx.send("You are not in a voice channel!")
        else:
            channel = authorVoice.channel
            voice = get(self.client.voice_clients, guild=ctx.guild)
            if voice.channel.id == channel.id:
                if voice and voice.is_connected():
                    await voice.disconnect()
                    await ctx.send("Successfully disconnected from \"{}\" channel.".format(channel))
                else:
                    await ctx.send("I am not in a voice channel!")
            else:
                await ctx.send("<@{}> we are not in the same voice channel!".format(ctx.message.author.id))

    @loop(seconds=10.0)
    async def disconnectLoop(self):
        for guild in self.client.guilds:
            voice = get(self.client.voice_clients, guild=guild)
            if voice and voice.is_connected() and functions.toDisconnect(guild.id):
                await voice.disconnect()


def setup(client):
    client.add_cog(VoiceChat(client))