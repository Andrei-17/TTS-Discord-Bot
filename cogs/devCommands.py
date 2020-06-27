from discord.ext import commands
import discord
import main

class DevCommands(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.check(main.isDev)
    async def guilds(self, ctx):
        guilds = self.client.guilds
        message = "Current guilds: {}\u0060\u0060\u0060\n".format(len(guilds))
        for guild in guilds:
            message += "{}   \u007c   {}\n".format(str(guild), guild.id)
        message += "\u0060\u0060\u0060"
        await ctx.send(message)

    @commands.command()
    @commands.check(main.isDev)
    async def presence(self, ctx, activity):
        activity = activity.lower()
        if activity == "online":
            await self.client.change_presence(status=discord.Status.online)
            activityText = "Online"
        elif activity == "dnd":
            await self.client.change_presence(status=discord.Status.dnd)
            activityText = "Do Not Disturb"
        elif activity == "idle":
            await self.client.change_presence(status=discord.Status.idle)
            activityText = "Idle"
        elif activity == "invisible":
            await self.client.change_presence(status=discord.Status.invisible)
            activityText = "Invisible"
        else:
            activityText = None
        if activityText:
            await ctx.send("The presence has been changed to: {}.".format(activityText))
        else:
            await ctx.send("The activity you specified is incorrect.")

def setup(client):
    client.add_cog(DevCommands(client))