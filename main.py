from discord.ext import commands
import discord
import functions
import os

TOKEN = os.environ.get("TOKEN")

client = bot = commands.Bot(command_prefix = os.environ.get("PREFIX"))
bot.remove_command('help')

def load_cogs():
    for file in os.listdir("./cogs"):
        if file != "__pycache__":
            client.load_extension(f"cogs.{file[:-3]}")

def unload_cogs():
    for file in os.listdir("./cogs"):
        if file != "__pycache__":
            client.unload_extension(f"cogs.{file[:-3]}")

def isDev(ctx):
    devID = os.environ.get("DEV_ID")
    if ctx.message.author.id == int(devID):
        return True
    return False

@client.event
async def on_ready():
    print("Bomber Bot is running.")
    await client.change_presence(activity=discord.Game("version {}".format(os.environ.get("VERSION"))))

#@client.event
#async def on_command_error(ctx, error):
    #pass

@client.command(aliases=["h"])
async def help(ctx):
    message = functions.getHelpMessage()
    await ctx.send(message)

@client.command()
@commands.check(isDev)
async def limit(ctx):
    charsNum = functions.getPollyChars()
    await ctx.send("Current limit:\u0060\u0060\u0060\n{} / 100000\u0060\u0060\u0060".format(charsNum))

@client.command()
@commands.check(isDev)
async def reload(ctx):
    unload_cogs()
    load_cogs()
    print("The extensions have been reloaded.")
    await ctx.send("\u0060\u0060\u0060The extensions have been reloaded.\u0060\u0060\u0060")

if __name__ == "__main__":
    load_cogs()
    client.run(TOKEN)