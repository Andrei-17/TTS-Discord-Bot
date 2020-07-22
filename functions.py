import json
import datetime

def getConfig():
    config = json.load(open("json/config.json"))
    return config

def getHelpMessage():
    help = open("txt/help.txt").read()
    return help

def getLanguage(serverID : int):
    tts_settings = json.load(open("json/tts_settings.json"))
    try:
        language = tts_settings[str(serverID)]
    except KeyError:
        setLanguage(serverID, "en-us")
        language = "en-us"
    return language

def getPolly():
    polly = json.load(open("json/languages.json"))["polly"]
    return polly

def getPollyChars():
    file = open("polly_chars.txt").read()
    if file.endswith("\n"):
        file = file[:-1]
    return file

def setLanguage(serverID : int, language : str):
    tts_settings = json.load(open("json/tts_settings.json"))
    tts_settings[str(serverID)] = language
    with open("json/tts_settings.json", "w") as file:
        json.dump(tts_settings, file, indent=2)

def getLanguageList():
    return json.load(open("json/languages.json"))

def updateTime(guildID : int):
    time = datetime.datetime.now()
    timeJson = {
        "year": time.year,
        "month": time.month,
        "day": time.day,
        "hour": time.hour,
        "minute": time.minute,
        "second": time.second
    }
    loopJson = json.load(open("json/disconnectLoop.json"))
    loopJson[str(guildID)] = timeJson
    with open("json/disconnectLoop.json", "w") as file:
        json.dump(loopJson, file, indent=2)

def getTime(guildID : int):
    loopJson = json.load(open("json/disconnectLoop.json"))
    timeJson = loopJson[str(guildID)]
    time = datetime.datetime(
        year = timeJson["year"],
        month = timeJson["month"],
        day = timeJson["day"],
        hour = timeJson["hour"],
        minute = timeJson["minute"],
        second = timeJson["second"]
    )
    return time

def toDisconnect(guildID : int):
    time = datetime.datetime.now()
    guildTime = getTime(guildID)
    seconds = (time - guildTime).seconds
    if seconds > 300:
        return True
    return False
