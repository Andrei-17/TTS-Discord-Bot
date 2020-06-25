from discord.ext import commands
from discord.utils import get
import discord
import modules.tts_module
import functions
import os

class TextToSpeech(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def tts(self, ctx, *, text : str):
        text_words = text.split()
        if text_words[0] == "language" or text_words[0] == "languages" or text_words[0] == "lang" or text_words[0] == "langs":
            if len(text_words) > 1:
                if text_words[1].lower() == "current":
                    await self.currentLang(ctx)
                else:
                    await self.setLang(ctx, text_words[1].lower())
            else:
                await self.langList(ctx)
        else:
            functions.updateTime(ctx.guild.id)
            await self.play(ctx, text)

    async def langList(self, ctx):
        langs = functions.getLanguageList()
        message = "Available languages:\u0060\u0060\u0060"
        for key in langs["langs"].keys():
            message += f"\n{key}   \u2192   {langs['langs'][key]}"
        message += "\u0060\u0060\u0060"
        await ctx.send(message)

    async def setLang(self, ctx, lang):
        try:
            current_lang = functions.getLanguage(ctx.message.guild.id)
        except KeyError:
            current_lang = None
        langs = functions.getLanguageList()
        invLangs = {v: k for k, v in langs["langs"].items()}
        if lang.capitalize() in invLangs:
            lang = invLangs[lang.capitalize()]
        if lang in langs["langs"]:
            if lang in langs["exceptions"]:
                toChange = langs["exceptions"][lang]
            else:
                toChange = lang
            if toChange == current_lang:
                await ctx.send("This language is already set.")
            else:
                functions.setLanguage(ctx.message.guild.id, toChange)
                await ctx.send("The language has been successfully changed to: {}".format(langs["langs"][lang]))
        else:
            await ctx.send("This language is not supported.")

    async def currentLang(self, ctx):
        langs = functions.getLanguageList()
        current_lang = functions.getLanguage(ctx.message.guild.id)
        invExceptions = {v: k for k, v in langs["exceptions"].items()}
        if current_lang in invExceptions:
            current_lang = invExceptions[current_lang]
        await ctx.send("The current language set is: {}".format(langs["langs"][current_lang]))

    async def play(self, ctx, text):
        authorVoice = ctx.message.author.voice
        if authorVoice == None:
            await ctx.send("You are not in a voice channel!")
        else:
            channel = authorVoice.channel
            voice = get(self.client.voice_clients, guild=ctx.guild)
            if voice and voice.is_connected():
                if not voice.channel.id == channel.id:
                    await voice.move_to(channel)
            else:
                voice = await channel.connect()
            if voice.is_playing():
                await ctx.send(f"<@{ctx.message.author.id}>, the previous command is not done yet.")
                await ctx.message.add_reaction(emoji="\u274c")
            else:
                guildID = ctx.message.guild.id
                lang = functions.getLanguage(guildID)
                polly = functions.getPolly()
                if lang in polly:
                    audio_path = modules.tts_module.polly(text, guildID, polly[lang])
                else:
                    audio_path = modules.tts_module.googleTTS(text, guildID, lang)
                await ctx.message.add_reaction(emoji="\u2705")
                voice.play(discord.FFmpegPCMAudio(audio_path))
                while voice.is_playing():
                    pass
                os.unlink(audio_path)
                voice.source = discord.PCMVolumeTransformer(voice.source)
                voice.source.volume = 0.70

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        functions.setLanguage(guild.id, "en-us")

def setup(client):
    client.add_cog(TextToSpeech(client))